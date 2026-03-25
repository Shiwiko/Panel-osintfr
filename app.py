from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# --- INTERFACE HTML (Intégrée) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>ULTIMATE OSINT PY</title>
    <style>
        :root { --neon: #00ff41; --bg: #050505; }
        body { background: var(--bg); color: var(--neon); font-family: 'Courier New', monospace; padding: 20px; }
        .container { max-width: 900px; margin: auto; border: 1px solid var(--neon); padding: 20px; box-shadow: 0 0 20px #00ff4133; }
        .input-group { display: flex; gap: 10px; margin-bottom: 30px; }
        input { flex: 1; background: #000; border: 1px solid var(--neon); color: #fff; padding: 15px; outline: none; }
        button { background: var(--neon); color: #000; border: none; padding: 15px 30px; cursor: pointer; font-weight: bold; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { border: 1px solid #333; padding: 15px; background: #111; border-radius: 5px; min-height: 200px; }
        h3 { border-bottom: 1px solid var(--neon); padding-bottom: 5px; font-size: 14px; color: #fff; }
        pre { color: #ccc; font-size: 11px; white-space: pre-wrap; word-wrap: break-word; overflow: auto; max-height: 300px; }
        .loading { color: yellow; font-style: italic; }
        a { color: cyan; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1 style="text-align:center">CORE_EXTRACTOR_OSINT</h1>
        <div class="input-group">
            <input type="text" id="target" placeholder="Pseudo Roblox, ID Discord, IP ou Email...">
            <button onclick="runScan()">LANCER LE SCAN</button>
        </div>
        <div class="grid">
            <div class="card"><h3>DISCORD (ID)</h3><pre id="ds-res">En attente...</pre></div>
            <div class="card"><h3>ROBLOX (Pseudo)</h3><pre id="rbx-res">En attente...</pre></div>
            <div class="card"><h3>IP TRACKER</h3><pre id="ip-res">En attente...</pre></div>
            <div class="card"><h3>EMAIL & LEAKS</h3><pre id="em-res">En attente...</pre></div>
        </div>
    </div>

    <script>
        async function runScan() {
            const val = document.getElementById('target').value;
            if(!val) return;
            document.querySelectorAll('pre').forEach(p => p.innerHTML = '<span class="loading">Extraction en cours...</span>');

            const res = await fetch('/scan', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({target: val})
            });
            const data = await res.json();

            document.getElementById('ds-res').innerHTML = JSON.stringify(data.discord, null, 2);
            document.getElementById('rbx-res').innerHTML = JSON.stringify(data.roblox, null, 2);
            document.getElementById('ip-res').innerHTML = JSON.stringify(data.ip, null, 2);
            document.getElementById('em-res').innerHTML = data.email ? `<a href="${data.email}" target="_blank">Vérifier fuites sur HIBP</a>` : "Aucun email détecté";
        }
    </script>
</body>
</html>
"""

# --- LOGIQUE DE SCAN ---

def get_discord(uid):
    if not uid.isdigit(): return "Nécessite un ID numérique"
    try:
        r = requests.get(f"https://discordlookup.mesalytic.moe/v1/user/{uid}", timeout=5)
        return r.json() if r.status_code == 200 else "Introuvable"
    except: return "Erreur de connexion"

def get_roblox(name):
    try:
        r = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [name]})
        data = r.json()
        if data.get('data'):
            uid = data['data'][0]['id']
            details = requests.get(f"https://users.roblox.com/v1/users/{uid}").json()
            return details
        return "Utilisateur inconnu"
    except: return "Erreur API Roblox"

# --- ROUTES ---

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/scan', methods=['POST'])
def scan():
    target = request.json.get('target', '').strip()
    is_ip = "." in target and not "@" in target
    
    return jsonify({
        "discord": get_discord(target),
        "roblox": get_roblox(target),
        "ip": requests.get(f"https://ipapi.co/{target}/json/").json() if is_ip else "Pas une IP",
        "email": f"https://haveibeenpwned.com/account/{target}" if "@" in target else None
    })

if __name__ == '__main__':
    app.run(debug=True)
