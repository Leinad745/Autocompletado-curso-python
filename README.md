# Bot de Automatización de Curso Python (RPA)

Este proyecto corresponde a la **Evaluación 1 / Caso Semestral** de la asignatura **Automatización de Procesos Robóticos** (RPA).

Consiste en un bot en Python desarrollado con **Selenium WebDriver** diseñado para automatizar la navegación, ingreso de parámetros (STDIN) y ejecución secuencial de los 20 módulos interactivos del curso web de Python en [https://mantistcy.cl/aprenderpython/](https://mantistcy.cl/aprenderpython/).

---

## Descripción General

El script simula la interacción completa de un usuario en la plataforma educativa del curso. Automatiza de manera robótica las siguientes tareas:

1. **Inicio y Conexión**: Inicializa Mozilla Firefox y navega a la URL de la plataforma.
2. **Navegación Dinámica**: Selecciona cada módulo desde la barra de navegación lateral (`github-sidebar`).
3. **Desplazamiento (Scroll)**: Ajusta la vista del navegador hacia el elemento del módulo correspondiente (`scrollIntoView`).
4. **Entrada de Datos (STDIN)**: Detecta ejercicios interactivos que requieren entrada de usuario, limpia el campo e ingresa los valores prefijados.
5. **Compilación y Ejecución**: Dispara la ejecución del snippet de código del módulo mediante un clic JavaScript.
6. **Sincronización por Espera Explícita**: Aguarda a que el elemento de consola (`console-{slug}`) aparezca en pantalla confirmando la respuesta del servidor antes de avanzar al siguiente módulo.

---

## Tecnologías Utilizadas

- **Python 3.x**
- **Selenium WebDriver**: Automatización de navegadores web.
- **Mozilla Firefox & GeckoDriver**: Navegador y controlador automatizado.
- **WebDriverWait & Expected Conditions (`EC`)**: Sincronización asíncrona basada en eventos del DOM.
- **JavaScript Injection (`execute_script`)**: Clics e interacciones directas en elementos que evitan problemas de superposición.

---

## Requisitos Previos

- **Python 3.8+** instalado en el sistema.
- **Mozilla Firefox** instalado.
- **GeckoDriver** configurado en las variables de entorno o gestionado automáticamente por Selenium 4+.

---

## Instalación y Configuración

1. Clonar o ubicar la carpeta del proyecto en su entorno local.
2. Instalar las dependencias necesarias ejecutando:

```bash
pip install selenium
```
