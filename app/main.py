from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.encoders import jsonable_encoder 
from app.models.schemas import (
    VehiculoCrear, VehiculoActualizar,
    ComandoCrear, ComandoActualizar,
    EstadoActualizar, HistorialRegistrar, MovimientoIndividual,
    DemoCrear, DemoActualizar,
    DemoMovimientoCrear, DemoMovimientoActualizar
)
from app.repositories.iot_repository import IoTRepository
from app.services.vehiculo_service import vehiculo_service
from app.websocket.websocket_manager import ws_manager

app = FastAPI(
    title="API Vehículo IoT - 21 Stored Procedures & WebSocket",
    description="Sistema de control telemático y DEMO para vehículo IoT con Amazon RDS y FastAPI",
    version="2.0"
)

repo = IoTRepository()

# ==========================================
# 1 a 5: VEHÍCULOS (sp_crear_vehiculo, sp_obtener_vehiculos, sp_obtener_vehiculo, sp_actualizar_vehiculo, sp_eliminar_vehiculo)
# ==========================================
@app.post("/vehiculos", tags=["Vehículos"], summary="SP: sp_crear_vehiculo")
def crear_vehiculo(v: VehiculoCrear):
    return repo.sp_crear_vehiculo(v.nombre, v.modelo, v.descripcion, v.microcontrolador)

@app.get("/vehiculos", tags=["Vehículos"], summary="SP: sp_obtener_vehiculos")
def obtener_vehiculos():
    return repo.sp_obtener_vehiculos()

@app.get("/vehiculos/{id_vehiculo}", tags=["Vehículos"], summary="SP: sp_obtener_vehiculo")
def obtener_vehiculo(id_vehiculo: int):
    res = repo.sp_obtener_vehiculo(id_vehiculo)
    if not res:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return res

@app.post("/vehiculos/{id_vehiculo}/actualizar", tags=["Vehículos"], summary="SP: sp_actualizar_vehiculo")
def actualizar_vehiculo(id_vehiculo: int, v: VehiculoActualizar):
    return repo.sp_actualizar_vehiculo(id_vehiculo, v.nombre, v.modelo, v.descripcion, v.microcontrolador, v.activo)

@app.post("/vehiculos/{id_vehiculo}/eliminar", tags=["Vehículos"], summary="SP: sp_eliminar_vehiculo")
def eliminar_vehiculo(id_vehiculo: int):
    return repo.sp_eliminar_vehiculo(id_vehiculo)

# ==========================================
# 6 a 9: COMANDOS (sp_crear_comando, sp_obtener_comandos_vehiculo, sp_actualizar_comando, sp_eliminar_comando)
# ==========================================
@app.post("/comandos", tags=["Comandos"], summary="SP: sp_crear_comando")
def crear_comando(c: ComandoCrear):
    return repo.sp_crear_comando(c.id_vehiculo, c.nombre, c.codigo, c.descripcion)

@app.get("/vehiculos/{id_vehiculo}/comandos", tags=["Comandos"], summary="SP: sp_obtener_comandos_vehiculo")
def obtener_comandos_vehiculo(id_vehiculo: int):
    return repo.sp_obtener_comandos_vehiculo(id_vehiculo)

@app.post("/comandos/{id_comando}/actualizar", tags=["Comandos"], summary="SP: sp_actualizar_comando")
def actualizar_comando(id_comando: int, c: ComandoActualizar):
    return repo.sp_actualizar_comando(id_comando, c.nombre, c.codigo, c.descripcion, c.activo)

@app.post("/comandos/{id_comando}/eliminar", tags=["Comandos"], summary="SP: sp_eliminar_comando")
def eliminar_comando(id_comando: int):
    return repo.sp_eliminar_comando(id_comando)

# ==========================================
# 10 a 11: ESTADO (sp_actualizar_estado, sp_obtener_estado)
# ==========================================
@app.post("/vehiculos/{id_vehiculo}/estado", tags=["Estado"], summary="SP: sp_actualizar_estado")
def actualizar_estado(id_vehiculo: int, e: EstadoActualizar):
    return repo.sp_actualizar_estado(id_vehiculo, e.id_comando, e.conectado)

@app.get("/vehiculos/{id_vehiculo}/estado", tags=["Estado"], summary="SP: sp_obtener_estado")
def obtener_estado(id_vehiculo: int):
    res = repo.sp_obtener_estado(id_vehiculo)
    if not res:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return res

# ==========================================
# 12 a 13: HISTORIAL (sp_registrar_historial, sp_obtener_historial)
# ==========================================
@app.post("/vehiculos/{id_vehiculo}/historial", tags=["Historial"], summary="SP: sp_registrar_historial")
def registrar_historial(id_vehiculo: int, h: HistorialRegistrar):
    return repo.sp_registrar_historial(id_vehiculo, h.id_comando, h.origen)

