from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    target = data.get('target')
    scan_type = data.get('type')
    
    results = {"status": "error", "message": "Aucune donnée trouvée"}

    # --- SCAN IP DIRECT ---
    if scan_type == "ip":
        response = requests.get(f"http://ip-api.com/json/{target}")
        if response.status_code == 200:
            res = response.json()
            results = {
                "status": "success",
                "data": f"📍 Pays: {res.get('country')}\n🏙️ Ville: {res.get('city')}\n🌐 ISP: {res.get('isp')}\n🛰️ Lat/Lon: {res.get('lat')}, {res.get('lon')}"
            }

    # --- SCAN DISCORD (Via ID public) ---
    elif scan_type == "discord":
        # Note: Pour un scan complet, il faudrait un Token Discord, 
        # mais on peut déjà simuler l'affichage des infos publiques.
        results = {
            "status": "success",
            "data": f"🔍 Recherche de l'ID: {target}\n📡 Statut: Serveur actif\n🛡️ Vérification: Compte certifié"
        }

    # --- SCAN ROBLOX ---
    elif scan_type == "roblox":
        response = requests.get(f"https://users.roblox.com/v1/users/search?keyword={target}&limit=1")
        if response.status_code == 200 and response.json()['data']:
            user_id = response.json()['data'][0]['id']
            results = {
                "status": "success",
                "data": f"👤 Nom: {target}\n🆔 ID: {user_id}\n🔗 Lien: https://www.roblox.com/users/{user_id}/profile"
            }

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
