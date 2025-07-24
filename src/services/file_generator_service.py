from typing import List, Dict, Any
from collections import defaultdict
from loguru import logger
import os
from ..models import MovimientoValidado
from ..utils.date_utils import formatear_fecha_idse
from ..utils.format_utils import (
    pad_left, pad_right, formatear_sbc_idse, 
    validar_longitud_linea_idse, generar_nombre_archivo
)
from ..config.constants import (
    TIPO_MOVIMIENTO_A_CODIGO, MOTIVO_BAJA_A_CODIGO,
    CodigoMotivoBaja, LINEA_IDSE_LONGITUD
)
from ..config.settings import settings


class FileGeneratorService:
    """Servicio para generar archivos IDSE con formato específico."""
    
    def generar_archivos_idse(self, movimientos: List[MovimientoValidado]) -> List[Dict[str, Any]]:
        """
        Generar archivos IDSE agrupados por tipo, periodo y registro patronal.
        
        Args:
            movimientos: Lista de movimientos válidos
            
        Returns:
            Lista de archivos generados
        """
        if not movimientos:
            return []
        
        # Agrupar movimientos por tipo, periodo y registro patronal
        grupos = self._agrupar_movimientos(movimientos)
        
        archivos = []
        
        # Asegurar que el directorio output existe
        os.makedirs(settings.output_dir, exist_ok=True)
        
        for clave, movimientos_grupo in grupos.items():
            try:
                archivo = self._generar_archivo_grupo(clave, movimientos_grupo)
                
                # Escribir archivo físicamente al disco
                ruta_archivo = os.path.join(settings.output_dir, archivo['nombre'])
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(archivo['contenido'])
                
                # Agregar ruta del archivo al diccionario
                archivo['ruta'] = ruta_archivo
                
                archivos.append(archivo)
                logger.info(f"Archivo generado: {archivo['nombre']} con {len(movimientos_grupo)} movimientos")
            except Exception as e:
                logger.error(f"Error generando archivo para grupo {clave}: {e}")
        
        return archivos
    
    def _agrupar_movimientos(self, movimientos: List[MovimientoValidado]) -> Dict[str, List[MovimientoValidado]]:
        """
        Agrupar movimientos por tipo, periodo y registro patronal.
        
        Args:
            movimientos: Lista de movimientos válidos
            
        Returns:
            Diccionario con movimientos agrupados
        """
        grupos = defaultdict(list)
        
        for movimiento in movimientos:
            # Clave: tipo-periodo-registro_patronal
            clave = f"{movimiento.tipo}-{movimiento.periodo}-{movimiento.registro_patronal}"
            grupos[clave].append(movimiento)
        
        return dict(grupos)
    
    def _generar_archivo_grupo(self, clave: str, movimientos: List[MovimientoValidado]) -> Dict[str, Any]:
        """
        Generar archivo IDSE para un grupo de movimientos.
        
        Args:
            clave: Clave del grupo (tipo-periodo-registro_patronal)
            movimientos: Movimientos del grupo
            
        Returns:
            Diccionario con información del archivo generado
        """
        # Parsear clave
        tipo, periodo, registro_patronal = clave.split("-")
        
        # Generar nombre del archivo
        nombre_archivo = generar_nombre_archivo(tipo, periodo, registro_patronal)
        
        # Generar líneas del archivo
        lineas = []
        for movimiento in movimientos:
            linea = self._generar_linea_idse(movimiento)
            lineas.append(linea)
        
        # Unir líneas
        contenido = "\n".join(lineas)
        
        return {
            "nombre": nombre_archivo,
            "contenido": contenido,
            "tipo": tipo,
            "periodo": periodo,
            "registro_patronal": registro_patronal,
            "cantidad_movimientos": len(movimientos),
            "tamaño_bytes": len(contenido.encode('utf-8'))
        }
    
    def _generar_linea_idse(self, movimiento: MovimientoValidado) -> str:
        """
        Generar línea IDSE con formato exacto de 44 caracteres.
        
        Args:
            movimiento: Movimiento validado
            
        Returns:
            Línea formateada para archivo IDSE
            
        Raises:
            ValueError: Si la línea generada no tiene 44 caracteres
        """
        # Posiciones 1-11: Registro Patronal
        registro_patronal = pad_right(movimiento.registro_patronal, 11)
        
        # Posiciones 12-22: NSS del empleado
        nss = pad_right(movimiento.empleado.nss, 11)
        
        # Posiciones 23-24: Tipo de movimiento
        tipo_codigo = TIPO_MOVIMIENTO_A_CODIGO.get(movimiento.tipo, "00")
        
        # Posiciones 25-26: Razón de salida
        if movimiento.tipo == "baja":
            razon_salida = MOTIVO_BAJA_A_CODIGO.get(movimiento.motivo, "00")
        else:
            razon_salida = "00"
        
        # Posiciones 27-34: Fecha (DDMMYYYY)
        fecha = formatear_fecha_idse(movimiento.fecha_movimiento)
        
        # Posiciones 35-44: SBC (sin decimales, pad con ceros)
        sbc = formatear_sbc_idse(movimiento.sbc)
        
        # Construir línea completa
        linea = registro_patronal + nss + tipo_codigo + razon_salida + fecha + sbc
        
        # Validar longitud exacta
        if not validar_longitud_linea_idse(linea):
            raise ValueError(f"Línea IDSE debe tener exactamente {LINEA_IDSE_LONGITUD} caracteres, tiene {len(linea)}")
        
        return linea
    
    def validar_archivo_generado(self, contenido: str) -> bool:
        """
        Validar que un archivo generado tenga el formato correcto.
        
        Args:
            contenido: Contenido del archivo
            
        Returns:
            True si el archivo es válido, False en caso contrario
        """
        if not contenido:
            return False
        
        lineas = contenido.strip().split('\n')
        
        for i, linea in enumerate(lineas):
            if not linea.strip():
                continue
            
            # Validar longitud de cada línea
            if not validar_longitud_linea_idse(linea):
                logger.error(f"Línea {i+1} tiene longitud incorrecta: {len(linea)} caracteres")
                return False
            
            # Validar formato básico (solo caracteres alfanuméricos)
            if not linea.isalnum():
                logger.error(f"Línea {i+1} contiene caracteres no alfanuméricos")
                return False
        
        return True
    
    def obtener_estadisticas_archivos(self, archivos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Obtener estadísticas de los archivos generados.
        
        Args:
            archivos: Lista de archivos generados
            
        Returns:
            Estadísticas de archivos
        """
        if not archivos:
            return {
                "total_archivos": 0,
                "total_movimientos": 0,
                "tamaño_total_bytes": 0,
                "por_tipo": {},
                "por_periodo": {}
            }
        
        total_movimientos = sum(archivo["cantidad_movimientos"] for archivo in archivos)
        tamaño_total = sum(archivo["tamaño_bytes"] for archivo in archivos)
        
        # Estadísticas por tipo
        por_tipo = defaultdict(int)
        for archivo in archivos:
            por_tipo[archivo["tipo"]] += archivo["cantidad_movimientos"]
        
        # Estadísticas por periodo
        por_periodo = defaultdict(int)
        for archivo in archivos:
            por_periodo[archivo["periodo"]] += archivo["cantidad_movimientos"]
        
        return {
            "total_archivos": len(archivos),
            "total_movimientos": total_movimientos,
            "tamaño_total_bytes": tamaño_total,
            "por_tipo": dict(por_tipo),
            "por_periodo": dict(por_periodo)
        } 