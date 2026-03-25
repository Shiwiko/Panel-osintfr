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

    # --- MODULE IP (MAX DATA) ---
    if scan_type == "ip":
        try:
            r = requests.get(f"http://ip-api.com/json/{target}?fields=16543743")
            res = r.json()
            if res.get('status') == 'success':
                info = (f"IP ADDRESS: {res.get('query')}\nCOUNTRY: {res.get('country')}\nCITY: {res.get('city')}\nISP: {res.get('isp')}\nLAT/LON: {res.get('lat')}, {res.get('lon')}\nVPN/PROXY: {res.get('proxy')}")
                return jsonify({"status": "success", "data": info})
            return jsonify({"status": "error", "message": "IP INTROUVABLE"})
        except: return jsonify({"status": "error", "message": "ERREUR API IP"})

    # --- MODULE USER TRACKING (SOCIAL SCAN) ---
    elif scan_type == "tracking":
        # Liste des plateformes à scanner
        sites = {
            "INSTAGRAM": f"https://www.instagram.com/{target}/",
            "TIKTOK": f"https://www.tiktok.com/@{target}",
            "TWITTER": f"https://twitter.com/{target}",
            "GITHUB": f"https://github.com/{target}",
            "TWITCH": f"https://www.twitch.tv/{target}",
            "PINTEREST": f"https://www.pinterest.com/{target}/",
            "ROBLOX": f"https://www.roblox.com/user.aspx?username={target}",
            "SNAPCHAT": f"https://www.snapchat.com/add/{target}"
        }
        
        found = []
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        for name, url in sites.items():
            try:
                # On check si la page répond 200 (OK)
                r = requests.get(url, headers=headers, timeout=1.5)
                if r.status_code == 200:
                    found.append(f"[+] FOUND: {name} -> {url}")
                else:
                    found.append(f"[-] NOT FOUND: {name}")
            except:
                found.append(f"[!] ERROR: {name} (BLOCKED)")

        res_text = f"USER_TRACKING_REPORT: {target}\n" + "\n".join(found)
        return jsonify({"status": "success", "data": res_text})

    # --- MODULE DISCORD ---
    elif scan_type == "discord":
        return jsonify({"status": "success", "data": f"USER ID: {target}\nLOOKUP: https://discordlookup.com/user/{target}"})

    return jsonify({"status": "error", "message": "MODULE INCONNU"})

if __name__ == '__main__':
    app.run(debug=True)
