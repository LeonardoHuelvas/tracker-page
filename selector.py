import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

def track_package(tracking_number):
    """
    Rastrea un paquete utilizando el número de seguimiento proporcionado mediante la automatización de un navegador web.
    Utiliza Selenium para abrir el sitio web de seguimiento de contenedores, introduce el número de seguimiento
    en el formulario de búsqueda y obtiene los detalles del envío como ciudades de origen y destino.

    Parámetros:
    - tracking_number (str): El número de seguimiento del paquete a rastrear.

    Devuelve:
    - list: Una lista de cadenas que contiene los detalles de origen y destino del paquete.

    Lanza:
    - WebDriverException: Si ocurre un error relacionado con la interacción del navegador.
    - Exception: Para cualquier otro error general que pueda ocurrir durante la ejecución.
    """
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless")  # Enable headless mode for automation without a GUI.

    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        driver.get("https://www.searates.com/container/tracking")
        time.sleep(random.randint(2, 6))  # Wait randomly to simulate human interaction
        
        search_input = WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
        )
        search_input.click()
        search_input.send_keys(tracking_number)

        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        search_button.click()

        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.result-container"))
        )

        results = driver.find_elements(By.CSS_SELECTOR, "div.result-container div.detail-row")
        details = [result.text for result in results]
        return details

    except WebDriverException as e:
        print(f"Error interacting with the browser: {e}")
        driver.save_screenshot('error_screenshot.png')
        with open("error_page.html", "w", encoding='utf-8') as f:
            f.write(driver.page_source)
    except Exception as e:
        print(f"General error: {e}")
        driver.save_screenshot('error_screenshot.png')
        with open("error_page.html", "w", encoding='utf-8') as f:
            f.write(driver.page_source)
    finally:
        driver.quit()

# Example of function usage
if __name__ == "__main__":
    tracking_number = 'HLBU1043510'  # Replace with actual tracking number
    try:
        tracking_details = track_package(tracking_number)
        print(tracking_details)
    except Exception as e:
        print(f"Failed to track package: {e}")
