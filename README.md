# Procesamiento de Movimientos IDSE 

## Alcance del programa

- **Encuentra errores** antes de enviar al IMSS
- **Genera archivos** con el formato exacto del IMSS
- **Reporte de errores** denota qué está mal en el input y señala su ubicación
- **Continúa trabajando** aunque encuentre errores
- **Te da estadísticas** claras de lo que procesó

## Instrucciones para correr el programa

```bash
# 1. Descargar el proyecto
git clone https://github.com/Beltry201/movimientos-idse.git
cd movimientos-idse

# 2. Preparar el entorno
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. ¡A usar!
python sistema_idse.py
```

## Procesamiento de archivos (opción 1)

### Indicar la ruta del archivo json
```
📂 Ingrese la ruta del archivo JSON: examples/input-ejemplo-2.json
```

### Despligue de resultados
```
✅ PROCESAMIENTO COMPLETADO
📊 Estadísticas:
   • Empresas procesadas: 2
   • Movimientos totales: 20
   • Movimientos válidos: 17
   • Movimientos inválidos: 3
   • Archivos generados: 10

❌ ERRORES ENCONTRADOS:
🏢 Empresa: A1234567890
   📋 Movimiento 7: NSS inválido (5554567890)
   📋 Movimiento 8: Fecha inválida (2024-02-30)

📁 Archivos generados:
   • IDSE_ALT_012024_A1234567890.txt
   • IDSE_MOD_032024_A1234567890.txt
   • IDSE_BAJ_032024_A1234567890.txt
   ... y más!
```

## Validaciones de sistema

### Datos básicos
- **NSS**: Exactamente 11 dígitos
- **CURP**: Exactamente 18 caracteres
- **Fechas**: Formato correcto (YYYY-MM-DD)
- **Registro Patronal**: 11 caracteres

### Salario Base Cotización (SBC)
- **Altas/Modificaciones**: SBC entre $1 y $2,089.12
- **Bajas**: NO debe incluir SBC

### Tipos de movimiento
- **Alta**: Nuevo empleado
- **Baja**: Salida del empleado (con motivo)
- **Modificación**: Cambio de datos

## Generación de archivos

El sistema crea archivos `.txt` con nombres como:
- `IDSE_ALT_012024_A1234567890.txt` (Altas de enero 2024)
- `IDSE_BAJ_032024_A1234567890.txt` (Bajas de marzo 2024)
- `IDSE_MOD_042024_A1234567890.txt` (Modificaciones de abril 2024)

Cada archivo tiene exactamente 44 caracteres por línea, como requiere el IMSS.

## Tests

Archivos de ejemplo para que puedas probar:

```bash
# Archivo con movimientos válidos
examples/input-ejemplo.json

# Archivo con errores para ver la validación en acción
examples/input-ejemplo-2.json
```

## Ejecutar tests

```bash
pytest
```

## Estructura del proyecto

```
movimientos-idse/
├── src/                    # Código principal
│   ├── models/            # Estructuras de datos
│   ├── validators/        # Validaciones
│   ├── services/          # Lógica de negocio
│   └── utils/             # Utilidades
├── tests/                 # Tests
├── examples/              # Archivos de ejemplo
├── output/                # Archivos generados
└── sistema_idse.py        # Interfaz principal
```