import asyncio
from datetime import datetime
from fastapi import HTTPException
from app.database import DatabaseManager
from app.repositories.iot_repository import IoTRepository
from app.websocket.websocket_manager import ws_manager

class VehiculoService:
    def __init__(self):
        self.repo = IoTRepository()
        # Control de demos activas: id_vehiculo -> asyncio.Task
        self.demos_en_ejecucion: dict[int, asyncio.Task] = {}

    def obtener_historial_reciente(self, id_vehiculo: int, limite: int = 10):
        """Consulta sp_obtener_historial y devuelve como máximo 10 registros."""
        todos = self.repo.sp_obtener_historial(id_vehiculo)
        # Los SP ya vienen ordenados DESC por fecha_hora
        return todos[:limite]

    async def ejecutar_movimiento_individual(self, id_vehiculo: int, id_comando: int, origen: str):
        """Regla de negocio: Transacción atómica estado + historial y notificación WebSocket."""
        # Validar vehículo
        vehiculo = self.repo.sp_obtener_vehiculo(id_vehiculo)
        if not vehiculo or not vehiculo.get("activo"):
            raise HTTPException(status_code=404, detail="Vehículo no encontrado o inactivo")

        # Validar comando perteneciente a este vehículo
        comandos = self.repo.sp_obtener_comandos_vehiculo(id_vehiculo)
        comando_valido = next((c for c in comandos if c["id_comando"] == id_comando and c["activo"]), None)
        if not comando_valido:
            raise HTTPException(status_code=400, detail="Comando inválido o no pertenece a este vehículo")

        # Transacción atómica directa en RDS
        with DatabaseManager.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    # 1. Actualizar estado
                    cursor.callproc("sp_actualizar_estado", (id_vehiculo, id_comando, True))
                    # 2. Registrar historial
                    cursor.callproc("sp_registrar_historial", (id_vehiculo, id_comando, origen))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise HTTPException(status_code=500, detail=f"Error en la transacción: {str(e)}")

        # Notificar por WebSocket a todos los clientes del vehículo
        evento = {
            "tipo": "MOVIMIENTO_INDIVIDUAL",
            "id_vehiculo": id_vehiculo,
            "id_comando": id_comando,
            "comando": comando_valido["nombre"],
            "codigo": comando_valido["codigo"],
            "origen": origen,
            "timestamp": datetime.now().isoformat()
        }
        await ws_manager.emitir_a_vehiculo(id_vehiculo, evento)
        return {"resultado": "OK", "evento": evento}

    async def _tarea_ejecutar_demo(self, id_vehiculo: int, id_demo: int):
        """Ejecuta los N movimientos ordenados por WebSocket SIN tocar el historial."""
        try:
            movimientos = self.repo.sp_obtener_movimientos_demo(id_demo)
            if not movimientos:
                return

            # Evento Inicio
            await ws_manager.emitir_a_vehiculo(id_vehiculo, {
                "tipo": "DEMO_INICIO",
                "id_vehiculo": id_vehiculo,
                "id_demo": id_demo,
                "total_movimientos": len(movimientos),
                "timestamp": datetime.now().isoformat()
            })

            for mov in movimientos:
                # 1. Actualizar estado (pero NUNCA registrar historial)
                self.repo.sp_actualizar_estado(id_vehiculo, mov["id_comando"], True)

                # 2. Emitir evento del movimiento
                await ws_manager.emitir_a_vehiculo(id_vehiculo, {
                    "tipo": "DEMO_MOVIMIENTO",
                    "orden": mov["orden"],
                    "id_comando": mov["id_comando"],
                    "comando": mov["comando"],
                    "codigo": mov["codigo"],
                    "duracion_ms": mov["duracion_ms"],
                    "pausa_ms": mov["pausa_ms"],
                    "timestamp": datetime.now().isoformat()
                })

                # 3. Esperar duración y pausa de forma asíncrona (no bloqueante)
                await asyncio.sleep(mov["duracion_ms"] / 1000.0)
                if mov["pausa_ms"] > 0:
                    await asyncio.sleep(mov["pausa_ms"] / 1000.0)

            # Evento Fin
            await ws_manager.emitir_a_vehiculo(id_vehiculo, {
                "tipo": "DEMO_FIN",
                "id_vehiculo": id_vehiculo,
                "id_demo": id_demo,
                "timestamp": datetime.now().isoformat()
            })
        except asyncio.CancelledError:
            await ws_manager.emitir_a_vehiculo(id_vehiculo, {
                "tipo": "DEMO_CANCELADA",
                "id_vehiculo": id_vehiculo,
                "timestamp": datetime.now().isoformat()
            })
        finally:
            self.demos_en_ejecucion.pop(id_vehiculo, None)

    async def iniciar_demo(self, id_vehiculo: int, id_demo: int):
        if id_vehiculo in self.demos_en_ejecucion:
            raise HTTPException(status_code=409, detail="Ya hay una DEMO en ejecución para este vehículo")

        tarea = asyncio.create_task(self._tarea_ejecutar_demo(id_vehiculo, id_demo))
        self.demos_en_ejecucion[id_vehiculo] = tarea
        return {"mensaje": "DEMO iniciada exitosamente", "id_demo": id_demo}

    async def cancelar_demo(self, id_vehiculo: int):
        tarea = self.demos_en_ejecucion.get(id_vehiculo)
        if not tarea:
            raise HTTPException(status_code=400, detail="No hay ninguna DEMO activa para este vehículo")
        tarea.cancel()
        return {"mensaje": "DEMO cancelada"}

vehiculo_service = VehiculoService()