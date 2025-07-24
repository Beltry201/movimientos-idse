from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación IDSE."""
    
    # Configuración de la aplicación
    app_name: str = "Sistema IDSE - IMSS"
    app_version: str = "1.0.0"
    app_description: str = "Sistema de Procesamiento de Movimientos IDSE para el IMSS"
    
    
    # Configuración de logging
    log_level: str = "INFO"
    log_format: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # Configuración de archivos
    output_dir: str = "output"
    max_file_size_mb: int = 10
    
    # Configuración de validación
    max_movimientos_por_empresa: int = 1000
    max_empresas_por_request: int = 100
    
    class Config:
        case_sensitive = False


# Instancia global de configuración
settings = Settings() 