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

    # --- MODULE IP (OK) ---
    if scan_type == "ip":
        r = requests.get(f"http://ip-api.com/json/{target}")
        res = r.json()
        if res.get('status') == 'success':
            return jsonify({"status": "success", "data": f"📍 PAYS : {res.get('country')}\n🏙️ VILLE : {res.get('city')}\n🌐 FAI : {res.get('isp')}"})

    # --- MODULE RÉSEAUX SOCIAUX (SHERLOCK LITE) ---
    elif scan_type == "social":
        networks = {
            "Instagram": f"https://www.instagram.com/{target}/",
            "TikTok": f"https://www.tiktok.com/@{target}",
            "Twitter (X)": f"https://twitter.com/{target}",
            "GitHub": f"https://github.com/{target}",
            "YouTube": f"https://www.youtube.com/@{target}",
            "Twitch": f"https://www.twitch.tv/{target}",
            "Pinterest": f"https://www.pinterest.com/{target}/"
        }
        
        found = []
        headers = {'User-Agent': 'Mozilla/5.0'} # Pour éviter d'être bloqué

        for name, url in networks.items():
            try:
                # On vérifie juste si la page répond (status 200)
                r = requests.get(url, headers=headers, timeout=2)
                if r.status_code == 200:
                    found.append(f"✅ {name} : {url}")
                else:
                    found.append(f"❌ {name} : Introuvable")
            except:
                found.append(f"⚠️ {name} : Erreur de connexion")

        result_text = "🔍 RECHERCHE PSEUDO : " + target + "\n\n" + "\n".join(found)
        return jsonify({"status": "success", "data": result_text})

    return jsonify({"status": "error", "message": "Type inconnu."})

if __name__ == '__main__':
    app.run(debug=True)
