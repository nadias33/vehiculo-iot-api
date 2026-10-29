from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from typing import Dict, List

class VehicleWebSocketManager:
    """Gestiona conexiones WebSocket segregadas por vehículo."""
    def __init__(self):
        self.canales: Dict[int, List[WebSocket]] = {}

    async def conectar(self, id_vehiculo: int, websocket: WebSocket):
        await websocket.accept()
        if id_vehiculo not in self.canales:
            self.canales[id_vehiculo] = []
        self.canales[id_vehiculo].append(websocket)

    def desconectar(self, id_vehiculo: int, websocket: WebSocket):
        if id_vehiculo in self.canales:
            if websocket in self.canales[id_vehiculo]:
                self.canales[id_vehiculo].remove(websocket)
            if len(self.canales[id_vehiculo]) == 0:
                del self.canales[id_vehiculo]

    async def emitir_a_vehiculo(self, id_vehiculo: int, mensaje: dict):
        if id_vehiculo not in self.canales:
            return
        
        # Convierte cualquier objeto o fecha a JSON seguro
        mensaje_seguro = jsonable_encoder(mensaje)
        desconectados = []
        for socket in self.canales[id_vehiculo]:
            try:
                await socket.send_json(mensaje_seguro)
            except Exception:
                desconectados.append(socket)
        for caido in desconectados:
            self.desconectar(id_vehiculo, caido)

ws_manager = VehicleWebSocketManager()