from pydantic import BaseModel, validator
from typing import Optional
import re


class EmpleadoBase(BaseModel):
    """Modelo base para representar un empleado sin validaciones estrictas."""
    
    nss: str
    nombre: str
    curp: Optional[str] = None
    
    class Config:
        """Configuración del modelo."""
        json_schema_extra = {
            "example": {
                "nss": "12345678901",
                "nombre": "Juan Pérez García",
                "curp": "PEGJ850301HDFRRN01"
            }
        }


class Empleado(EmpleadoBase):
    """Modelo para representar un empleado en el sistema IDSE."""
    
    @validator('nss')
    def validar_nss(cls, v):
        """Validar que el NSS tenga exactamente 11 dígitos numéricos."""
        if not v or len(v) != 11:
            raise ValueError('El NSS debe tener exactamente 11 dígitos')
        
        if not v.isdigit():
            raise ValueError('El NSS debe contener solo dígitos numéricos')
        
        return v
    
    @validator('nombre')
    def validar_nombre(cls, v):
        """Validar que el nombre no esté vacío."""
        if not v or not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        
        # Limpiar espacios extra y normalizar
        return ' '.join(v.strip().split())
    
    @validator('curp')
    def validar_curp(cls, v):
        """Validar que el CURP tenga exactamente 18 caracteres alfanuméricos."""
        if v is None:
            return v
        
        if len(v) != 18:
            raise ValueError('El CURP debe tener exactamente 18 caracteres')
        
        # Validar que contenga solo caracteres alfanuméricos
        if not re.match(r'^[A-Za-z0-9]+$', v):
            raise ValueError('El CURP debe contener solo caracteres alfanuméricos')
        
        return v.upper()
    
    class Config:
        """Configuración del modelo."""
        json_schema_extra = {
            "example": {
                "nss": "12345678901",
                "nombre": "Juan Pérez García",
                "curp": "PEGJ850301HDFRRN01"
            }
        } 