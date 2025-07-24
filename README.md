# Sistema IDSE - Procesamiento de Movimientos IMSS

Sistema para procesar movimientos de empleados y generar archivos compatibles con el portal IDSE (IMSS Desde Su Empresa) del Instituto Mexicano del Seguro Social.

## Características

- ✅ Validación completa de movimientos según reglas IMSS
- ✅ Generación de archivos .txt con formato IDSE exacto
- ✅ Interfaz de consola interactiva
- ✅ Tests comprehensivos
- ✅ Logging detallado
- ✅ Manejo de errores robusto

## Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd movimientos_idse

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

# O ejecutar directamente
python -m src.main
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
# Ingresar la ruta del archivo: examples/input-ejemplo.json
```

## Tests

```bash
# Ejecutar todos los tests
pytest

# Tests con coverage
pytest --cov=src

# Tests específicos
pytest tests/unit/
pytest tests/integration/
```

## Estructura del Proyecto

```
src/
├── models/          # Modelos Pydantic
├── validators/      # Lógica de validación
├── services/        # Servicios de procesamiento
├── utils/           # Utilidades
├── config/          # Configuración
└── main.py          # Punto de entrada
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

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 