from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import json
import time

def run_process():
    # Configurar o WebDriver (Chromium)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Se quiser rodar sem abrir o navegador
    driver = webdriver.Chrome(options=options)

    try:
        # Abrir o site
        driver.get("https://zenit.games/priston/login.php")
        # Aguardar a página carregar
        time.sleep(3)

        print("Página Login Carregada")

        # Localizar e preencher campos de login
        driver.find_element(By.ID, "email").send_keys("lutadorpriston382@gmail.com")
        driver.find_element(By.ID, "c2").send_keys("ywt7wYWT7W@" + Keys.RETURN)

        # Esperar login ser processado
        time.sleep(5)

        print("Logado")

        # Abrir o site
        driver.get("https://zenit.games/priston/login.php")
        # Aguardar a página carregar
        time.sleep(3)

        print("Página Clãs")

        driver.get("https://zenit.games/priston/clan.php")
        time.sleep(3)

        print("Meu Clã")

        # 1. Encontrar e clicar no <select> para abrir o menu suspenso
        select_element = driver.find_element(By.TAG_NAME, "select")
        select_element.click()
        time.sleep(1)  # Pequeno delay para garantir que as opções sejam carregadas

        # 2. Criar objeto Select e selecionar a opção desejada
        select = Select(select_element)
        select.select_by_value("43;8")

        # 3. Clicar na opção selecionada usando JavaScript
        option_element = driver.find_element(By.XPATH, "//option[@value='43;8']")
        driver.execute_script("arguments[0].click();", option_element)
        time.sleep(3)

        print("Pardal Gaming")

        # Lista para armazenar os dados dos jogadores
        jogadores = []

        # Localiza todas as divs de jogadores
        linhas_clan = driver.find_elements(By.XPATH, "//div[contains(@class, 'clanLinha')]")

        # Itera por cada linha de jogador e extrai os dados
        for linha in linhas_clan:
            posicao = linha.find_element(By.CLASS_NAME, "membroPosicao").text
            nome = linha.find_element(By.CLASS_NAME, "membroNome").text
            classe = linha.find_element(By.CLASS_NAME, "membroClasse").text
            lvl = linha.find_element(By.CLASS_NAME, "membroLvl").text
            desde = linha.find_element(By.CLASS_NAME, "membroDesde").text

            # Adiciona o jogador à lista como um dicionário
            jogador = {
                "posicao": posicao,
                "nome": nome,
                "classe": classe,
                "lvl": lvl,
                "desde": desde
            }
            jogadores.append(jogador)

        # Converte a lista para JSON e salva no arquivo jogadores.json
        with open("jogadores.json", "w", encoding="utf-8") as file:
            json.dump(jogadores, file, indent=4, ensure_ascii=False)

        print("Arquivo jogadores.json salvo com sucesso!")

    finally:
        driver.quit()  # Fechar o navegador

# Loop para repetir o processo a cada 1 hora (3600 segundos)
while True:
    run_process()  # Executar o processo
    print("Aguardando 1 hora para repetir o processo...")
    time.sleep(3600)  # Espera de 1 hora (3600 segundos) antes de repetir
