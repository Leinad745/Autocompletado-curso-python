# Bot de Automatización de Curso Python (RPA)

Este proyecto corresponde a la **Evaluación 1 / Caso Semestral** de la asignatura **Automatización de Procesos Robóticos** (RPA).

Consiste en un bot en Python desarrollado con **Selenium WebDriver** diseñado para ejecutarse en modo headless (servidores Linux / TTY, flujos n8n, terminales sin interfaz gráfica), automatizando la interacción, ingreso de parámetros (STDIN) y ejecución secuencial de los 20 módulos interactivos del curso web de Python en [https://mantistcy.cl/aprenderpython/](https://mantistcy.cl/aprenderpython/).

---

## 📋 Tabla de Contenidos
- [Descripción General](#-descripción-general)
- [Modo Servidor / Headless](#-modo-servidor--headless)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso y Ejecución](#-uso-y-ejecución)
- [Formato del Log de Ejecución y Cobertura](#-formato-del-log-de-ejecución-y-cobertura)
- [Módulos Automatizados](#-módulos-automatizados)

---

## 🚀 Descripción General

El script [botCurso.py](file:///home/sub4k3m1/Estudios/Universidad/6to-semestre/AutomatizacionDeProcesosRoboticos/CasoSemestral/codigoCursoPython/botCurso.py) simula la interacción completa de un usuario en la plataforma educativa del curso. Automatiza de manera robótica las siguientes tareas:

1. **Inicio y Conexión Headless**: Inicializa Mozilla Firefox en segundo plano (`-headless`, `--disable-gpu`, `--no-sandbox`).
2. **Navegación Dinámica**: Selecciona cada módulo desde la barra de navegación lateral (`github-sidebar`).
3. **Desplazamiento (Scroll)**: Ajusta la vista del navegador hacia el elemento del módulo correspondiente (`scrollIntoView`).
4. **Entrada de Datos (STDIN)**: Detecta ejercicios interactivos que requieren entrada de usuario, limpia el campo e ingresa los valores prefijados.
5. **Compilación y Ejecución**: Dispara la ejecución del snippet de código del módulo mediante un clic JavaScript.
6. **Sincronización por Espera Explícita**: Aguarda a que el elemento de consola (`console-{slug}`) aparezca en pantalla confirmando la respuesta del servidor antes de avanzar.
7. **Monitoreo y Métricas de Cobertura**: Calcula tiempos individuales, tasa de éxito y porcentaje de cobertura global, exportando los resultados en formato JSON y guardando una copia en la carpeta `logs/`.

---

## 🖥️ Modo Servidor / Headless

El script está adaptado a la arquitectura de [botCursoHeadless.py](file:///home/sub4k3m1/Estudios/Universidad/6to-semestre/AutomatizacionDeProcesosRoboticos/CasoSemestral/codigoCursoPython/botCursoHeadless.py):
- **Opciones de Firefox**: Sin entorno gráfico (`-headless`), deshabilitando GPU y con `--no-sandbox`.
- **Compatibilidad de Geckodriver**: Soporta rutas de servidor Linux (`/usr/local/bin/geckodriver`) con fallback automático a la ruta del sistema (`/usr/bin/geckodriver` o variable `PATH`).
- **Salida estándar limpia**: Retorna un objeto JSON por `stdout`, facilitando su integración directa en herramientas de automatización como **n8n**, cronjobs o pipelines CI/CD.

---

## 📁 Estructura del Proyecto

```text
codigoCursoPython/
├── botCurso.py            # Script principal adaptado (Headless + Logs + Cobertura)
├── botCursoHeadless.py    # Script de referencia para servidor TTY
├── logs/                  # Registro histórico de ejecuciones en formato JSON
└── README.md              # Documentación técnica
```

---

## 🔧 Requisitos Previos

- **Python 3.8+**
- **Mozilla Firefox**
- **GeckoDriver** (disponible en `/usr/local/bin/geckodriver` o en el `PATH` del sistema).

---

## 💻 Instalación y Configuración

```bash
pip install selenium
```

---

## ▶️ Uso y Ejecución

Ejecuta el script directamente desde la terminal:

```bash
python botCurso.py
```

También puede ser importado como módulo en otros scripts de Python:

```python
from botCurso import ejecutar_bot_curso

resultado = ejecutar_bot_curso()
print(f"Cobertura obtenida: {resultado['cobertura']['porcentaje_cobertura']}%")
```

---

## 📊 Formato del Log de Ejecución y Cobertura

Al finalizar, el bot retorna un objeto JSON estructurado:

```json
{
  "fecha_inicio": "2026-10-05T09:28:57.568753",
  "fecha_fin": "2026-10-05T09:29:12.313062",
  "duracion_segundos": 14.74,
  "estado_general": "COMPLETADO",
  "plataforma_url": "https://mantistcy.cl/aprenderpython/",
  "modo_ejecucion": "headless (servidor Linux TTY)",
  "cobertura": {
    "total_modulos": 20,
    "modulos_exitosos": 20,
    "modulos_fallidos": 0,
    "porcentaje_cobertura": 100.0
  },
  "detalle_modulos": [
    {
      "modulo_id": "sentencia-que-es-python",
      "slug": "que-es-python",
      "nombre": "¿Qué es Python?",
      "input_data": "",
      "estado": "exitoso",
      "duracion_segundos": 0.62,
      "error": null
    }
  ],
  "archivo_log": ".../logs/log_ejecucion_20261005_092857.json",
  "error": null
}
```

---

## 📚 Módulos Automatizados

El bot cubre los 20 módulos disponibles en la plataforma:

| # | ID Módulo | Slug | Nombre del Módulo | STDIN |
|---|:---|:---|:---|:---|
| 1 | `sentencia-que-es-python` | `que-es-python` | ¿Qué es Python? | *(Vacío)* |
| 2 | `sentencia-variables-print` | `variables-print` | Variables y Comando Print | *(Vacío)* |
| 3 | `sentencia-ideacion-importancia` | `ideacion-importancia` | Ideación e Importancia | *(Vacío)* |
| 4 | `sentencia-entrada-salida` | `entrada-salida` | Entrada y Salida de Datos | `Estudiante Python` |
| 5 | `sentencia-importancia-indentacion` | `importancia-indentacion` | Importancia de la Indentación | *(Vacío)* |
| 6 | `sentencia-if-elif-else-avanzado` | `if-elif-else-avanzado` | Estructuras if / elif / else | *(Vacío)* |
| 7 | `sentencia-try-except` | `try-except` | Gestión de Errores (try / except) | *(Vacío)* |
| 8 | `sentencia-while-loop-basico` | `while-loop-basico` | While: Fundamentos y Contadores | *(Vacío)* |
| 9 | `sentencia-while-loop-condicional` | `while-loop-condicional` | While: Control por Banderas | `25` |
| 10 | `sentencia-for-loop-listas` | `for-loop-listas` | For: Recorrido de Colecciones | *(Vacío)* |
| 11 | `sentencia-for-range-completo` | `for-range-completo` | For con Range: Rangos Avanzados | *(Vacío)* |
| 12 | `sentencia-while-true-avanzado` | `while-true-avanzado` | While True: Menús Interactivos | `4` |
| 13 | `sentencia-control-break-continue` | `control-break-continue` | Modificadores Break y Continue | *(Vacío)* |
| 14 | `sentencia-bucles-anidados` | `bucles-anidados` | Bucles Anidados (Complejidad) | *(Vacío)* |
| 15 | `sentencia-arreglos` | `arreglos` | Arreglos y Listas | *(Vacío)* |
| 16 | `sentencia-listas-crud` | `listas-crud` | CRUD en Listas Dinámicas | *(Vacío)* |
| 17 | `sentencia-listas-procesos-comunes` | `listas-procesos-comunes` | Operaciones y Métodos Comunes | *(Vacío)* |
| 18 | `sentencia-manejo-archivos` | `manejo-archivos` | Archivos TXT y CSV | *(Vacío)* |
| 19 | `sentencia-funciones-python` | `funciones-python` | Modularidad con Funciones | *(Vacío)* |
| 20 | `sentencia-1` | `1` | Ensayo Aplicado | `6` |
