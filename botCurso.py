from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
import os
import time

options = Options()

driver = webdriver.Firefox(options=options)

driver.set_window_size(1280, 900)

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

try:
    driver.get(f"https://mantistcy.cl/aprenderpython/")

    main_content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "main-content"))
    )

    if main_content:
        print("Ingreso correcto a la plataforma del curso")
        print("Iniciando realización automática de los módulos...\n")

        for modulo_id, slug, nombre_modulo, input_data in modulos_curso:
            print(f"Procesando módulo: {nombre_modulo}")

            try:
                link_menu = driver.find_element(
                    By.XPATH, f"//nav[contains(@class, 'github-sidebar')]//a[@href='#{modulo_id}']"
                )
                driver.execute_script("arguments[0].click();", link_menu)
            except NoSuchElementException:
                print(f"Modulo: {modulo_id} no encontrado")
                pass

            # Desplazar la vista al artículo del módulo
            articulo = driver.find_element(By.ID, modulo_id)
            driver.execute_script("arguments[0].scrollIntoView(true);", articulo)

            if input_data:
                input_field = driver.find_element(By.ID, f"user-param-{slug}")
                input_field.clear()
                input_field.send_keys(input_data)
                print(f"  -> Datos de entrada (STDIN) ingresados: '{input_data}'")

            # Presionar el botón para compilar y ejecutar el código del módulo
            boton_ejecutar = driver.find_element(By.XPATH, f"//button[@data-slug='{slug}']")
            driver.execute_script("arguments[0].click();", boton_ejecutar)

            # Esperar a que la consola del módulo responda
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, f"console-{slug}"))
            )

            print(f"  -> Módulo '{nombre_modulo}' completado exitosamente.\n")
            time.sleep(1)

        print("Curso completado.")
        time.sleep(3)
    else:
        print("No se pudo acceder al contenido del curso.")
        time.sleep(3)

except NoSuchElementException:
    print("Elemento no encontrado")

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
