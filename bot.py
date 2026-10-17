import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Identifica a pasta correta se for .exe ou script normal
if getattr(sys, 'frozen', False):
    diretorio_atual = os.path.dirname(sys.executable)
else:
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

pasta_perfil = os.path.join(diretorio_atual, "whatsapp_session")

options = Options()
options.add_argument(f"--user-data-dir={pasta_perfil}")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-gpu")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://web.whatsapp.com")

print("Aguardando carregamento inicial...")
time.sleep(15)
print("Robo ativado e monitorando conversas!")

LINK_HOTMART = "https://seulinkdaqui.hotmart.com"

RESPOSTAS = {
    "prf": f"Ola! Que excelente escolha focar na PRF Administrativa. Nosso cronograma cobre todo o edital de forma mastigada. Para ver os modulos e garantir a sua vaga, acesse aqui: {LINK_HOTMART}",
    "curso": f"O metodo Fenix para a PRF Administrativa tem videoaulas, resumos em PDF e simulados semanais. Veja os detalhes: {LINK_HOTMART}",
    "valor": f"O curso completo esta com valor promocional por tempo limitado. Confira as condicoes no link oficial: {LINK_HOTMART}"
}

ultima_resposta_enviada = ""

def responder_mensagem():
    global ultima_resposta_enviada
    try:
        nao_lidas = driver.find_elements(By.CSS_SELECTOR, "span[aria-label*='nao lida'], span[aria-label*='não lida'], span[aria-label*='unread']")
        
        if nao_lidas:
            print("Nova mensagem detectada! Abrindo conversa...")
            nao_lidas[0].click()
            
            wait = WebDriverWait(driver, 10)
            caixa_texto = wait.until(
                EC.presence_of_element_located((By.XPATH, '//footer//div[@contenteditable="true"]'))
            )
            
            time.sleep(2)
            
            textos_recebidos = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]//span[contains(@class, "selectable-text")]')
            
            ultima_msg = ""
            if textos_recebidos:
                ultima_msg = textos_recebidos[-1].text.lower()
            else:
                mensagens_gerais = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
                if mensagens_gerais:
                    ultima_msg = mensagens_gerais[-1].text.lower()
                    
            print(f"Texto lido pelo robo: '{ultima_msg}'")
            
            resposta_escolhida = None
            for chave in RESPOSTAS:
                if chave in ultima_msg:
                    resposta_escolhida = RESPOSTAS[chave]
                    break
            
            if not resposta_escolhida:
                resposta_escolhida = (
                    "Ola! Sou a assistente virtual. Digite *PRF* para conhecer o cronograma, "
                    "*CURSO* para ver o conteudo ou *VALOR* para consultar a inscricao."
                )
            
            print("Digitando resposta...")
            time.sleep(2)
            
            caixa_texto.click()
            time.sleep(1)
            caixa_texto.send_keys(resposta_escolhida)
            time.sleep(1)
            caixa_texto.send_keys(Keys.ENTER)
            
            print("--> Resposta enviada com sucesso!")
            time.sleep(4)
            
    except Exception as e:
        print(f"Status/Aviso: {e}")

while True:
    responder_mensagem()
    time.sleep(3)