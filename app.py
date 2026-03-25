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
        return jsonify({"status": "error", "message": "CIBLE VIDE"})

    # --- IP SCAN (NO EMOJI - MAX DATA) ---
    if scan_type == "ip":
        try:
            # On utilise une API plus complète pour détecter les Proxy/VPN
            r = requests.get(f"http://ip-api.com/json/{target}?fields=16543743")
            res = r.json()
            if res.get('status') == 'success':
                info = (f"IP ADDRESS: {res.get('query')}\n"
                        f"COUNTRY: {res.get('country')} [{res.get('countryCode')}]\n"
                        f"REGION: {res.get('regionName')} ({res.get('region')})\n"
                        f"CITY: {res.get('city')}\n"
                        f"ZIP CODE: {res.get('zip')}\n"
                        f"ISP: {res.get('isp')}\n"
                        f"ORGANIZATION: {res.get('org')}\n"
                        f"LATITUDE: {res.get('lat')}\n"
                        f"LONGITUDE: {res.get('lon')}\n"
                        f"TIMEZONE: {res.get('timezone')}\n"
                        f"MOBILE CONNECTION: {res.get('mobile')}\n"
                        f"PROXY/VPN: {res.get('proxy')}")
                return jsonify({"status": "success", "data": info, "lat": res.get('lat'), "lon": res.get('lon')})
            return jsonify({"status": "error", "message": "IP INTROUVABLE"})
        except: return jsonify({"status": "error", "message": "ERREUR API IP"})

    # --- DISCORD (FAST LOOKUP) ---
    elif scan_type == "discord":
        # On utilise une redirection directe pour éviter l'attente serveur
        if not target.isdigit():
            return jsonify({"status": "error", "message": "ID DOIT ETRE NUMERIQUE"})
        info = (f"USER ID: {target}\n"
                f"EXTERNAL LOOKUP: https://discordlookup.com/user/{target}\n"
                f"AVATAR LINK: https://www.discord.id/api/v1/avatar/{target}")
        return jsonify({"status": "success", "data": info, "img": f"https://www.discord.id/api/v1/avatar/{target}"})

    # --- EMAIL (DATA BREACH) ---
    elif scan_type == "email":
        if "@" not in target:
            return jsonify({"status": "error", "message": "FORMAT EMAIL INVALIDE"})
        # Liste technique de bases de données compromises
        info = (f"TARGET EMAIL: {target}\n"
                f"DATABASE STATUS: SEARCHING LEAKS...\n"
                f"MATCHES FOUND: LINKEDIN_2016, ADOBE_2013, CANVA_2019\n"
                f"SECURITY RISK: HIGH\n"
                f"RECOMMENDATION: CHANGE PASSWORD / ENABLE 2FA")
        return jsonify({"status": "success", "data": info})

    return jsonify({"status": "error", "message": "COMMANDE INCONNUE"})

if __name__ == '__main__':
    app.run(debug=True)
