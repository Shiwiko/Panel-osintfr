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

    # --- IP ---
    if scan_type == "ip":
        r = requests.get(f"http://ip-api.com/json/{target}")
        res = r.json()
        if res.get('status') == 'success':
            return jsonify({"status": "success", "data": f"📍 PAYS : {res.get('country')}\n🏙️ VILLE : {res.get('city')}\n🌐 FAI : {res.get('isp')}"})
        return jsonify({"status": "error", "message": "IP introuvable."})

    # --- DISCORD (Via API spécialisée) ---
    elif scan_type == "discord":
        try:
            # On utilise une API publique pour lookup les ID Discord
            r = requests.get(f"https://discord.id/api/v1/lookup?id={target}")
            res = r.json()
            if res.get('status') == 200:
                data = res.get('data', {})
                info = (f"👤 USERNAME : {data.get('username')}#{data.get('discriminator')}\n"
                        f"🆔 ID : {target}\n"
                        f"📅 CRÉATION : {data.get('created_at')}\n"
                        f"🤖 BOT : {'OUI' if data.get('bot') else 'NON'}")
                return jsonify({"status": "success", "data": info})
            return jsonify({"status": "error", "message": "ID Discord invalide ou non trouvé."})
        except:
            return jsonify({"status": "error", "message": "Erreur connexion API Discord."})

    # --- EMAIL (Simulation réaliste de fuites) ---
    elif scan_type == "email":
        return jsonify({"status": "success", "data": f"🔍 SCAN EMAIL : {target}\n✅ Aucune fuite majeure détectée dans les bases de données publiques.\n⚠️ Note : Ce scan est une simulation de sécurité."})

    return jsonify({"status": "error", "message": "Type de scan inconnu."})

if __name__ == '__main__':
    app.run(debug=True)
