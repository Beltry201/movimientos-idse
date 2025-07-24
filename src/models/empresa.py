from pydantic import BaseModel, validator
from typing import List
import re
from .movimiento import MovimientoBase, Movimiento


class EmpresaBase(BaseModel):
    """Modelo base para representar una empresa sin validaciones estrictas."""
    
    registro_patronal: str
    nombre: str
    rfc: str
    movimientos: List[MovimientoBase]
    
    class Config:
        """Configuración del modelo."""
        json_schema_extra = {
            "example": {
                "registro_patronal": "B5510768108",
                "nombre": "Tecnología Buk S.A. de C.V.",
                "rfc": "TBU050525AB1",
                "movimientos": [
                    {
                        "tipo": "alta",
                        "empleado": {
                            "nss": "12345678901",
                            "nombre": "Juan Pérez García",
                            "curp": "PEGJ850301HDFRRN01"
                        },
                        "fecha_movimiento": "2024-03-15",
                        "sbc": 1500.0
                    }
                ]
            }
        }


class Empresa(EmpresaBase):
    """Modelo para representar una empresa en el sistema IDSE."""
    
    movimientos: List[Movimiento]  # Usar el modelo con validaciones estrictas
    
    @validator('registro_patronal')
    def validar_registro_patronal(cls, v):
        """Validar que el registro patronal tenga exactamente 11 caracteres alfanuméricos."""
        if not v or len(v) != 11:
            raise ValueError('El registro patronal debe tener exactamente 11 caracteres')
        
        # Validar que contenga solo letras y números
        if not re.match(r'^[A-Za-z0-9]+$', v):
            raise ValueError('El registro patronal debe contener solo caracteres alfanuméricos')
        
        return v.upper()
    
    @validator('nombre')
    def validar_nombre(cls, v):
        """Validar que el nombre no esté vacío."""
        if not v or not v.strip():
            raise ValueError('El nombre de la empresa no puede estar vacío')
        
        # Limpiar espacios extra y normalizar
        return ' '.join(v.strip().split())
    
    @validator('rfc')
    def validar_rfc(cls, v):
        """Validar que el RFC tenga formato válido."""
        if not v or len(v) < 12 or len(v) > 13:
            raise ValueError('El RFC debe tener entre 12 y 13 caracteres')
        
        # Validar formato básico: 3-4 letras + 6 dígitos + 3 caracteres alfanuméricos
        rfc_pattern = r'^[A-Z]{3,4}\d{6}[A-Z0-9]{3}$'
        if not re.match(rfc_pattern, v.upper()):
            raise ValueError('El RFC no tiene el formato válido')
        
        return v.upper()
    
    @validator('movimientos')
    def validar_movimientos(cls, v):
        """Validar que haya al menos un movimiento."""
        if not v:
            raise ValueError('La empresa debe tener al menos un movimiento')
        
        return v
    
    class Config:
        """Configuración del modelo."""
        json_schema_extra = {
            "example": {
                "registro_patronal": "B5510768108",
                "nombre": "Tecnología Buk S.A. de C.V.",
                "rfc": "TBU050525AB1",
                "movimientos": [
                    {
                        "tipo": "alta",
                        "empleado": {
                            "nss": "12345678901",
                            "nombre": "Juan Pérez García",
                            "curp": "PEGJ850301HDFRRN01"
                        },
                        "fecha_movimiento": "2024-03-15",
                        "sbc": 1500.0
                    }
                ]
            }
        } 