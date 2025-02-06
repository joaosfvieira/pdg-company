from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

#from webdriver_manager.chrome import ChromeDriverManager
import orjson
import time
import os

def iniciar_driver():
    api_token = os.getenv("BROWSERLESS_API_TOKEN")

    if not api_token:
        api_token = "RiwbM78mAwsQBr92c2cee3399fb89b349138a5b578"
        #raise ValueError("BROWSERLESS_API_TOKEN is not set")

    # Construct the URL dynamically
    #selenium_endpoint = f"https://{api_token}@chrome.browserless.io/webdriver"

    browserless_url = "https://chrome.browserless.io/webdriver"

    """Inicializa o WebDriver do Chrome em modo headless."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa sem interface gráfica
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")


    # Set the API token as a capability
    chrome_options.set_capability("browserless:token", api_token)

    driver = webdriver.Remote(
        command_executor=browserless_url,
        options=chrome_options  # ✅ Replacing deprecated desired_capabilities
    )

    return driver

# RiwbM78mAwsQBr92c2cee3399fb89b349138a5b578

def executar_scraper():
    start_time = datetime.now()
    """Executa o processo de scraping no site da Zenit Games."""
    driver = iniciar_driver()

    try:
        # Acessa a página de login
        driver.get("https://zenit.games/priston/login.php")
        #time.sleep(1)

        end_time = datetime.now()
        elapsed_time = end_time - start_time

        print(f"Página Login Carregada - {elapsed_time}")


        # Preenche os campos de login e submete o formulário
        driver.find_element(By.ID, "email").send_keys("lutadorpriston382@gmail.com")
        driver.find_element(By.ID, "c2").send_keys("ywt7wYWT7W@" + Keys.RETURN)

        #time.sleep(2)
        end_time = datetime.now()
        elapsed_time = end_time - start_time

        print(f"Logado - {elapsed_time}")

        # Acessa a página do clã
        driver.get("https://zenit.games/priston/clan.php")
        #time.sleep(1)
        end_time = datetime.now()
        elapsed_time = end_time - start_time

        print(f"Meu Clã - {elapsed_time}")

        # Encontra o menu suspenso e seleciona o clã
        select_element = driver.find_element(By.TAG_NAME, "select")
        select = Select(select_element)
        select.select_by_value("43;8")

        option_element = driver.find_element(By.XPATH, "//option[@value='43;8']")
        driver.execute_script("arguments[0].click();", option_element)
        #time.sleep(1)
        end_time = datetime.now()
        elapsed_time = end_time - start_time

        print(f"Pardal Gaming - {elapsed_time}")

        # Lista para armazenar os dados dos jogadores
        jogadores = []

        def extrair_dados_jogador(linha):
            return {
                "posicao": linha.find_element(By.CLASS_NAME, "membroPosicao").text,
                "nome": linha.find_element(By.CLASS_NAME, "membroNome").text,
                "classe": linha.find_element(By.CLASS_NAME, "membroClasse").text,
                "lvl": linha.find_element(By.CLASS_NAME, "membroLvl").text,
                "desde": linha.find_element(By.CLASS_NAME, "membroDesde").text
            }

        # Captura todas as linhas de jogadores do clã
        linhas_clan = driver.find_elements(By.XPATH, "//div[contains(@class, 'clanLinha')]")

        # Processa as linhas em paralelo
        with ThreadPoolExecutor() as executor:
            jogadores = list(executor.map(extrair_dados_jogador, linhas_clan))

        # Salvar JSON sem indentação para mais velocidade
        with open("jogadores.json", "wb") as file:
            file.write(orjson.dumps(jogadores, option=orjson.OPT_INDENT_2))


        print("Arquivo jogadores.json salvo com sucesso!")

    finally:
        driver.quit()  # Fecha o navegador

        end_time = datetime.now()
        elapsed_time = end_time - start_time

        print(f"Execution Time: {elapsed_time}")


if __name__ == "__main__":
    executar_scraper()
