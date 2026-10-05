import json
import os
import shutil
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

# Lista de módulos del curso con sus correspondientes slugs, nombres y datos de entrada (STDIN)
modulos_curso = [
    ("sentencia-que-es-python", "que-es-python", "¿Qué es Python?", ""),
    ("sentencia-variables-print", "variables-print", "Variables y Comando Print", ""),
    ("sentencia-ideacion-importancia", "ideacion-importancia", "Ideación e Importancia", ""),
    ("sentencia-entrada-salida", "entrada-salida", "Entrada y Salida de Datos", "Estudiante Python"),
    ("sentencia-importancia-indentacion", "importancia-indentacion", "Importancia de la Indentación", ""),
    ("sentencia-if-elif-else-avanzado", "if-elif-else-avanzado", "Estructuras if / elif / else", ""),
    ("sentencia-try-except", "try-except", "Gestión de Errores (try / except)", ""),
    ("sentencia-while-loop-basico", "while-loop-basico", "While: Fundamentos y Contadores", ""),
    ("sentencia-while-loop-condicional", "while-loop-condicional", "While: Control por Banderas", "25"),
    ("sentencia-for-loop-listas", "for-loop-listas", "For: Recorrido de Colecciones", ""),
    ("sentencia-for-range-completo", "for-range-completo", "For con Range: Rangos Avanzados", ""),
    ("sentencia-while-true-avanzado", "while-true-avanzado", "While True: Menús Interactivos", "4"),
    ("sentencia-control-break-continue", "control-break-continue", "Modificadores Break y Continue", ""),
    ("sentencia-bucles-anidados", "bucles-anidados", "Bucles Anidados (Complejidad)", ""),
    ("sentencia-arreglos", "arreglos", "Arreglos y Listas", ""),
    ("sentencia-listas-crud", "listas-crud", "CRUD en Listas Dinámicas", ""),
    ("sentencia-listas-procesos-comunes", "listas-procesos-comunes", "Operaciones y Métodos Comunes", ""),
    ("sentencia-manejo-archivos", "manejo-archivos", "Archivos TXT y CSV", ""),
    ("sentencia-funciones-python", "funciones-python", "Modularidad con Funciones", ""),
    ("sentencia-1", "1", "Ensayo Aplicado", "6")
]