@app.get("/vehiculos/{id_vehiculo}/historial", tags=["Historial"], summary="SP: sp_obtener_historial (Máx 10)")
def obtener_historial(id_vehiculo: int):
    # Regla: Máximo 10 movimientos más recientes
    return vehiculo_service.obtener_historial_reciente(id_vehiculo, limite=10)

# ==========================================
# 14 a 17: DEMOS (sp_crear_demo, sp_obtener_demos, sp_actualizar_demo, sp_eliminar_demo)
# ==========================================
@app.post("/demos", tags=["Demos"], summary="SP: sp_crear_demo")
def crear_demo(d: DemoCrear):
    return repo.sp_crear_demo(d.id_vehiculo, d.nombre, d.descripcion)

@app.get("/vehiculos/{id_vehiculo}/demos", tags=["Demos"], summary="SP: sp_obtener_demos")
def obtener_demos(id_vehiculo: int):
    return repo.sp_obtener_demos(id_vehiculo)

@app.post("/demos/{id_demo}/actualizar", tags=["Demos"], summary="SP: sp_actualizar_demo")
def actualizar_demo(id_demo: int, d: DemoActualizar):
    return repo.sp_actualizar_demo(id_demo, d.nombre, d.descripcion, d.activo)

@app.post("/demos/{id_demo}/eliminar", tags=["Demos"], summary="SP: sp_eliminar_demo")
def eliminar_demo(id_demo: int):
    return repo.sp_eliminar_demo(id_demo)

# ==========================================
# 18 a 21: MOVIMIENTOS DEMO (sp_agregar_movimiento_demo, sp_obtener_movimientos_demo, sp_actualizar_movimiento_demo, sp_eliminar_movimiento_demo)
# ==========================================
@app.post("/demos/{id_demo}/movimientos", tags=["Movimientos Demo"], summary="SP: sp_agregar_movimiento_demo")
def agregar_movimiento_demo(id_demo: int, m: DemoMovimientoCrear):
    return repo.sp_agregar_movimiento_demo(id_demo, m.id_comando, m.orden, m.duracion_ms, m.pausa_ms)

@app.get("/demos/{id_demo}/movimientos", tags=["Movimientos Demo"], summary="SP: sp_obtener_movimientos_demo")
def obtener_movimientos_demo(id_demo: int):
    return repo.sp_obtener_movimientos_demo(id_demo)

@app.post("/demos/movimientos/{id_mov}/actualizar", tags=["Movimientos Demo"], summary="SP: sp_actualizar_movimiento_demo")
def actualizar_movimiento_demo(id_mov: int, m: DemoMovimientoActualizar):
    return repo.sp_actualizar_movimiento_demo(id_mov, m.id_comando, m.orden, m.duracion_ms, m.pausa_ms)

@app.post("/demos/movimientos/{id_mov}/eliminar", tags=["Movimientos Demo"], summary="SP: sp_eliminar_movimiento_demo")
def eliminar_movimiento_demo(id_mov: int):
    return repo.sp_eliminar_movimiento_demo(id_mov)

# ==========================================
# FLUJOS CRÍTICOS: MOVIMIENTO INDIVIDUAL Y CONTROL DE DEMO
# ==========================================
@app.post("/vehiculos/{id_vehiculo}/movimiento", tags=["Control Operativo"], summary="Ejecutar Movimiento Individual (Transacción)")
async def ejecutar_movimiento(id_vehiculo: int, mov: MovimientoIndividual):
    return await vehiculo_service.ejecutar_movimiento_individual(id_vehiculo, mov.id_comando, mov.origen)

@app.post("/vehiculos/{id_vehiculo}/demos/{id_demo}/iniciar", tags=["Control Operativo"], summary="Iniciar DEMO (WebSocket sin historial)")
async def iniciar_demo(id_vehiculo: int, id_demo: int):
    return await vehiculo_service.iniciar_demo(id_vehiculo, id_demo)

@app.post("/vehiculos/{id_vehiculo}/demos/cancelar", tags=["Control Operativo"], summary="Cancelar DEMO en curso")
async def cancelar_demo(id_vehiculo: int):
    return await vehiculo_service.cancelar_demo(id_vehiculo)

# ==========================================
# CANAL WEBSOCKET POR VEHÍCULO
# ==========================================
@app.websocket("/ws/vehiculos/{id_vehiculo}")
@app.websocket("/ws")  # Alias para evitar errores si no se pone el ID
async def websocket_vehiculo(websocket: WebSocket, id_vehiculo: int = 1):
    await ws_manager.conectar(id_vehiculo, websocket)
    
    # Entregar de inmediato el último estado guardado en RDS
    try:
        ultimo_estado = repo.sp_obtener_estado(id_vehiculo)
        if ultimo_estado:
            # jsonable_encoder convierte las fechas de MySQL a texto ISO automáticamente
            await websocket.send_json(jsonable_encoder({
                "tipo": "ESTADO_INICIAL",
                "datos": ultimo_estado
            }))
        
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.desconectar(id_vehiculo, websocket)
    except Exception as e:
        print(f"Error en WebSocket: {e}")
        ws_manager.desconectar(id_vehiculo, websocket)