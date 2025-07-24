from typing import List, Dict, Any, Tuple
from loguru import logger
from ..models import Movimiento, MovimientoValidado, Empresa, EmpresaBase, MovimientoBase
from ..utils.date_utils import extraer_periodo
from .validation_rules import ValidationRules


class MovimientoValidator:
    """Validador principal para movimientos IDSE."""
    
    @staticmethod
    def validar_movimientos(data: Dict[str, Any]) -> Tuple[List[MovimientoValidado], List[Dict[str, Any]]]:
        """
        Validar todos los movimientos en el JSON de entrada.
        
        Args:
            data: Datos JSON con empresas y movimientos
            
        Returns:
            Tuple con (movimientos_validados, errores_detallados)
        """
        movimientos_validados = []
        errores_detallados = []
        
        # Validar estructura básica del JSON
        if not ValidationRules.validar_estructura_json(data):
            raise ValueError("Estructura JSON inválida. Se requiere campo 'empresa' con lista de empresas")
        
        # Parsear empresas usando el modelo base (sin validaciones estrictas)
        empresas_data = data["empresa"]
        
        for empresa_idx, empresa_data in enumerate(empresas_data):
            try:
                empresa = EmpresaBase(**empresa_data)
            except Exception as e:
                # Si la empresa no se puede parsear, registrar error y continuar
                error_info = {
                    "tipo": "empresa_invalida",
                    "empresa_idx": empresa_idx,
                    "registro_patronal": empresa_data.get("registro_patronal", "DESCONOCIDO"),
                    "error": str(e),
                    "datos": empresa_data
                }
                errores_detallados.append(error_info)
                logger.error(f"Empresa {empresa_idx} inválida: {e}")
                continue
            
            # Validar límites de movimientos por empresa
            if not ValidationRules.validar_limites_movimientos(empresa):
                error_info = {
                    "tipo": "limite_movimientos_excedido",
                    "empresa": empresa.registro_patronal,
                    "movimientos_count": len(empresa.movimientos),
                    "limite": ValidationRules.get_limite_movimientos()
                }
                errores_detallados.append(error_info)
                logger.warning(f"Demasiados movimientos para empresa {empresa.registro_patronal}")
                continue
            
            # Validar cada movimiento individualmente
            for mov_idx, movimiento in enumerate(empresa.movimientos):
                movimiento_validado, errores_mov = MovimientoValidator._validar_movimiento_individual(
                    movimiento, empresa, mov_idx
                )
                movimientos_validados.append(movimiento_validado)
                
                # Agregar errores del movimiento a la lista detallada
                if errores_mov:
                    for error in errores_mov:
                        errores_detallados.append(error)
        
        # Aplicar reglas de unicidad
        movimientos_finales = ValidationRules.validar_unicidad_movimientos(movimientos_validados)
        
        return movimientos_finales, errores_detallados
    
    @staticmethod
    def _validar_movimiento_individual(movimiento: MovimientoBase, empresa: EmpresaBase, mov_idx: int) -> Tuple[MovimientoValidado, List[Dict[str, Any]]]:
        """
        Validar un movimiento individual.
        
        Args:
            movimiento: Movimiento a validar
            empresa: Empresa a la que pertenece el movimiento
            mov_idx: Índice del movimiento en la empresa
            
        Returns:
            Tuple con (movimiento_validado, errores_detallados)
        """
        errores_detallados = []
        errores_generales = []
        
        try:
            # Extraer periodo para validaciones (manejar fechas inválidas)
            try:
                periodo = extraer_periodo(movimiento.fecha_movimiento)
            except ValueError:
                periodo = "000000"  # Periodo por defecto para fechas inválidas
            
            # Crear movimiento validado
            movimiento_validado = MovimientoValidado(
                **movimiento.dict(),
                es_valido=True,
                errores=[],
                periodo=periodo,
                registro_patronal=empresa.registro_patronal
            )
            
            # Validaciones básicas del empleado
            errores_empleado = MovimientoValidator._validar_empleado(movimiento.empleado, empresa, mov_idx)
            errores_detallados.extend(errores_empleado)
            
            # Validaciones de fecha
            errores_fecha = MovimientoValidator._validar_fecha(movimiento.fecha_movimiento, empresa, mov_idx)
            errores_detallados.extend(errores_fecha)
            
            # Validaciones de SBC
            errores_sbc = MovimientoValidator._validar_sbc(movimiento, empresa, mov_idx)
            errores_detallados.extend(errores_sbc)
            
            # Validaciones de tipo y motivo
            errores_tipo = MovimientoValidator._validar_tipo_motivo(movimiento, empresa, mov_idx)
            errores_detallados.extend(errores_tipo)
            
            # Actualizar estado de validación
            movimiento_validado.es_valido = len(errores_detallados) == 0
            movimiento_validado.errores = [error["mensaje"] for error in errores_detallados]
            
            return movimiento_validado, errores_detallados
            
        except Exception as e:
            logger.error(f"Error validando movimiento {mov_idx} de empresa {empresa.registro_patronal}: {e}")
            error_info = {
                "tipo": "error_validacion",
                "empresa": empresa.registro_patronal,
                "movimiento_idx": mov_idx,
                "error": str(e),
                "datos_movimiento": movimiento.dict() if hasattr(movimiento, 'dict') else str(movimiento)
            }
            errores_detallados.append(error_info)
            
            # Intentar extraer periodo de forma segura
            try:
                periodo_error = extraer_periodo(movimiento.fecha_movimiento) if hasattr(movimiento, 'fecha_movimiento') else "000000"
            except ValueError:
                periodo_error = "000000"
            
            return MovimientoValidado(
                **movimiento.dict(),
                es_valido=False,
                errores=[f"Error de validación: {str(e)}"],
                periodo=periodo_error,
                registro_patronal=empresa.registro_patronal
            ), errores_detallados
    
    @staticmethod
    def _validar_empleado(empleado, empresa: EmpresaBase, mov_idx: int) -> List[Dict[str, Any]]:
        """Validar datos del empleado."""
        errores = []
        
        # Validar NSS
        if not empleado.nss or len(str(empleado.nss)) != 11:
            errores.append({
                "tipo": "nss_invalido",
                "empresa": empresa.registro_patronal,
                "movimiento_idx": mov_idx,
                "campo": "empleado.nss",
                "valor": empleado.nss,
                "mensaje": f"El NSS debe tener exactamente 11 dígitos (actual: {len(str(empleado.nss)) if empleado.nss else 0})"
            })
        
        # Validar CURP si está presente
        if hasattr(empleado, 'curp') and empleado.curp:
            if len(empleado.curp) != 18:
                errores.append({
                    "tipo": "curp_invalido",
                    "empresa": empresa.registro_patronal,
                    "movimiento_idx": mov_idx,
                    "campo": "empleado.curp",
                    "valor": empleado.curp,
                    "mensaje": f"El CURP debe tener exactamente 18 caracteres (actual: {len(empleado.curp)})"
                })
        
        return errores
    
    @staticmethod
    def _validar_fecha(fecha_str: str, empresa: EmpresaBase, mov_idx: int) -> List[Dict[str, Any]]:
        """Validar fecha de movimiento."""
        errores = []
        
        try:
            from datetime import datetime
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            
            # Validar que no sea fecha futura
            if fecha > datetime.now():
                errores.append({
                    "tipo": "fecha_futura",
                    "empresa": empresa.registro_patronal,
                    "movimiento_idx": mov_idx,
                    "campo": "fecha_movimiento",
                    "valor": fecha_str,
                    "mensaje": "La fecha de movimiento no puede ser futura"
                })
                
        except ValueError:
            errores.append({
                "tipo": "fecha_invalida",
                "empresa": empresa.registro_patronal,
                "movimiento_idx": mov_idx,
                "campo": "fecha_movimiento",
                "valor": fecha_str,
                "mensaje": "La fecha debe tener formato YYYY-MM-DD"
            })
        
        return errores
    
    @staticmethod
    def _validar_sbc(movimiento: MovimientoBase, empresa: EmpresaBase, mov_idx: int) -> List[Dict[str, Any]]:
        """Validar SBC según tipo de movimiento."""
        errores = []
        
        if movimiento.tipo in ["alta", "modificacion"]:
            # Altas y modificaciones requieren SBC
            if movimiento.sbc is None:
                errores.append({
                    "tipo": "sbc_requerido",
                    "empresa": empresa.registro_patronal,
                    "movimiento_idx": mov_idx,
                    "campo": "sbc",
                    "valor": movimiento.sbc,
                    "mensaje": "El SBC es obligatorio para altas y modificaciones"
                })
            elif movimiento.sbc <= 0:
                errores.append({
                    "tipo": "sbc_invalido",
                    "empresa": empresa.registro_patronal,
                    "movimiento_idx": mov_idx,
                    "campo": "sbc",
                    "valor": movimiento.sbc,
                    "mensaje": "El SBC debe ser mayor a 0"
                })
            elif not ValidationRules.validar_sbc_limite(movimiento.sbc):
                errores.append({
                    "tipo": "sbc_excede_limite",
                    "empresa": empresa.registro_patronal,
                    "movimiento_idx": mov_idx,
                    "campo": "sbc",
                    "valor": movimiento.sbc,
                    "mensaje": f"El SBC no puede exceder ${ValidationRules.get_sbc_maximo()}"
                })
        
        elif movimiento.tipo == "baja":
            # Bajas no deben tener SBC
            if movimiento.sbc is not None and movimiento.sbc != 0:
                errores.append({
                    "tipo": "sbc_no_permitido_baja",
                    "empresa": empresa.registro_patronal,
                    "movimiento_idx": mov_idx,
                    "campo": "sbc",
                    "valor": movimiento.sbc,
                    "mensaje": "Las bajas no deben incluir SBC"
                })
        
        return errores
    
    @staticmethod
    def _validar_tipo_motivo(movimiento: MovimientoBase, empresa: EmpresaBase, mov_idx: int) -> List[Dict[str, Any]]:
        """Validar tipo de movimiento y motivo."""
        errores = []
        
        if movimiento.tipo == "baja":
            # Bajas requieren motivo
            if not movimiento.motivo:
                errores.append({
                    "tipo": "motivo_requerido_baja",
                    "empresa": empresa.registro_patronal,
                    "movimiento_idx": mov_idx,
                    "campo": "motivo",
                    "valor": movimiento.motivo,
                    "mensaje": "El motivo es obligatorio para bajas"
                })
        else:
            # Otros tipos no deben tener motivo
            if movimiento.motivo:
                errores.append({
                    "tipo": "motivo_no_permitido",
                    "empresa": empresa.registro_patronal,
                    "movimiento_idx": mov_idx,
                    "campo": "motivo",
                    "valor": movimiento.motivo,
                    "mensaje": "El motivo solo se permite para bajas"
                })
        
        return errores
    
    @staticmethod
    def obtener_resumen_validacion(movimientos: List[MovimientoValidado], errores_detallados: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generar resumen de la validación.
        
        Args:
            movimientos: Lista de movimientos validados
            errores_detallados: Lista de errores detallados
            
        Returns:
            Diccionario con resumen de validación
        """
        total_movimientos = len(movimientos)
        movimientos_validos = len([m for m in movimientos if m.es_valido])
        movimientos_invalidos = total_movimientos - movimientos_validos
        
        # Contar errores por tipo
        errores_por_tipo = {}
        for error in errores_detallados:
            tipo_error = error.get("tipo", "desconocido")
            errores_por_tipo[tipo_error] = errores_por_tipo.get(tipo_error, 0) + 1
        
        return {
            "total_movimientos": total_movimientos,
            "movimientos_validos": movimientos_validos,
            "movimientos_invalidos": movimientos_invalidos,
            "porcentaje_exito": (movimientos_validos / total_movimientos * 100) if total_movimientos > 0 else 0,
            "errores_por_tipo": errores_por_tipo,
            "errores_detallados": errores_detallados
        } 