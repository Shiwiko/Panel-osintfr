from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    target = data.get('target', '').strip()
    scan_type = data.get('type')

    if not target:
        return jsonify({"status": "error", "message": "Cible vide."})

    # --- IP DEEP SCAN ---
    if scan_type == "ip":
        r = requests.get(f"http://ip-api.com/json/{target}?fields=66846719")
        res = r.json()
        if res.get('status') == 'success':
            return jsonify({"status": "success", "data": f"📍 PAYS : {res.get('country')}\n🏙️ VILLE : {res.get('city')}\n📮 CODE POSTAL : {res.get('zip')}\n📡 FAI : {res.get('isp')}\n🗺️ GPS : {res.get('lat')}, {res.get('lon')}\n⏰ TIMEZONE : {res.get('timezone')}"})
        return jsonify({"status": "error", "message": "IP introuvable."})

    # --- TRACKING USER (SOCIALS) ---
    elif scan_type == "tracking":
        networks = {"GitHub": f"https://github.com/{target}", "Twitch": f"https://www.twitch.tv/{target}", "Pinterest": f"https://www.pinterest.com/{target}/", "Roblox": f"https://www.roblox.com/user.aspx?username={target}"}
        found = []
        for name, url in networks.items():
            try:
                if requests.get(url, timeout=2).status_code == 200:
                    found.append(f"✅ {name} : {url}")
            except: pass
        return jsonify({"status": "success", "data": "🔍 RÉSULTATS :\n" + ("\n".join(found) if found else "❌ Aucun compte public trouvé.")})

    # --- ROBLOX PSEUDO ---
    elif scan_type == "roblox":
        r = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [target]})
        if r.json().get('data'):
            u_id = r.json()['data'][0]['id']
            res2 = requests.get(f"https://users.roblox.com/v1/users/{u_id}").json()
            return jsonify({"status": "success", "data": f"👤 NOM : {res2.get('displayName')}\n🆔 ID : {u_id}\n📅 CRÉATION : {res2.get('created')[:10]}\n📝 BIO : {res2.get('description') or 'Vide'}"})
        return jsonify({"status": "error", "message": "Joueur introuvable."})

    # --- DISCORD ---
    elif scan_type == "discord":
        return jsonify({"status": "success", "data": f"🔍 ID : {target}\n🔗 VOIR : https://discordlookup.com/user/{target}"})

    return jsonify({"status": "error", "message": "Type inconnu."})

if __name__ == '__main__':
    app.run(debug=True)
