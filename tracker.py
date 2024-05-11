import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

def track_package(tracking_number):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false})")

    try:
        driver.get("https://www.searates.com/container/tracking")
        time.sleep(random.randint(2, 6))  # Simula interacción humana y espera que la página cargue

        # Espera que el input de búsqueda sea visible y lo utiliza
        search_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Container, Booking, Bill of lading']"))
        )
        search_input.click()
        search_input.clear()
        search_input.send_keys(tracking_number)
        search_input.send_keys(Keys.RETURN)

        # Espera que el botón de búsqueda sea clickeable y lo presiona
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.WTsBDL.DX8c49.en0Ha_.cewbX8"))
        )
        search_button.click()

        # Extrae los resultados de la búsqueda
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".result-class"))   
        )
        results = driver.find_elements(By.CSS_SELECTOR, ".result-class")   
        for result in results:
            print(result.text)

    except WebDriverException as e:
        print(f"Error al interactuar con el navegador: {e}")
        driver.save_screenshot('error_screenshot.png')
        raise

    finally:
        driver.quit()

if __name__ == "__main__":
    tracking_number = input("Ingrese el número de seguimiento: ")
    track_package(tracking_number)
