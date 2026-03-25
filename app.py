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
        return jsonify({"status": "error", "message": "ERREUR : Cible vide."})

    # --- LOGIQUE IP ---
    if scan_type == "ip":
        try:
            r = requests.get(f"http://ip-api.com/json/{target}?fields=status,message,country,city,isp,org,as,query")
            res = r.json()
            if res['status'] == 'success':
                info = (f"📍 PAYS : {res.get('country')}\n"
                        f"🏙️ VILLE : {res.get('city')}\n"
                        f"🌐 FAI : {res.get('isp')}\n"
                        f"🏢 ORG : {res.get('org')}\n"
                        f"📡 IP : {res.get('query')}")
                return jsonify({"status": "success", "data": info})
            return jsonify({"status": "error", "message": "IP Introuvable."})
        except:
            return jsonify({"status": "error", "message": "Erreur de connexion API."})

    # --- LOGIQUE ROBLOX ---
    elif scan_type == "roblox":
        try:
            r = requests.get(f"https://users.roblox.com/v1/users/search?keyword={target}&limit=1")
            res = r.json()
            if res.get('data'):
                user = res['data'][0]
                u_id = user['id']
                # On récupère plus d'infos avec l'ID
                r2 = requests.get(f"https://users.roblox.com/v1/users/{u_id}")
                res2 = r2.json()
                info = (f"👤 PSEUDO : {res2.get('name')}\n"
                        f"🆔 ID : {u_id}\n"
                        f"📝 BIO : {res2.get('description')[:50]}...\n"
                        f"📅 CRÉATION : {res2.get('created')[:10]}")
                return jsonify({"status": "success", "data": info})
            return jsonify({"status": "error", "message": "Utilisateur introuvable."})
        except:
            return jsonify({"status": "error", "message": "Erreur API Roblox."})

    return jsonify({"status": "error", "message": "Type de scan inconnu."})

if __name__ == '__main__':
    app.run(debug=True)
