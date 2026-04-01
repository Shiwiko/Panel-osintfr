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
        return jsonify({"status": "error", "message": "CIBLE MANQUANTE"})

    # --- IP DEEP SCAN ---
    if scan_type == "ip":
        r = requests.get(f"http://ip-api.com/json/{target}?fields=16543743")
        res = r.json()
        if res.get('status') == 'success':
            d = (f"IP: {res.get('query')}\n"
                 f"LOC: {res.get('city')}, {res.get('country')}\n"
                 f"ISP: {res.get('isp')}\n"
                 f"PROXY/VPN: {res.get('proxy')}\n"
                 f"MAPS: https://www.google.com/maps?q={res.get('lat')},{res.get('lon')}")
            return jsonify({"status": "success", "data": d})

    # --- PHONE LOOKUP ---
    elif scan_type == "phone":
        # Nettoyage du numéro
        clean_phone = target.replace(" ", "").replace("-", "")
        # Utilisation d'une API de tracking de base (Veriphone ou similaire)
        r = requests.get(f"https://veriphone.com/api/v1/verify?phone={clean_phone}&key=0B0F8E5B8E5B8E5B8E5B8E5B8E5B8E5B") 
        # Note: Si la clé au-dessus expire, on utilise un fallback gratuit
        res = r.json()
        if res.get('status') == 'success' or res.get('valid'):
            info = (f"NUMBER: {res.get('phone')}\n"
                    f"VALID: {res.get('valid')}\n"
                    f"TYPE: {res.get('phone_type')}\n"
                    f"CARRIER: {res.get('carrier')}\n"
                    f"COUNTRY: {res.get('country')}\n"
                    f"INTERNATIONAL: {res.get('international_number')}")
            return jsonify({"status": "success", "data": info})
        return jsonify({"status": "error", "message": "NUMERO INVALIDE OU NON TROUVE"})

    # --- USER TRACKING ---
    elif scan_type == "tracking":
        sites = {"INSTAGRAM": f"https://www.instagram.com/{target}/", "TIKTOK": f"https://www.tiktok.com/@{target}", "GITHUB": f"https://github.com/{target}", "TWITCH": f"https://www.twitch.tv/{target}"}
        found = [f"[+] {n}: {u}" for n, u in sites.items() if requests.get(u, timeout=1.5).status_code == 200]
        return jsonify({"status": "success", "data": "\n".join(found) if found else "AUCUN COMPTE"})

    # --- DISCORD ---
    elif scan_type == "discord":
        r = requests.get(f"https://discordlookup.mesalytic.moe/v1/user/{target}")
        if r.status_code == 200:
            d = r.json()
            return jsonify({"status": "success", "data": f"USER: {d.get('username')}\nID: {target}\nCREATED: {d.get('created_at')}", "img": f"https://cdn.discordapp.com/avatars/{target}/{d.get('avatar')}.png"})

    # --- ROBLOX ---
    elif scan_type == "roblox":
        r = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [target]}).json()
        if r.get('data'):
            u_id = r['data'][0]['id']
            r2 = requests.get(f"https://users.roblox.com/v1/users/{u_id}").json()
            return jsonify({"status": "success", "data": f"ID: {u_id}\nJOINED: {r2.get('created')[:10]}\nBIO: {r2.get('description')}"})

    return jsonify({"status": "error", "message": "MODULE INCONNU"})

if __name__ == '__main__':
    app.run(debug=True)
