import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.service import Service

# 1. Configurar modo headless para servidor TTY
options = Options()
options.add_argument("-headless")
# Recomendado en servidores Linux sin aceleración de GPU
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = Service(executable_path="/usr/local/bin/geckodriver")

driver = webdriver.Firefox(service=service, options=options)

usuarios = [
    ("Juaquin", "duoc@duoc.cl", "Valparaiso"),
    ("Pedro", "duoc@duoc.cl", "Valparaiso"),
    ("Juan", "duoc@duoc.cl", "Valparaiso"),
    ("Agustin", "duoc@duoc.cl", "Valparaiso"),
    ("Ricardo", "duoc@duoc.cl", "Valparaiso"),
]

resultado = []

try:
    driver.get(
        "https://fundacion-instituto-profesional-duoc-uc.github.io/ATY1102-MantenedorUsuarios/index.html"
    )

    usuario = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    usuario.send_keys("duoc")
    driver.find_element(By.ID, "password").send_keys("duoc123")
    driver.find_element(By.ID, "loginForm").submit()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dataForm"))
    )

    for nombre, correo, ciudad in usuarios:
        user_field = driver.find_element(By.ID, "nombre")
        user_field.clear()
        user_field.send_keys(nombre)

        email_field = driver.find_element(By.ID, "email")
        email_field.clear()
        email_field.send_keys(correo)

        ciudad_field = driver.find_element(By.ID, "ciudad")
        ciudad_field.clear()
        ciudad_field.send_keys(ciudad)

        driver.find_element(By.ID, "dataForm").submit()

    time.sleep(1)

    filas = driver.find_elements(By.XPATH, '//*[@id="dataTableBody"]/tr')
    for i, fila in enumerate(filas):
        celdas = fila.find_elements(By.TAG_NAME, "td")
        if len(celdas) >= 3:
            resultado.append(
                {
                    "nombre": celdas[0].text.strip(),
                    "email": celdas[1].text.strip(),
                    "ciudad": celdas[2].text.strip(),
                }
            )

    # Imprimir resultado limpio en formato JSON (útil para capturarlo en n8n)
    print(json.dumps(resultado))

except Exception as e:
    # Corrección: imprimir el error como string
    print(json.dumps({"error": str(e)}))
finally:
    driver.quit()

