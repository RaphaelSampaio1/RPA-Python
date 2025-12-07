from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def iniciar_driver():
    chrome_options = Options()

    arguments = [
        "lang=pt-BR",
        "--start-maximized",
        "disable-notifications",
        "--disable-infobars",
        "--disable-blink-features=AutomationControlled",
        "--enable-logging",
        "--disable-backgrounding-occluded-windows"
    ]

    for arg in arguments:
        chrome_options.add_argument(arg)

    driver = webdriver.Chrome(options=chrome_options)
    return driver

driver = iniciar_driver()
driver.get("https://cursoautomacao.netlify.app/")


h1_text = driver.find_element(By.XPATH,"//*[text()='Brasil']")
if h1_text is not None:
    print("Elemento encontrado pelo texto.")   


input('')