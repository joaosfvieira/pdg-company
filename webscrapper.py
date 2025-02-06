from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time


def iniciar_driver():
    """Inicializa o WebDriver do Chrome em modo headless."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executa sem interface gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def executar_scraper():
    """Executa o processo de scraping no site da Zenit Games."""
    driver = iniciar_driver()

    try:
        # Acessa a página de login
        driver.get("https://zenit.games/priston/login.php")
        time.sleep(3)

        print("Página Login Carregada")

        # Preenche os campos de login e submete o formulário
        driver.find_element(By.ID, "email").send_keys("lutadorpriston382@gmail.com")
        driver.find_element(By.ID, "c2").send_keys("ywt7wYWT7W@" + Keys.RETURN)

        time.sleep(5)
        print("Logado")

        # Acessa a página do clã
        driver.get("https://zenit.games/priston/clan.php")
        time.sleep(3)
        print("Meu Clã")

        # Encontra o menu suspenso e seleciona o clã
        select_element = driver.find_element(By.TAG_NAME, "select")
        select = Select(select_element)
        select.select_by_value("43;8")

        option_element = driver.find_element(By.XPATH, "//option[@value='43;8']")
        driver.execute_script("arguments[0].click();", option_element)
        time.sleep(3)
        print("Pardal Gaming")

        # Lista para armazenar os dados dos jogadores
        jogadores = []

        # Captura todas as linhas de jogadores do clã
        linhas_clan = driver.find_elements(By.XPATH, "//div[contains(@class, 'clanLinha')]")

        for linha in linhas_clan:
            posicao = linha.find_element(By.CLASS_NAME, "membroPosicao").text
            nome = linha.find_element(By.CLASS_NAME, "membroNome").text
            classe = linha.find_element(By.CLASS_NAME, "membroClasse").text
            lvl = linha.find_element(By.CLASS_NAME, "membroLvl").text
            desde = linha.find_element(By.CLASS_NAME, "membroDesde").text

            jogadores.append({
                "posicao": posicao,
                "nome": nome,
                "classe": classe,
                "lvl": lvl,
                "desde": desde
            })

        # Salva os dados no arquivo jogadores.json
        with open("jogadores.json", "w", encoding="utf-8") as file:
            json.dump(jogadores, file, indent=4, ensure_ascii=False)

        print("Arquivo jogadores.json salvo com sucesso!")

    finally:
        driver.quit()  # Fecha o navegador


if __name__ == "__main__":
    executar_scraper()
