from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from .empleado import EmpleadoBase, Empleado


class MovimientoBase(BaseModel):
    """Modelo base para representar un movimiento de empleado sin validaciones estrictas."""
    
    tipo: str
    empleado: EmpleadoBase
    fecha_movimiento: str
    sbc: Optional[float] = None
    motivo: Optional[str] = None
    
    class Config:
        """Configuración del modelo."""
        json_schema_extra = {
            "example": {
                "tipo": "alta",
                "empleado": {
                    "nss": "12345678901",
                    "nombre": "Juan Pérez García",
                    "curp": "PEGJ850301HDFRRN01"
                },
                "fecha_movimiento": "2024-03-15",
                "sbc": 1500.0
            }
        }


class Movimiento(MovimientoBase):
    """Modelo para representar un movimiento de empleado en el sistema IDSE."""
    
    empleado: Empleado  # Usar el modelo con validaciones estrictas
    
    @validator('tipo')
    def validar_tipo(cls, v):
        """Validar que el tipo de movimiento sea válido."""
        tipos_validos = ['alta', 'baja', 'modificacion']
        if v not in tipos_validos:
            raise ValueError(f'El tipo de movimiento debe ser uno de: {tipos_validos}')
        return v
    
    @validator('fecha_movimiento')
    def validar_fecha(cls, v):
        """Validar que la fecha tenga formato YYYY-MM-DD y sea válida."""
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('La fecha debe tener formato YYYY-MM-DD')
        return v
    
    @validator('sbc')
    def validar_sbc(cls, v, values):
        """Validar el SBC según el tipo de movimiento."""
        tipo = values.get('tipo')
        
        if tipo == 'baja':
            if v is not None:
                raise ValueError('Las bajas no deben incluir SBC')
        else:
            if v is None or v <= 0:
                raise ValueError('El SBC debe ser mayor a 0 para altas y modificaciones')
            
            # SBC máximo según reglas IMSS
            if v > 2089.12:
                raise ValueError('El SBC no puede exceder $2,089.12')
        
        return v
    
    @validator('motivo')
    def validar_motivo(cls, v, values):
        """Validar el motivo solo para bajas."""
        tipo = values.get('tipo')
        
        if tipo == 'baja':
            if not v:
                raise ValueError('El motivo es obligatorio para bajas')
            
            motivos_validos = ['renuncia', 'despido', 'termino_contrato', 'invalidez', 'muerte']
            if v not in motivos_validos:
                raise ValueError(f'El motivo debe ser uno de: {motivos_validos}')
        else:
            if v:
                raise ValueError('El motivo solo se permite para bajas')
        
        return v
    
    class Config:
        """Configuración del modelo."""
        json_schema_extra = {
            "example": {
                "tipo": "alta",
                "empleado": {
                    "nss": "12345678901",
                    "nombre": "Juan Pérez García",
                    "curp": "PEGJ850301HDFRRN01"
                },
                "fecha_movimiento": "2024-03-15",
                "sbc": 1500.0
            }
        }


class MovimientoValidado(MovimientoBase):
    """Modelo para representar un movimiento validado con información adicional."""
    
    es_valido: bool
    errores: List[str]
    periodo: str  # MMYYYY
    registro_patronal: str
    
    class Config:
        """Configuración del modelo."""
        json_schema_extra = {
            "example": {
                "tipo": "alta",
                "empleado": {
                    "nss": "12345678901",
                    "nombre": "Juan Pérez García",
                    "curp": "PEGJ850301HDFRRN01"
                },
                "fecha_movimiento": "2024-03-15",
                "sbc": 1500.0,
                "es_valido": True,
                "errores": [],
                "periodo": "032024",
                "registro_patronal": "B5510768108"
            }
        } 