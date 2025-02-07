from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import orjson
import time
import os

def iniciar_driver():
    """Inicializa o WebDriver do Chrome em modo headless."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa sem interface gráfica
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def executar_scraper():
    start_time = datetime.now()
    driver = iniciar_driver()
    
    try:
        driver.get("https://zenit.games/priston/login.php")
        print(f"Página Login Carregada - {datetime.now() - start_time}")

        driver.find_element(By.ID, "email").send_keys("lutadorpriston382@gmail.com")
        driver.find_element(By.ID, "c2").send_keys("ywt7wYWT7W@" + Keys.RETURN)
        print(f"Logado - {datetime.now() - start_time}")
        
        driver.get("https://zenit.games/priston/clan.php")
        print(f"Meu Clã - {datetime.now() - start_time}")

        select_element = driver.find_element(By.TAG_NAME, "select")
        select = Select(select_element)
        select.select_by_value("43;8")
        
        option_element = driver.find_element(By.XPATH, "//option[@value='43;8']")
        driver.execute_script("arguments[0].click();", option_element)
        print(f"Pardal Gaming - {datetime.now() - start_time}")

        jogadores = []

        def extrair_dados_jogador(linha):
            return {
                "posicao": linha.find_element(By.CLASS_NAME, "membroPosicao").text,
                "nome": linha.find_element(By.CLASS_NAME, "membroNome").text,
                "classe": linha.find_element(By.CLASS_NAME, "membroClasse").text,
                "lvl": linha.find_element(By.CLASS_NAME, "membroLvl").text,
                "desde": linha.find_element(By.CLASS_NAME, "membroDesde").text
            }

        linhas_clan = driver.find_elements(By.XPATH, "//div[contains(@class, 'clanLinha')]")
        
        with ThreadPoolExecutor() as executor:
            jogadores = list(executor.map(extrair_dados_jogador, linhas_clan))

        with open("jogadores.json", "wb") as file:
            file.write(orjson.dumps(jogadores, option=orjson.OPT_INDENT_2))
        
        print("Arquivo jogadores.json salvo com sucesso!")

    finally:
        driver.quit()
        print(f"Execution Time: {datetime.now() - start_time}")

if __name__ == "__main__":
    executar_scraper()