def ejecutar_bot_curso(url="https://mantistcy.cl/aprenderpython/", guardar_archivo_log=True):
    inicio_ejecucion = datetime.now()
    t_inicio = time.time()
    total_modulos = len(modulos_curso)

    log_ejecucion = {
        "fecha_inicio": inicio_ejecucion.isoformat(),
        "fecha_fin": None,
        "duracion_segundos": 0.0,
        "estado_general": "INICIADO",
        "plataforma_url": url,
        "modo_ejecucion": "headless (servidor Linux TTY)",
        "cobertura": {
            "total_modulos": total_modulos,
            "modulos_exitosos": 0,
            "modulos_fallidos": 0,
            "porcentaje_cobertura": 0.0
        },
        "detalle_modulos": [],
        "archivo_log": None,
        "error": None
    }

    # 1. Configurar modo headless para servidor TTY (sin interfaz gráfica)
    options = Options()
    options.add_argument("-headless")
    # Recomendado en servidores Linux sin aceleración de GPU
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Configuración de ruta de geckodriver (compatible con /usr/local/bin y PATH local)
    gecko_path = "/usr/local/bin/geckodriver"

    service = Service(executable_path=gecko_path) if (gecko_path and os.path.isfile(gecko_path)) else Service()

    driver = None
    try:
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_window_size(1280, 900)

        driver.get(url)

        main_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "main-content"))
        )

        if not main_content:
            raise RuntimeError("No se pudo acceder al contenedor principal del curso.")

        modulos_exitosos = 0
        modulos_fallidos = 0

        for modulo_id, slug, nombre_modulo, input_data in modulos_curso:
            t_mod_inicio = time.time()
            detalle = {
                "modulo_id": modulo_id,
                "slug": slug,
                "nombre": nombre_modulo,
                "input_data": input_data,
                "estado": "pendiente",
                "duracion_segundos": 0.0,
                "error": None
            }

            try:
                # Navegar por el menú lateral si existe el enlace
                try:
                    link_menu = driver.find_element(
                        By.XPATH, f"//nav[contains(@class, 'github-sidebar')]//a[@href='#{modulo_id}']"
                    )
                    driver.execute_script("arguments[0].click();", link_menu)
                except NoSuchElementException:
                    pass

                # Desplazar la vista al artículo del módulo
                articulo = driver.find_element(By.ID, modulo_id)
                driver.execute_script("arguments[0].scrollIntoView(true);", articulo)

                # Si el ejercicio requiere entrada estándar (STDIN), ingresarla
                if input_data:
                    input_field = driver.find_element(By.ID, f"user-param-{slug}")
                    input_field.clear()
                    input_field.send_keys(input_data)

                # Presionar el botón para compilar y ejecutar el código del módulo
                boton_ejecutar = driver.find_element(By.XPATH, f"//button[@data-slug='{slug}']")
                driver.execute_script("arguments[0].click();", boton_ejecutar)

                # Esperar a que la consola del módulo responda
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, f"console-{slug}"))
                )

                detalle["estado"] = "exitoso"
                modulos_exitosos += 1
                time.sleep(0.5)

            except Exception as e_mod:
                detalle["estado"] = "fallido"
                detalle["error"] = str(e_mod)
                modulos_fallidos += 1

            finally:
                detalle["duracion_segundos"] = round(time.time() - t_mod_inicio, 2)
                log_ejecucion["detalle_modulos"].append(detalle)

        # Cálculo de cobertura alcanzada
        porcentaje = round((modulos_exitosos / total_modulos) * 100, 2)
        log_ejecucion["cobertura"]["modulos_exitosos"] = modulos_exitosos
        log_ejecucion["cobertura"]["modulos_fallidos"] = modulos_fallidos
        log_ejecucion["cobertura"]["porcentaje_cobertura"] = porcentaje

        if modulos_exitosos == total_modulos:
            log_ejecucion["estado_general"] = "COMPLETADO"
        elif modulos_exitosos > 0:
            log_ejecucion["estado_general"] = "PARCIAL"
        else:
            log_ejecucion["estado_general"] = "FALLIDO"

    except Exception as e:
        log_ejecucion["estado_general"] = "ERROR"
        log_ejecucion["error"] = str(e)

    finally:
        fin_ejecucion = datetime.now()
        log_ejecucion["fecha_fin"] = fin_ejecucion.isoformat()
        log_ejecucion["duracion_segundos"] = round(time.time() - t_inicio, 2)

        if driver:
            try:
                driver.quit()
            except Exception:
                pass

        # Guardar archivo de log en disco
        if guardar_archivo_log:
            try:
                dir_actual = os.path.dirname(os.path.abspath(__file__))
                dir_logs = os.path.join(dir_actual, "logs")
                os.makedirs(dir_logs, exist_ok=True)
                nombre_archivo = f"log_ejecucion_{inicio_ejecucion.strftime('%Y%m%d_%H%M%S')}.json"
                ruta_completa = os.path.join(dir_logs, nombre_archivo)
                with open(ruta_completa, "w", encoding="utf-8") as f:
                    json.dump(log_ejecucion, f, indent=2, ensure_ascii=False)
                log_ejecucion["archivo_log"] = ruta_completa
            except Exception as e_log:
                log_ejecucion["error_guardado_log"] = str(e_log)

    return log_ejecucion


if __name__ == "__main__":
    # Imprimir resultado limpio en formato JSON (capturable por n8n o procesos Linux)
    resultado = ejecutar_bot_curso()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
