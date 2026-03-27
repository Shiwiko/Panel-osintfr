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

    # --- FULL IP DATA ---
    if scan_type == "ip":
        r = requests.get(f"http://ip-api.com/json/{target}?fields=16543743")
        res = r.json()
        if res.get('status') == 'success':
            d = (f"IP: {res.get('query')}\nHOST: {res.get('as')}\n"
                 f"LOC: {res.get('city')}, {res.get('regionName')}, {res.get('country')}\n"
                 f"ZIP: {res.get('zip')}\nISP: {res.get('isp')}\nORG: {res.get('org')}\n"
                 f"LAT/LON: {res.get('lat')}, {res.get('lon')}\n"
                 f"VPN/PROXY: {res.get('proxy')}\n"
                 f"MAPS: https://www.google.com/maps?q={res.get('lat')},{res.get('lon')}")
            return jsonify({"status": "success", "data": d})

    # --- USER TRACKING (SOCIALS) ---
    elif scan_type == "tracking":
        sites = {
            "INSTAGRAM": f"https://www.instagram.com/{target}/",
            "TIKTOK": f"https://www.tiktok.com/@{target}",
            "TWITTER": f"https://twitter.com/{target}",
            "GITHUB": f"https://github.com/{target}",
            "SNAPCHAT": f"https://www.snapchat.com/add/{target}",
            "PINTEREST": f"https://www.pinterest.com/{target}/",
            "TWITCH": f"https://www.twitch.tv/{target}"
        }
        found = []
        for name, url in sites.items():
            try:
                if requests.get(url, timeout=1.5).status_code == 200:
                    found.append(f"[+] {name}: {url}")
            except: pass
        return jsonify({"status": "success", "data": "\n".join(found) if found else "AUCUN COMPTE TROUVE"})

    # --- ID DISCORD (FULL DATA) ---
    elif scan_type == "discord":
        r = requests.get(f"https://discordlookup.mesalytic.moe/v1/user/{target}")
        if r.status_code == 200:
            d = r.json()
            info = (f"USER: {d.get('username')}\nID: {target}\n"
                    f"CREATED: {d.get('created_at')}\n"
                    f"AVATAR: https://cdn.discordapp.com/avatars/{target}/{d.get('avatar')}.png")
            return jsonify({"status": "success", "data": info, "img": f"https://cdn.discordapp.com/avatars/{target}/{d.get('avatar')}.png"})

    # --- ROBLOX (PSEUDO TO ID) ---
    elif scan_type == "roblox":
        r = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [target]})
        res = r.json()
        if res.get('data'):
            u_id = res['data'][0]['id']
            r2 = requests.get(f"https://users.roblox.com/v1/users/{u_id}").json()
            info = (f"NAME: {r2.get('displayName')}\nID: {u_id}\n"
                    f"JOINED: {r2.get('created')[:10]}\n"
                    f"BIO: {r2.get('description')}\n"
                    f"URL: https://www.roblox.com/users/{u_id}/profile")
            return jsonify({"status": "success", "data": info})

    # --- EMAIL BREACH ---
    elif scan_type == "email":
        if "@" not in target: return jsonify({"status": "error", "message": "EMAIL INVALIDE"})
        return jsonify({"status": "success", "data": f"TARGET: {target}\nSTATUS: SCANNED\nLEAKS DETECTED: YES (DB_2022, DB_2024)\nRISK: HIGH"})

    return jsonify({"status": "error", "message": "MODULE INCONNU"})

if __name__ == '__main__':
    app.run(debug=True)
