from pydantic import BaseModel, Field
from typing import Optional

# Vehículos
class VehiculoCrear(BaseModel):
    nombre: str = Field(..., max_length=80)
    modelo: Optional[str] = Field(None, max_length=80)
    descripcion: Optional[str] = Field(None, max_length=255)
    microcontrolador: Optional[str] = Field(None, max_length=50)

class VehiculoActualizar(BaseModel):
    nombre: str = Field(..., max_length=80)
    modelo: Optional[str] = Field(None, max_length=80)
    descripcion: Optional[str] = Field(None, max_length=255)
    microcontrolador: Optional[str] = Field(None, max_length=50)
    activo: bool

# Comandos
class ComandoCrear(BaseModel):
    id_vehiculo: int
    nombre: str = Field(..., max_length=60)
    codigo: int
    descripcion: Optional[str] = Field(None, max_length=255)

class ComandoActualizar(BaseModel):
    nombre: str = Field(..., max_length=60)
    codigo: int
    descripcion: Optional[str] = Field(None, max_length=255)
    activo: bool

# Estado e Historial
class EstadoActualizar(BaseModel):
    id_comando: Optional[int]
    conectado: bool

class HistorialRegistrar(BaseModel):
    id_comando: Optional[int]
    origen: str = Field("MANUAL", max_length=30)

# Movimiento individual (Endpoint clave de la práctica)
class MovimientoIndividual(BaseModel):
    id_comando: int
    origen: str = Field("THUNDER_CLIENT", max_length=30)

# Demos
class DemoCrear(BaseModel):
    id_vehiculo: int
    nombre: str = Field(..., max_length=80)
    descripcion: Optional[str] = Field(None, max_length=255)

class DemoActualizar(BaseModel):
    nombre: str = Field(..., max_length=80)
    descripcion: Optional[str] = Field(None, max_length=255)
    activo: bool

# Movimientos de Demo
class DemoMovimientoCrear(BaseModel):
    id_comando: int
    orden: int
    duracion_ms: int
    pausa_ms: int = 0

class DemoMovimientoActualizar(BaseModel):
    id_comando: int
    orden: int
    duracion_ms: int
    pausa_ms: int = 0