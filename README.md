
<p align="center">
  <img src="https://img.shields.io/badge/Version-10.0-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Language-Python-white?style=for-the-badge">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Termux-red?style=for-the-badge">
</p>

O **Fallen Angels Metadados** é uma ferramenta de captura de metadados e rastreio de conexões. Ao ser executado, o script gera um link de "isca" que, ao ser acessado pelo alvo, redireciona para uma página de erro **404 Not Found**, enquanto captura silenciosamente todas as informações técnicas do dispositivo.

---

## O que ele faz?

- 🛡️ **Filtro de IP Único:** Não polui seus logs. Se a mesma pessoa entrar 10 vezes, ela só aparece uma vez.
  
- 📱 **Detecção de Dispositivo:** Identifica se é iPhone, Android (com modelo), Windows ou Mac.
  
- 🗺️ **Geolocalização:** Captura Cidade, Estado, País e Coordenadas exatas.
  
- 🌐 **ISP & Rede:** Mostra o provedor de internet e se o alvo está usando VPN/Proxy.
  
- 📁 **Logs Automáticos:** Cria um arquivo `fallen_db.txt` com todas as capturas detalhadas.


---

## 🛠️ Requisitos

Antes de começar, você precisa ter instalado:
1. **Python 3.x**
2. **Node.js** (Necessário para o túnel Cloudflare)
3. **Pip** (Gerenciador de pacotes do Python)

---

## 📥 Instalação e Uso

### 💻 Windows
1. Baixe o repositório ou copie o código.
2. Abra o CMD na pasta do script e instale as bibliotecas:
   ```bash
   pip install flask requests colorama

Instale o Cloudflared (Túnel):
--
    npm install -g cloudflared

 clonar repositório:
-
    git clone https://github.com/jvxiteerdudu-rgb/Fallen.git

   abrir repositório:
   -
    cd nome-da-pasta

  executar o script:
  -
    python fallen.py

-----------------------------
## 📥 Instalação e Uso

📱 Termux
--
    pkg update && pkg upgrade -y
    
Instale as partes:
-
    pkg install python nodejs -y
    pip install flask requests colorama

Instale o Cloudflared:
-
    npm install -g cloudflared

clonar repositório:
-
    git clone https://github.com/jvxiteerdudu-rgb/Fallen.git

   abrir repositório:
   -
    cd nome-da-pasta

  executar o script:
  -
    python fallen.py
    

# 🖥️ Como Monitorar
Após rodar o roteiro, ele vai gerar um link como: https://xxxx-xxxx-xxxx.trycloudflare.com.

Link para o Alvo: Envie uma URL principal. Ele verá um erro 404.

Seu Painel: Acesse URL_GERADA/logsno seu navegador para ver quem caiu.
