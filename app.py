from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# --- INTERFACE VISUELLE (DESIGN NÉON) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TERMINAL OSINT FR v5.0</title>
    <style>
        :root { --neon: #00ff41; --bg: #050505; --card: #111; }
        body { background: var(--bg); color: var(--neon); font-family: 'Courier New', monospace; padding: 20px; margin: 0; }
        .wrapper { max-width: 1000px; margin: auto; border: 1px solid var(--neon); padding: 25px; box-shadow: 0 0 20px rgba(0,255,65,0.2); }
        h1 { text-align: center; letter-spacing: 5px; text-transform: uppercase; border-bottom: 2px solid var(--neon); padding-bottom: 10px; }
        .search-box { display: flex; gap: 10px; margin: 30px 0; }
        input { flex: 1; background: #000; border: 1px solid var(--neon); color: #fff; padding: 15px; font-size: 16px; outline: none; }
        button { background: var(--neon); color: #000; border: none; padding: 15px 30px; cursor: pointer; font-weight: bold; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 15px #fff; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: var(--card); border: 1px solid #333; padding: 20px; border-radius: 4px; position: relative; }
        .card h3 { margin-top: 0; font-size: 14px; color: #fff; border-bottom: 1px solid #333; padding-bottom: 10px; }
        pre { color: #00ff41; font-size: 12px; white-space: pre-wrap; word-wrap: break-word; overflow-y: auto; max-height: 250px; }
        .loading { color: orange; font-style: italic; }
        .footer { text-align: center; margin-top: 40px; font-size: 10px; opacity: 0.5; }
        a { color: cyan; text-decoration: none; }
    </style>
</head>
<body>
    <div class="wrapper">
        <h1>[ TERMINAL OSINT ]</h1>
        <div class="search-box">
            <input type="text" id="target" placeholder="Pseudo Roblox, ID Discord, IP ou Email...">
            <button onclick="runScan()">SCANNER LA CIBLE</button>
        </div>
        <div class="grid">
            <div class="card"><h3>🔵 DISCORD INTELLIGENCE</h3><pre id="ds-res">En attente d'ID...</pre></div>
            <div class="card"><h3>🔴 ROBLOX DATA</h3><pre id="rbx-res">En attente de pseudo...</pre></div>
            <div class="card"><h3>🌐 IP GEOLOCATION</h3><pre id="ip-res">En attente d'IP...</pre></div>
            <div class="card"><h3>📧 DATA LEAKS (EMAIL)</h3><pre id="em-res">En attente d'email...</pre></div>
        </div>
        <div class="footer">SHIWIKO OSINT TOOL - USAGE ÉDUCATIF UNIQUEMENT</div>
    </div>

    <script>
        async function runScan() {
            const val = document.getElementById('target').value.trim();
            if(!val) return;
            document.querySelectorAll('pre').forEach(p => p.innerHTML = '<span class="loading">[ RECHERCHE EN COURS... ]</span>');

            try {
                const response = await fetch('/scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target: val})
                });
                const data = await response.json();

                document.getElementById('ds-res').innerHTML = JSON.stringify(data.discord, null, 2);
                document.getElementById('rbx-res').innerHTML = JSON.stringify(data.roblox, null, 2);
                document.getElementById('ip-res').innerHTML = JSON.stringify(data.ip, null, 2);
                document.getElementById('em-res').innerHTML = data.email_link ? 
                    `Lien de fuite : <a href="${data.email_link}" target="_blank">Cliquez ici (HIBP)</a>` : "Aucune donnée email.";
            } catch(e) {
                alert("Erreur lors de la connexion au serveur.");
            }
        }
    </script>
</body>
</html>
"""

# --- LOGIQUE SERVEUR ---

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/scan', methods=['POST'])
def scan():
    target = request.json.get('target', '').strip()
    results = {"discord": "Non testé", "roblox": "Non trouvé", "ip": "Pas une IP", "email_link": None}

    # Discord (via API publique)
    if target.isdigit() and len(target) >= 17:
        try:
            r = requests.get(f"https://discordlookup.mesalytic.moe/v1/user/{target}")
            results['discord'] = r.json() if r.status_code == 200 else "Introuvable"
        except: pass

    # Roblox
    try:
        r_rbx = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [target]}).json()
        if r_rbx.get('data'):
            uid = r_rbx['data'][0]['id']
            results['roblox'] = requests.get(f"https://users.roblox.com/v1/users/{uid}").json()
    except: pass

    # IP Tracker
    if "." in target and not "@" in target:
        try:
            results['ip'] = requests.get(f"https://ipapi.co/{target}/json/").json()
        except: pass

    # Email
    if "@" in target:
        results['email_link'] = f"https://haveibeenpwned.com/account/{target}"

    return jsonify(results)

if __name__ == '__main__':
    app.run()
