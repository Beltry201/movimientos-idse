# Sistema IDSE - Procesamiento de Movimientos IMSS

Sistema para procesar movimientos de empleados y generar archivos compatibles con el portal IDSE (IMSS Desde Su Empresa) del Instituto Mexicano del Seguro Social.

## Características

- ✅ Validación completa de movimientos según reglas IMSS
- ✅ Generación de archivos .txt con formato IDSE exacto
- ✅ Interfaz de consola interactiva
- ✅ Tests comprehensivos
- ✅ Logging detallado
- ✅ Manejo de errores robusto
- ✅ Validación granular con reportes detallados

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Beltry201/movimientos-idse.git
cd movimientos-idse

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

### Ejecutar la aplicación

```bash
# Ejecutar sistema interactivo
python sistema_idse.py
```

### Funcionalidades disponibles

- **Procesar archivo JSON**: Cargar y procesar archivos JSON con movimientos
- **Validaciones de ejemplo**: Ver reglas y formatos de validación
- **Generar archivos IDSE**: Crear archivos de ejemplo
- **Tests del sistema**: Ejecutar validaciones automatizadas
- **Información del sistema**: Ver detalles y estadísticas
- **Limpiar archivos**: Eliminar archivos generados

### Ejemplo de uso

```bash
# Ejecutar el sistema
python sistema_idse.py

# Seleccionar opción 1 para procesar un archivo JSON
# Ingresar la ruta del archivo: examples/input-ejemplo-2.json
```

### Ejemplo de salida

```
✅ PROCESAMIENTO COMPLETADO
==================================================
📊 Estadísticas:
   • Empresas procesadas: 2
   • Movimientos totales: 20
   • Movimientos válidos: 17
   • Movimientos inválidos: 3
   • Archivos generados: 10

❌ ERRORES DE VALIDACIÓN DETECTADOS:
--------------------------------------------------
🏢 Empresa: A1234567890
   📋 Movimiento 7:
      ❌ Tipo: nss_invalido
      📝 Campo: empleado.nss
      💾 Valor: 5554567890
      ⚠️  Error: El NSS debe tener exactamente 11 dígitos (actual: 10)

📁 Archivos IDSE generados:
   • IDSE_ALT_012024_A1234567890.txt
     - Tipo: alta
     - Periodo: 012024
     - Registro Patronal: A1234567890
     - Movimientos: 1
     - Tamaño: 44 bytes
```

## Tests

```bash
# Ejecutar todos los tests
pytest

# Tests con coverage
pytest --cov=src

# Tests específicos
pytest tests/unit/
```

## Estructura del Proyecto

```
movimientos-idse/
├── src/
│   ├── models/          # Modelos Pydantic (Empleado, Empresa, Movimiento)
│   ├── validators/      # Lógica de validación con reportes detallados
│   ├── services/        # Servicios de procesamiento y generación de archivos
│   ├── utils/           # Utilidades (fechas, formato)
│   └── config/          # Configuración y constantes
├── tests/               # Tests unitarios
├── examples/            # Archivos JSON de ejemplo
├── output/              # Archivos IDSE generados
├── sistema_idse.py      # Interfaz de consola principal
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Documentación
```

## Reglas de Validación

### Campos Obligatorios
- **NSS**: Exactamente 11 dígitos numéricos
- **CURP**: Exactamente 18 caracteres alfanuméricos
- **Registro Patronal**: 11 caracteres alfanuméricos
- **Fechas**: Formato YYYY-MM-DD válido

### SBC (Salario Base Cotización)
- **Altas/Modificaciones**: SBC > 0 y SBC ≤ $2,089.12
- **Bajas**: NO debe incluir SBC

### Motivos de Baja
- `renuncia` → código 01
- `despido` → código 02
- `termino_contrato` → código 03
- `invalidez` → código 04
- `muerte` → código 05

### Reglas de Unicidad
- Máximo 1 alta por empleado por mes
- Máximo 1 baja por empleado por mes
- Múltiples modificaciones permitidas si SBC diferente

## Formato de Archivo IDSE

Cada línea tiene exactamente 44 caracteres:
- Posiciones 1-11: Registro Patronal
- Posiciones 12-22: NSS del empleado
- Posiciones 23-24: Tipo movimiento (07=alta, 08=modificación, 09=baja)
- Posiciones 25-26: Razón salida (01-05 para bajas, 00 para otros)
- Posiciones 27-34: Fecha DDMMYYYY
- Posiciones 35-44: SBC sin decimales, pad con ceros

## Validación Robusta

El sistema implementa validación robusta que:

- ✅ **Procesa movimientos válidos** incluso cuando hay errores
- ✅ **Reporta errores detallados** con ubicación específica
- ✅ **Continúa el procesamiento** sin interrumpir por errores
- ✅ **Genera archivos** para movimientos válidos
- ✅ **Maneja excepciones** de forma elegante

### Ejemplo de reporte de errores

```
❌ ERRORES DE VALIDACIÓN DETECTADOS:
--------------------------------------------------
🏢 Empresa: A1234567890
   📋 Movimiento 7:
      ❌ Tipo: nss_invalido
      📝 Campo: empleado.nss
      💾 Valor: 5554567890
      ⚠️  Error: El NSS debe tener exactamente 11 dígitos (actual: 10)
   📋 Movimiento 8:
      ❌ Tipo: fecha_invalida
      📝 Campo: fecha_movimiento
      💾 Valor: 2024-02-30
      ⚠️  Error: La fecha debe tener formato YYYY-MM-DD
```

## Archivos de Ejemplo

El proyecto incluye archivos JSON de ejemplo:

- `examples/input-ejemplo.json`: Ejemplo básico con movimientos válidos
- `examples/input-ejemplo-2.json`: Ejemplo con errores de validación para demostrar el sistema

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 