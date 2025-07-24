#!/usr/bin/env python3
"""
Sistema IDSE - IMSS Desde Su Empresa
=====================================

Interfaz unificada para procesar movimientos IDSE del IMSS.
Consolida todas las funcionalidades de demo y testing en una sola aplicación.
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, List

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Importar componentes del sistema
from src.services.processor_service import ProcessorService
from src.services.file_generator_service import FileGeneratorService
from src.validators.movimiento_validator import MovimientoValidator
from src.config.constants import *
from src.utils.date_utils import *
from src.utils.format_utils import *
from loguru import logger

class SistemaIDSE:
    """Clase principal del Sistema IDSE"""
    
    def __init__(self):
        """Inicializar el sistema"""
        self.processor = ProcessorService()
        self.file_generator = FileGeneratorService()
        
        # Configurar logging
        logger.remove()
        logger.add(sys.stderr, level="INFO", format="{time} | {level} | {message}")
        
        # Crear directorios necesarios
        os.makedirs("output", exist_ok=True)
        os.makedirs("logs", exist_ok=True)
    
    def mostrar_banner(self):
        """Mostrar banner del sistema"""
        print("🚀 Sistema IDSE - IMSS Desde Su Empresa")
        print("=" * 50)
        print("📋 Versión: 1.0.0")
        print("🏢 Procesamiento de movimientos IMSS")
        print("📄 Generación de archivos IDSE")
        print("=" * 50)
    
    def mostrar_menu_principal(self):
        """Mostrar menú principal"""
        print("\n📋 MENÚ PRINCIPAL")
        print("=" * 30)
        print("1. 📊 Procesar archivo JSON")
        print("2. 🔍 Ejecutar validaciones de ejemplo")
        print("3. 📁 Generar archivos IDSE de ejemplo")
        print("4. 🧪 Ejecutar tests del sistema")
        print("5. 📖 Mostrar información del sistema")
        print("6. 🧹 Limpiar archivos generados")
        print("0. ❌ Salir")
        print("=" * 30)
    
    def procesar_archivo_json(self):
        """Procesar archivo JSON ingresado por el usuario"""
        print("\n📊 PROCESAR ARCHIVO JSON")
        print("-" * 30)
        
        # Solicitar ruta del archivo
        ruta_archivo = input("📂 Ingrese la ruta del archivo JSON: ").strip()
        
        if not ruta_archivo:
            print("❌ No se ingresó una ruta válida")
            return
        
        if not os.path.exists(ruta_archivo):
            print(f"❌ El archivo {ruta_archivo} no existe")
            return
        
        try:
            # Leer y procesar archivo
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            resultado = self.processor.procesar_archivo_json(contenido)
            
            # Mostrar resultados
            self.mostrar_resultados_procesamiento(resultado)
            
        except Exception as e:
            print(f"❌ Error procesando archivo: {e}")
            logger.exception("Error en procesamiento de archivo")
    
    def ejecutar_validaciones_ejemplo(self):
        """Ejecutar validaciones con datos de ejemplo"""
        print("\n🔍 VALIDACIONES DE EJEMPLO")
        print("-" * 30)
        
        # Mostrar reglas de validación
        print("📋 REGLAS DE VALIDACIÓN:")
        print("   • SBC máximo: $2089.12")
        print("   • NSS longitud: 11 dígitos")
        print("   • CURP longitud: 18 caracteres")
        print("   • Registro patronal: 11 caracteres")
        print("   • Línea IDSE: 44 caracteres")
        
        print("\n📝 TIPOS DE MOVIMIENTO:")
        for tipo in TipoMovimiento:
            codigo = CodigoTipoMovimiento[tipo.value].value
            print(f"   • {tipo.value}: {codigo}")
        
        print("\n🏷️ MOTIVOS DE BAJA:")
        for motivo in MotivoBaja:
            codigo = CodigoMotivoBaja[motivo.value].value
            print(f"   • {motivo.value}: {codigo}")
        
        # Mostrar formato IDSE
        print("\n📄 FORMATO IDSE")
        print("=" * 30)
        print("Cada línea tiene exactamente 44 caracteres:")
        print("┌─────────────┬─────────────┬────┬────┬────────┬────────────┐")
        print("│ Registro    │ NSS         │Tipo│Razón│ Fecha  │    SBC     │")
        print("│ Patronal    │ Empleado    │Mov.│Sal. │DDMMYYYY│  (centavos)│")
        print("│   (11)      │   (11)      │(2) │ (2) │  (8)   │   (10)     │")
        print("└─────────────┴─────────────┴────┴────┴────────┴────────────┘")
        
        ejemplo_linea = "B5510768108098765432100700010320230000112000"
        print(f"Ejemplo de línea IDSE:")
        print(f"'{ejemplo_linea}'")
        print(f"Longitud: {len(ejemplo_linea)} caracteres")
        
        # Desglose del ejemplo
        print("\nDesglose:")
        print(f"  Registro Patronal: '{ejemplo_linea[:11]}'")
        print(f"  NSS: '{ejemplo_linea[11:22]}'")
        print(f"  Tipo Movimiento: '{ejemplo_linea[22:24]}' (07 = alta)")
        print(f"  Razón Salida: '{ejemplo_linea[24:26]}' (00 = no aplica)")
        print(f"  Fecha: '{ejemplo_linea[26:34]}' (05/03/2023)")
        print(f"  SBC: '{ejemplo_linea[34:44]}' (112000 centavos = $1,120.00)")
    
    def generar_archivos_ejemplo(self):
        """Generar archivos IDSE con datos de ejemplo"""
        print("\n📁 GENERAR ARCHIVOS IDSE DE EJEMPLO")
        print("-" * 40)
        
        # Cargar datos de ejemplo
        archivo_ejemplo = "examples/input-ejemplo.json"
        
        if not os.path.exists(archivo_ejemplo):
            print(f"❌ No se encontró el archivo de ejemplo: {archivo_ejemplo}")
            return
        
        try:
            # Leer datos de ejemplo
            with open(archivo_ejemplo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Procesar datos
            resultado = self.processor.procesar_archivo_json(contenido)
            
            # Mostrar resultados
            self.mostrar_resultados_procesamiento(resultado)
            
        except Exception as e:
            print(f"❌ Error generando archivos de ejemplo: {e}")
            logger.exception("Error en generación de archivos de ejemplo")
    

    
    def ejecutar_tests_sistema(self):
        """Ejecutar tests del sistema"""
        print("\n🧪 TESTS DEL SISTEMA")
        print("-" * 20)
        
        print("🔍 Ejecutando tests unitarios...")
        
        try:
            # Ejecutar tests con pytest
            import subprocess
            resultado = subprocess.run([
                "python", "-m", "pytest", "tests/", "-v"
            ], capture_output=True, text=True)
            
            if resultado.returncode == 0:
                print("✅ Tests ejecutados exitosamente")
                print(resultado.stdout)
            else:
                print("❌ Algunos tests fallaron")
                print(resultado.stdout)
                print(resultado.stderr)
                
        except Exception as e:
            print(f"❌ Error ejecutando tests: {e}")
    
    def mostrar_informacion_sistema(self):
        """Mostrar información del sistema"""
        print("\n📖 INFORMACIÓN DEL SISTEMA")
        print("=" * 30)
        
        print("🚀 Sistema IDSE - IMSS Desde Su Empresa")
        print("📋 Versión: 1.0.0")
        print("🏢 Propósito: Procesamiento de movimientos IMSS")
        print("📄 Funcionalidad: Generación de archivos IDSE")
        
        print("\n📁 Estructura del proyecto:")
        print("   • src/ - Código fuente del sistema")
        print("   • examples/ - Archivos de ejemplo")
        print("   • tests/ - Tests unitarios")
        print("   • output/ - Archivos IDSE generados")
        print("   • logs/ - Archivos de log")
        
        print("\n🔧 Tecnologías utilizadas:")
        print("   • Python 3.x")
        print("   • Pydantic v1.10.2")
        print("   • Loguru 0.7.0")
        print("   • pytest 7.3.1")
        
        print("\n📋 Funcionalidades principales:")
        print("   • Validación de movimientos IMSS")
        print("   • Generación de archivos IDSE")
        print("   • Tests automatizados")
        print("   • Logging detallado")
        
        # Mostrar archivos en output
        output_dir = "output"
        if os.path.exists(output_dir):
            archivos = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
            if archivos:
                print(f"\n📁 Archivos IDSE generados ({len(archivos)}):")
                for archivo in archivos[:5]:  # Mostrar solo los primeros 5
                    ruta = os.path.join(output_dir, archivo)
                    tamaño = os.path.getsize(ruta)
                    print(f"   • {archivo} ({tamaño} bytes)")
                if len(archivos) > 5:
                    print(f"   ... y {len(archivos) - 5} archivos más")
    
    def limpiar_archivos_generados(self):
        """Limpiar archivos generados"""
        print("\n🧹 LIMPIAR ARCHIVOS GENERADOS")
        print("-" * 30)
        
        # Limpiar directorio output
        output_dir = "output"
        if os.path.exists(output_dir):
            archivos = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
            if archivos:
                for archivo in archivos:
                    ruta = os.path.join(output_dir, archivo)
                    os.remove(ruta)
                    print(f"🗑️  Eliminado: {archivo}")
                print(f"✅ Se eliminaron {len(archivos)} archivos")
            else:
                print("📁 No hay archivos para eliminar")
        else:
            print("📁 El directorio output no existe")
        
        # Limpiar archivos __pycache__
        import subprocess
        try:
            subprocess.run([
                "find", ".", "-name", "__pycache__", "-type", "d", 
                "-not", "-path", "./venv/*", "-exec", "rm", "-rf", "{}", "+"
            ], capture_output=True)
            print("🧹 Archivos __pycache__ eliminados")
        except:
            print("⚠️  No se pudieron eliminar archivos __pycache__")
    
    def mostrar_resultados_procesamiento(self, resultado: Dict[str, Any]):
        """Mostrar resultados del procesamiento"""
        print("\n✅ PROCESAMIENTO COMPLETADO")
        print("=" * 50)
        
        # Mostrar estadísticas
        resumen = resultado.get('resumen', {})
        print(f"📊 Estadísticas:")
        print(f"   • Empresas procesadas: {resumen.get('total_empresas', 0)}")
        print(f"   • Movimientos totales: {resumen.get('total_movimientos', 0)}")
        print(f"   • Movimientos válidos: {resumen.get('movimientos_validos', 0)}")
        print(f"   • Movimientos inválidos: {resumen.get('movimientos_invalidos', 0)}")
        print(f"   • Archivos generados: {resumen.get('archivos_a_generar', 0)}")
        
        # Mostrar errores detallados si los hay
        errores = resultado.get('errores', [])
        if errores:
            print(f"\n❌ ERRORES DE VALIDACIÓN DETECTADOS:")
            print("-" * 50)
            
            # Agrupar errores por empresa
            errores_por_empresa = {}
            for error in errores:
                empresa = error.get('empresa', 'DESCONOCIDA')
                if empresa not in errores_por_empresa:
                    errores_por_empresa[empresa] = []
                errores_por_empresa[empresa].append(error)
            
            for empresa, errores_empresa in errores_por_empresa.items():
                print(f"\n🏢 Empresa: {empresa}")
                for error in errores_empresa:
                    tipo = error.get('tipo', 'error_desconocido')
                    mensaje = error.get('mensaje', 'Error sin descripción')
                    campo = error.get('campo', 'campo_desconocido')
                    valor = error.get('valor', 'valor_desconocido')
                    mov_idx = error.get('movimiento_idx', 'N/A')
                    
                    print(f"   📋 Movimiento {mov_idx}:")
                    print(f"      ❌ Tipo: {tipo}")
                    print(f"      📝 Campo: {campo}")
                    print(f"      💾 Valor: {valor}")
                    print(f"      ⚠️  Error: {mensaje}")
                    print()
        
        # Mostrar archivos generados
        archivos = resultado.get('archivos', [])
        if archivos:
            print(f"\n📁 Archivos IDSE generados:")
            for archivo in archivos:
                print(f"   • {archivo['nombre']}")
                print(f"     - Tipo: {archivo['tipo']}")
                print(f"     - Periodo: {archivo['periodo']}")
                print(f"     - Registro Patronal: {archivo['registro_patronal']}")
                print(f"     - Movimientos: {archivo['cantidad_movimientos']}")
                print(f"     - Tamaño: {archivo['tamaño_bytes']} bytes")
        
        # Verificar archivos en disco
        output_dir = "output"
        if os.path.exists(output_dir):
            archivos_disco = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
            if archivos_disco:
                print(f"\n💾 Archivos en disco ({output_dir}/):")
                for archivo in archivos_disco:
                    ruta_completa = os.path.join(output_dir, archivo)
                    tamaño = os.path.getsize(ruta_completa)
                    print(f"   • {archivo} ({tamaño} bytes)")
    
    def ejecutar(self):
        """Ejecutar el sistema principal"""
        self.mostrar_banner()
        
        while True:
            try:
                self.mostrar_menu_principal()
                opcion = input("\n🔢 Seleccione una opción: ").strip()
                
                if opcion == "1":
                    self.procesar_archivo_json()
                elif opcion == "2":
                    self.ejecutar_validaciones_ejemplo()
                elif opcion == "3":
                    self.generar_archivos_ejemplo()
                elif opcion == "4":
                    self.ejecutar_tests_sistema()
                elif opcion == "5":
                    self.mostrar_informacion_sistema()
                elif opcion == "6":
                    self.limpiar_archivos_generados()
                elif opcion == "0":
                    print("\n👋 ¡Gracias por usar el Sistema IDSE!")
                    break
                else:
                    print("❌ Opción inválida. Intente nuevamente.")
                
                input("\n⏸️  Presione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                logger.exception("Error inesperado en el sistema")

def main():
    """Función principal"""
    try:
        sistema = SistemaIDSE()
        sistema.ejecutar()
    except Exception as e:
        print(f"❌ Error iniciando el sistema: {e}")
        logger.exception("Error crítico en el sistema")

if __name__ == "__main__":
    main() 