from enum import Enum
from typing import Dict


class TipoMovimiento(str, Enum):
    """Tipos de movimiento válidos en el sistema IDSE."""
    ALTA = "alta"
    BAJA = "baja"
    MODIFICACION = "modificacion"


class CodigoTipoMovimiento(str, Enum):
    """Códigos de tipo de movimiento para archivos IDSE."""
    ALTA = "07"
    MODIFICACION = "08"
    BAJA = "09"


class MotivoBaja(str, Enum):
    """Motivos de baja válidos."""
    RENUNCIA = "renuncia"
    DESPIDO = "despido"
    TERMINO_CONTRATO = "termino_contrato"
    INVALIDEZ = "invalidez"
    MUERTE = "muerte"


class CodigoMotivoBaja(str, Enum):
    """Códigos de motivo de baja para archivos IDSE."""
    RENUNCIA = "01"
    DESPIDO = "02"
    TERMINO_CONTRATO = "03"
    INVALIDEZ = "04"
    MUERTE = "05"


# Constantes de validación
SBC_MAXIMO = 2089.12
NSS_LONGITUD = 11
CURP_LONGITUD = 18
REGISTRO_PATRONAL_LONGITUD = 11
LINEA_IDSE_LONGITUD = 44

# Mapeos
TIPO_MOVIMIENTO_A_CODIGO = {
    TipoMovimiento.ALTA: CodigoTipoMovimiento.ALTA,
    TipoMovimiento.MODIFICACION: CodigoTipoMovimiento.MODIFICACION,
    TipoMovimiento.BAJA: CodigoTipoMovimiento.BAJA,
}

MOTIVO_BAJA_A_CODIGO = {
    MotivoBaja.RENUNCIA: CodigoMotivoBaja.RENUNCIA,
    MotivoBaja.DESPIDO: CodigoMotivoBaja.DESPIDO,
    MotivoBaja.TERMINO_CONTRATO: CodigoMotivoBaja.TERMINO_CONTRATO,
    MotivoBaja.INVALIDEZ: CodigoMotivoBaja.INVALIDEZ,
    MotivoBaja.MUERTE: CodigoMotivoBaja.MUERTE,
}

# Configuración de archivos
PREFIJO_ARCHIVO_IDSE = "IDSE"
SEPARADOR_ARCHIVO = "_"
EXTENSION_ARCHIVO = ".txt"

# Formatos de fecha
FORMATO_FECHA_ENTRADA = "%Y-%m-%d"
FORMATO_FECHA_IDSE = "%d%m%Y"
FORMATO_PERIODO = "%m%Y" 