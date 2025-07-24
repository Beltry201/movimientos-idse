from typing import List, Dict, Any
from collections import defaultdict
from loguru import logger
from ..models import Movimiento, MovimientoValidado, Empresa, EmpresaBase
from ..utils.date_utils import extraer_periodo
from ..config.constants import SBC_MAXIMO


class ValidationRules:
    """Reglas de validación para el sistema IDSE."""
    
    @staticmethod
    def get_limite_movimientos() -> int:
        """Obtener el límite de movimientos por empresa."""
        from ..config.settings import settings
        return settings.max_movimientos_por_empresa
    
    @staticmethod
    def get_sbc_maximo() -> float:
        """Obtener el SBC máximo permitido."""
        return SBC_MAXIMO
    
    @staticmethod
    def validar_unicidad_movimientos(movimientos: List[MovimientoValidado]) -> List[MovimientoValidado]:
        """
        Validar reglas de unicidad por empleado y periodo.
        
        Args:
            movimientos: Lista de movimientos validados
            
        Returns:
            Lista de movimientos con validaciones de unicidad aplicadas
        """
        # Agrupar por empleado y periodo
        grupos = defaultdict(list)
        
        for movimiento in movimientos:
            clave = f"{movimiento.empleado.nss}-{movimiento.periodo}"
            grupos[clave].append(movimiento)
        
        movimientos_finales = []
        
        for clave, movimientos_grupo in grupos.items():
            # Separar por tipo de movimiento
            altas = [m for m in movimientos_grupo if m.tipo == "alta"]
            bajas = [m for m in movimientos_grupo if m.tipo == "baja"]
            modificaciones = [m for m in movimientos_grupo if m.tipo == "modificacion"]
            
            # Validar altas (máximo 1 por empleado/periodo)
            if len(altas) > 1:
                logger.warning(f"Múltiples altas para empleado {altas[0].empleado.nss} en periodo {altas[0].periodo}")
                # Marcar como inválidas todas excepto la primera
                for alta in altas[1:]:
                    alta.es_valido = False
                    alta.errores.append("Solo se permite una alta por empleado por periodo")
            
            # Validar bajas (máximo 1 por empleado/periodo)
            if len(bajas) > 1:
                logger.warning(f"Múltiples bajas para empleado {bajas[0].empleado.nss} en periodo {bajas[0].periodo}")
                # Marcar como inválidas todas excepto la primera
                for baja in bajas[1:]:
                    baja.es_valido = False
                    baja.errores.append("Solo se permite una baja por empleado por periodo")
            
            # Validar modificaciones (múltiples permitidas si SBC diferente)
            modificaciones_validas = ValidationRules._filtrar_modificaciones_unicas(modificaciones)
            
            # Agregar todos los movimientos válidos
            movimientos_finales.extend(altas)
            movimientos_finales.extend(bajas)
            movimientos_finales.extend(modificaciones_validas)
        
        return movimientos_finales
    
    @staticmethod
    def _filtrar_modificaciones_unicas(modificaciones: List[MovimientoValidado]) -> List[MovimientoValidado]:
        """
        Filtrar modificaciones para mantener solo aquellas con SBC único.
        
        Args:
            modificaciones: Lista de modificaciones
            
        Returns:
            Lista de modificaciones con SBC único
        """
        if not modificaciones:
            return []
        
        # Agrupar por SBC
        sbc_grupos = defaultdict(list)
        for modificacion in modificaciones:
            sbc_key = str(modificacion.sbc) if modificacion.sbc else "None"
            sbc_grupos[sbc_key].append(modificacion)
        
        modificaciones_unicas = []
        
        for sbc, mods in sbc_grupos.items():
            if len(mods) > 1:
                logger.warning(f"Múltiples modificaciones con mismo SBC {sbc} para empleado {mods[0].empleado.nss}")
                # Marcar como inválidas todas excepto la primera
                for mod in mods[1:]:
                    mod.es_valido = False
                    mod.errores.append("Modificaciones con mismo SBC no permitidas")
            
            modificaciones_unicas.append(mods[0])
        
        return modificaciones_unicas
    
    @staticmethod
    def validar_estructura_json(data: Dict[str, Any]) -> bool:
        """
        Validar estructura básica del JSON de entrada.
        
        Args:
            data: Datos JSON a validar
            
        Returns:
            True si la estructura es válida, False en caso contrario
        """
        if not isinstance(data, dict):
            return False
        
        if "empresa" not in data:
            return False
        
        if not isinstance(data["empresa"], list):
            return False
        
        return True
    
    @staticmethod
    def validar_limites_empresas(empresas: List[Empresa]) -> bool:
        """
        Validar límites de empresas por request.
        
        Args:
            empresas: Lista de empresas
            
        Returns:
            True si está dentro de los límites, False en caso contrario
        """
        from ..config.settings import settings
        
        if len(empresas) > settings.max_empresas_por_request:
            logger.warning(f"Demasiadas empresas en request: {len(empresas)}")
            return False
        
        return True
    
    @staticmethod
    def validar_limites_movimientos(empresa: EmpresaBase) -> bool:
        """
        Validar límites de movimientos por empresa.
        
        Args:
            empresa: Empresa a validar
            
        Returns:
            True si está dentro de los límites, False en caso contrario
        """
        from ..config.settings import settings
        
        if len(empresa.movimientos) > settings.max_movimientos_por_empresa:
            logger.warning(f"Demasiados movimientos para empresa {empresa.registro_patronal}: {len(empresa.movimientos)}")
            return False
        
        return True
    
    @staticmethod
    def validar_sbc_limite(sbc: float) -> bool:
        """
        Validar que el SBC no exceda el límite máximo.
        
        Args:
            sbc: Valor del SBC
            
        Returns:
            True si el SBC es válido, False en caso contrario
        """
        return sbc <= SBC_MAXIMO
    
    @staticmethod
    def validar_fecha_no_futura(fecha_str: str) -> bool:
        """
        Validar que la fecha no sea futura.
        
        Args:
            fecha_str: Fecha en formato YYYY-MM-DD
            
        Returns:
            True si la fecha no es futura, False en caso contrario
        """
        from ..utils.date_utils import validar_fecha_futura
        return validar_fecha_futura(fecha_str) 