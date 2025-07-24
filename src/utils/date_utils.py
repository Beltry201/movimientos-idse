from datetime import datetime
from typing import Optional
from ..config.constants import FORMATO_FECHA_ENTRADA, FORMATO_FECHA_IDSE, FORMATO_PERIODO


def parsear_fecha(fecha_str: str) -> Optional[datetime]:
    """
    Parsear una fecha en formato YYYY-MM-DD.
    
    Args:
        fecha_str: Fecha en formato string YYYY-MM-DD
        
    Returns:
        Objeto datetime o None si la fecha es inválida
    """
    try:
        return datetime.strptime(fecha_str, FORMATO_FECHA_ENTRADA)
    except ValueError:
        return None


def formatear_fecha_idse(fecha_str: str) -> str:
    """
    Formatear fecha para archivo IDSE (DDMMYYYY).
    
    Args:
        fecha_str: Fecha en formato YYYY-MM-DD
        
    Returns:
        Fecha formateada como DDMMYYYY
        
    Raises:
        ValueError: Si la fecha es inválida
    """
    fecha = parsear_fecha(fecha_str)
    if not fecha:
        raise ValueError(f"Fecha inválida: {fecha_str}")
    
    return fecha.strftime(FORMATO_FECHA_IDSE)


def extraer_periodo(fecha_str: str) -> str:
    """
    Extraer periodo de una fecha (MMYYYY).
    
    Args:
        fecha_str: Fecha en formato YYYY-MM-DD
        
    Returns:
        Periodo en formato MMYYYY
        
    Raises:
        ValueError: Si la fecha es inválida
    """
    fecha = parsear_fecha(fecha_str)
    if not fecha:
        raise ValueError(f"Fecha inválida: {fecha_str}")
    
    return fecha.strftime(FORMATO_PERIODO)


def validar_fecha_futura(fecha_str: str) -> bool:
    """
    Validar que una fecha no sea futura.
    
    Args:
        fecha_str: Fecha en formato YYYY-MM-DD
        
    Returns:
        True si la fecha no es futura, False en caso contrario
    """
    fecha = parsear_fecha(fecha_str)
    if not fecha:
        return False
    
    return fecha <= datetime.now()


def obtener_fecha_actual() -> str:
    """
    Obtener fecha actual en formato YYYY-MM-DD.
    
    Returns:
        Fecha actual formateada
    """
    return datetime.now().strftime(FORMATO_FECHA_ENTRADA)


def validar_rango_fechas(fecha_inicio: str, fecha_fin: str) -> bool:
    """
    Validar que fecha_inicio sea anterior o igual a fecha_fin.
    
    Args:
        fecha_inicio: Fecha de inicio en formato YYYY-MM-DD
        fecha_fin: Fecha de fin en formato YYYY-MM-DD
        
    Returns:
        True si el rango es válido, False en caso contrario
    """
    fecha_inicio_dt = parsear_fecha(fecha_inicio)
    fecha_fin_dt = parsear_fecha(fecha_fin)
    
    if not fecha_inicio_dt or not fecha_fin_dt:
        return False
    
    return fecha_inicio_dt <= fecha_fin_dt 