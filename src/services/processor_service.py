from typing import List, Dict, Any
from loguru import logger
from ..models import MovimientoValidado
from ..validators import MovimientoValidator
from .file_generator_service import FileGeneratorService


class ProcessorService:
    """Servicio principal de procesamiento de movimientos IDSE."""
    
    def __init__(self):
        """Inicializar el servicio de procesamiento."""
        self.file_generator = FileGeneratorService()
    
    def procesar_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesar JSON de entrada y generar archivos IDSE.
        
        Args:
            data: JSON con empresas y movimientos
            
        Returns:
            Diccionario con resultados del procesamiento
        """
        try:
            logger.info("Iniciando procesamiento de movimientos IDSE")
            
            # 1. Validar movimientos
            movimientos_validados, errores_detallados = MovimientoValidator.validar_movimientos(data)
            logger.info(f"Movimientos validados: {len(movimientos_validados)}")
            
            # 2. Obtener resumen de validación
            resumen = MovimientoValidator.obtener_resumen_validacion(movimientos_validados, errores_detallados)
            logger.info(f"Resumen: {resumen['movimientos_validos']} válidos, {resumen['movimientos_invalidos']} inválidos")
            
            # 3. Filtrar solo movimientos válidos para generación de archivos
            movimientos_validos = [m for m in movimientos_validados if m.es_valido]
            
            # 4. Generar archivos IDSE
            archivos = []
            if movimientos_validos:
                archivos = self.file_generator.generar_archivos_idse(movimientos_validos)
                logger.info(f"Archivos generados: {len(archivos)}")
            
            # 5. Preparar respuesta
            resultado = {
                "resumen": {
                    "total_empresas": len(data.get("empresa", [])),
                    "total_movimientos": resumen["total_movimientos"],
                    "movimientos_validos": resumen["movimientos_validos"],
                    "movimientos_invalidos": resumen["movimientos_invalidos"],
                    "archivos_a_generar": len(archivos)
                },
                "archivos": archivos,
                "errores": errores_detallados
            }
            
            logger.info("Procesamiento completado exitosamente")
            return resultado
            
        except Exception as e:
            logger.error(f"Error en procesamiento: {e}")
            raise
    
    def _extraer_errores(self, movimientos: List[MovimientoValidado]) -> List[Dict[str, Any]]:
        """
        Extraer errores de movimientos inválidos.
        
        Args:
            movimientos: Lista de movimientos validados
            
        Returns:
            Lista de errores formateados
        """
        errores = []
        
        for i, movimiento in enumerate(movimientos):
            if not movimiento.es_valido:
                errores.append({
                    "movimiento_index": i,
                    "empleado_nss": movimiento.empleado.nss,
                    "tipo_movimiento": movimiento.tipo,
                    "fecha_movimiento": movimiento.fecha_movimiento,
                    "errores": movimiento.errores
                })
        
        return errores
    
    def procesar_archivo_json(self, contenido_archivo: str) -> Dict[str, Any]:
        """
        Procesar contenido de archivo JSON.
        
        Args:
            contenido_archivo: Contenido del archivo JSON como string
            
        Returns:
            Resultado del procesamiento
        """
        import json
        
        try:
            # Parsear JSON
            data = json.loads(contenido_archivo)
            logger.info("Archivo JSON parseado correctamente")
            
            # Procesar con el método principal
            return self.procesar_json(data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parseando JSON: {e}")
            raise ValueError(f"Archivo JSON inválido: {e}")
        except Exception as e:
            logger.error(f"Error procesando archivo: {e}")
            raise
    
    def obtener_estadisticas(self, movimientos: List[MovimientoValidado]) -> Dict[str, Any]:
        """
        Obtener estadísticas detalladas de los movimientos.
        
        Args:
            movimientos: Lista de movimientos validados
            
        Returns:
            Estadísticas detalladas
        """
        if not movimientos:
            return {
                "total_movimientos": 0,
                "por_tipo": {},
                "por_empresa": {},
                "por_periodo": {}
            }
        
        # Estadísticas por tipo
        por_tipo = {}
        for movimiento in movimientos:
            tipo = movimiento.tipo
            if tipo not in por_tipo:
                por_tipo[tipo] = {"total": 0, "validos": 0, "invalidos": 0}
            
            por_tipo[tipo]["total"] += 1
            if movimiento.es_valido:
                por_tipo[tipo]["validos"] += 1
            else:
                por_tipo[tipo]["invalidos"] += 1
        
        # Estadísticas por empresa
        por_empresa = {}
        for movimiento in movimientos:
            empresa = movimiento.registro_patronal
            if empresa not in por_empresa:
                por_empresa[empresa] = {"total": 0, "validos": 0, "invalidos": 0}
            
            por_empresa[empresa]["total"] += 1
            if movimiento.es_valido:
                por_empresa[empresa]["validos"] += 1
            else:
                por_empresa[empresa]["invalidos"] += 1
        
        # Estadísticas por periodo
        por_periodo = {}
        for movimiento in movimientos:
            periodo = movimiento.periodo
            if periodo not in por_periodo:
                por_periodo[periodo] = {"total": 0, "validos": 0, "invalidos": 0}
            
            por_periodo[periodo]["total"] += 1
            if movimiento.es_valido:
                por_periodo[periodo]["validos"] += 1
            else:
                por_periodo[periodo]["invalidos"] += 1
        
        return {
            "total_movimientos": len(movimientos),
            "por_tipo": por_tipo,
            "por_empresa": por_empresa,
            "por_periodo": por_periodo
        } 