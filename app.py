@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    target = data.get('target', '').strip()
    scan_type = data.get('type')

    if not target:
        return jsonify({"status": "error", "message": "ERREUR : Cible vide."})

    # --- SCAN IP (OK) ---
    if scan_type == "ip":
        r = requests.get(f"http://ip-api.com/json/{target}")
        res = r.json()
        if res.get('status') == 'success':
            return jsonify({"status": "success", "data": f"📍 PAYS : {res.get('country')}\n🏙️ VILLE : {res.get('city')}\n🌐 FAI : {res.get('isp')}"})

    # --- SCAN ROBLOX (AMÉLIORÉ) ---
    elif scan_type == "roblox":
        # On cherche d'abord l'ID avec le pseudo
        r = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [target]})
        res = r.json()
        if res.get('data'):
            u_id = res['data'][0]['id']
            # On récupère les infos du profil
            r2 = requests.get(f"https://users.roblox.com/v1/users/{u_id}")
            res2 = r2.json()
            return jsonify({"status": "success", "data": f"👤 NOM : {res2.get('displayName')}\n🆔 ID : {u_id}\n📅 CRÉATION : {res2.get('created')[:10]}\n🔗 PROFIL : https://www.roblox.com/users/{u_id}/profile"})
        return jsonify({"status": "error", "message": "Joueur introuvable."})

    # --- SCAN DISCORD (LIEN DIRECT) ---
    elif scan_type == "discord":
        return jsonify({"status": "success", "data": f"🔍 RECHERCHE ID : {target}\n🔗 VOIR PROFIL : https://discord.com/users/{target}\n⚠️ Note : Discord nécessite un Token Bot pour plus d'infos."})

    return jsonify({"status": "error", "message": "Type inconnu."})
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
