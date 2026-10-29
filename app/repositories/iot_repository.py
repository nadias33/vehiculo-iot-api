from app.database import DatabaseManager

class IoTRepository:
    """Capa de acceso a datos que implementa los 21 Stored Procedures en MySQL/RDS."""

    # ------------------ 1 a 5: VEHÍCULOS ------------------
    def sp_crear_vehiculo(self, nombre, modelo, descripcion, microcontrolador):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_crear_vehiculo", (nombre, modelo, descripcion, microcontrolador))
                res = cursor.fetchone()
                conn.commit()
                return res

    def sp_obtener_vehiculos(self):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_vehiculos")
                return cursor.fetchall()

    def sp_obtener_vehiculo(self, id_vehiculo: int):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_vehiculo", (id_vehiculo,))
                return cursor.fetchone()

    def sp_actualizar_vehiculo(self, id_vehiculo: int, nombre, modelo, descripcion, micro, activo: bool):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_actualizar_vehiculo", (id_vehiculo, nombre, modelo, descripcion, micro, activo))
                conn.commit()
                return {"mensaje": "Vehículo actualizado exitosamente"}

    def sp_eliminar_vehiculo(self, id_vehiculo: int):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_eliminar_vehiculo", (id_vehiculo,))
                conn.commit()
                return {"mensaje": "Vehículo eliminado exitosamente"}

    # ------------------ 6 a 9: COMANDOS ------------------
    def sp_crear_comando(self, id_vehiculo: int, nombre, codigo: int, descripcion):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_crear_comando", (id_vehiculo, nombre, codigo, descripcion))
                res = cursor.fetchone()
                conn.commit()
                return res

    def sp_obtener_comandos_vehiculo(self, id_vehiculo: int):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_comandos_vehiculo", (id_vehiculo,))
                return cursor.fetchall()

    def sp_actualizar_comando(self, id_comando: int, nombre, codigo: int, descripcion, activo: bool):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_actualizar_comando", (id_comando, nombre, codigo, descripcion, activo))
                conn.commit()
                return {"mensaje": "Comando actualizado exitosamente"}

    def sp_eliminar_comando(self, id_comando: int):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_eliminar_comando", (id_comando,))
                conn.commit()
                return {"mensaje": "Comando eliminado exitosamente"}

    # ------------------ 10 a 11: ESTADO ------------------
    def sp_actualizar_estado(self, id_vehiculo: int, id_comando, conectado: bool):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_actualizar_estado", (id_vehiculo, id_comando, conectado))
                conn.commit()
                return {"mensaje": "Estado actualizado"}

    def sp_obtener_estado(self, id_vehiculo: int):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_estado", (id_vehiculo,))
                return cursor.fetchone()

    # ------------------ 12 a 13: HISTORIAL ------------------
    def sp_registrar_historial(self, id_vehiculo: int, id_comando, origen: str):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_registrar_historial", (id_vehiculo, id_comando, origen))
                conn.commit()
                return {"mensaje": "Movimiento registrado en historial"}

    def sp_obtener_historial(self, id_vehiculo: int):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_historial", (id_vehiculo,))
                return cursor.fetchall()

    # ------------------ 14 a 17: DEMOS ------------------
    def sp_crear_demo(self, id_vehiculo: int, nombre: str, descripcion: str):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_crear_demo", (id_vehiculo, nombre, descripcion))
                res = cursor.fetchone()
                conn.commit()
                return res

    def sp_obtener_demos(self, id_vehiculo: int):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_demos", (id_vehiculo,))
                return cursor.fetchall()

    def sp_actualizar_demo(self, id_demo: int, nombre: str, descripcion: str, activo: bool):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_actualizar_demo", (id_demo, nombre, descripcion, activo))
                conn.commit()
                return {"mensaje": "Demo actualizada exitosamente"}

    def sp_eliminar_demo(self, id_demo: int):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_eliminar_demo", (id_demo,))
                conn.commit()
                return {"mensaje": "Demo eliminada exitosamente"}

    # ------------------ 18 a 21: MOVIMIENTOS DEMO ------------------
    def sp_agregar_movimiento_demo(self, id_demo: int, id_comando: int, orden: int, duracion_ms: int, pausa_ms: int):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_agregar_movimiento_demo", (id_demo, id_comando, orden, duracion_ms, pausa_ms))
                conn.commit()
                return {"mensaje": "Movimiento agregado a la demo"}

    def sp_obtener_movimientos_demo(self, id_demo: int):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_obtener_movimientos_demo", (id_demo,))
                return cursor.fetchall()

    def sp_actualizar_movimiento_demo(self, id_demo_movimiento: int, id_comando: int, orden: int, duracion_ms: int, pausa_ms: int):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_actualizar_movimiento_demo", (id_demo_movimiento, id_comando, orden, duracion_ms, pausa_ms))
                conn.commit()
                return {"mensaje": "Movimiento de demo actualizado"}

    def sp_eliminar_movimiento_demo(self, id_demo_movimiento: int):
        with DatabaseManager.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.callproc("sp_eliminar_movimiento_demo", (id_demo_movimiento,))
                conn.commit()
                return {"mensaje": "Movimiento de demo eliminado"}