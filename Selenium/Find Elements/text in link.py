from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def iniciar_driver():
    chrome_options = Options()

    arguments = [
        "lang=pt-BR",
        "--start-maximized",
        "disable-notifications",
        "incognito",
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


link_name = driver.find_element(By.LINK_TEXT, "Desafios") # Localiza o link pelo texto visível
if link_name:
    print("Link encontrado pelo texto visível.")
else:
    print("Link não encontrado pelo texto visível.")


try_link_name = driver.find_element(By.PARTIAL_LINK_TEXT, "Des") # Localiza o link pelo texto parcial
if try_link_name:
    print("Link encontrado pelo texto parcial.")
else:
    print("Link não encontrado pelo texto parcial.")

input('')