import re
from typing import Optional
from ..config.constants import LINEA_IDSE_LONGITUD


def pad_left(texto: str, longitud: int, caracter: str = "0") -> str:
    """
    Rellenar texto a la izquierda hasta alcanzar la longitud especificada.
    
    Args:
        texto: Texto a rellenar
        longitud: Longitud deseada
        caracter: Caracter de relleno
        
    Returns:
        Texto rellenado
    """
    return str(texto).rjust(longitud, caracter)


def pad_right(texto: str, longitud: int, caracter: str = " ") -> str:
    """
    Rellenar texto a la derecha hasta alcanzar la longitud especificada.
    
    Args:
        texto: Texto a rellenar
        longitud: Longitud deseada
        caracter: Caracter de relleno
        
    Returns:
        Texto rellenado
    """
    return str(texto).ljust(longitud, caracter)


def es_numerico(texto: str) -> bool:
    """
    Verificar si un texto contiene solo dígitos numéricos.
    
    Args:
        texto: Texto a verificar
        
    Returns:
        True si el texto es numérico, False en caso contrario
    """
    return bool(re.match(r'^\d+$', str(texto)))


def es_alfanumerico(texto: str) -> bool:
    """
    Verificar si un texto contiene solo caracteres alfanuméricos.
    
    Args:
        texto: Texto a verificar
        
    Returns:
        True si el texto es alfanumérico, False en caso contrario
    """
    return bool(re.match(r'^[A-Za-z0-9]+$', str(texto)))


def formatear_sbc_idse(sbc: Optional[float]) -> str:
    """
    Formatear SBC para archivo IDSE (sin decimales, pad con ceros).
    
    Args:
        sbc: Valor del SBC
        
    Returns:
        SBC formateado como string de 10 dígitos
    """
    if sbc is None:
        return "0" * 10
    
    # Convertir a centavos (multiplicar por 100) y formatear
    centavos = int(sbc * 100)
    return pad_left(str(centavos), 10, "0")


def validar_longitud_linea_idse(linea: str) -> bool:
    """
    Validar que una línea IDSE tenga exactamente 44 caracteres.
    
    Args:
        linea: Línea a validar
        
    Returns:
        True si la línea tiene la longitud correcta, False en caso contrario
    """
    return len(linea) == LINEA_IDSE_LONGITUD


def limpiar_texto(texto: str) -> str:
    """
    Limpiar texto eliminando espacios extra y normalizando.
    
    Args:
        texto: Texto a limpiar
        
    Returns:
        Texto limpio
    """
    if not texto:
        return ""
    
    # Eliminar espacios extra y normalizar
    return " ".join(texto.strip().split())


def normalizar_texto(texto: str, longitud_maxima: Optional[int] = None) -> str:
    """
    Normalizar texto para uso en archivos IDSE.
    
    Args:
        texto: Texto a normalizar
        longitud_maxima: Longitud máxima permitida
        
    Returns:
        Texto normalizado
    """
    texto_limpio = limpiar_texto(texto)
    
    if longitud_maxima and len(texto_limpio) > longitud_maxima:
        texto_limpio = texto_limpio[:longitud_maxima]
    
    return texto_limpio


def generar_nombre_archivo(tipo: str, periodo: str, registro_patronal: str) -> str:
    """
    Generar nombre de archivo IDSE según el formato especificado.
    
    Args:
        tipo: Tipo de movimiento (alta, baja, modificacion)
        periodo: Periodo en formato MMYYYY
        registro_patronal: Registro patronal de la empresa
        
    Returns:
        Nombre del archivo
    """
    from ..config.constants import PREFIJO_ARCHIVO_IDSE, SEPARADOR_ARCHIVO, EXTENSION_ARCHIVO
    
    # Mapear tipo a código
    tipo_codigo = {
        "alta": "ALT",
        "baja": "BAJ", 
        "modificacion": "MOD"
    }.get(tipo, "MOV")
    
    return f"{PREFIJO_ARCHIVO_IDSE}{SEPARADOR_ARCHIVO}{tipo_codigo}{SEPARADOR_ARCHIVO}{periodo}{SEPARADOR_ARCHIVO}{registro_patronal}{EXTENSION_ARCHIVO}" 