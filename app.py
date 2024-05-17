from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import uuid


app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

@app.route("/")
def start():
    """ Page d'accueil redirigée vers les actualités """
    return redirect(url_for('actualite'))

@app.route("/actualites")
def actualite():
    """ Afficher les actualités """
    dataActualites = read_json("actualites")
    dataCommentaire = read_json("commentaire")
    return render_template("actualites.html", data=dataActualites, commentaire=dataCommentaire, name="all")

@app.route("/authentification", methods=["GET", "POST"])
def authentification():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # Exemple simple d'authentification. À remplacer par votre logique.
        if email == "admin@example.com" and password == "password":
            session['user'] = email
            flash("Connexion réussie!", "success")
            return redirect(url_for('actualite'))
        else:
            flash("Invalid Credentials", "danger")
    return render_template('authentification.html')

@app.route("/logout")
def logout():
    session.pop('user', None)
    flash("Déconnexion réussie!", "success")
    return redirect(url_for('authentification'))

@app.route("/actualites/<name>")
def specific_actualite(name):
    """ Afficher les actualités par type """
    dataActualites = read_json("actualites")
    dataCommentaire = read_json("commentaire")
    return render_template("actualites.html", data=dataActualites, commentaire=dataCommentaire, name=name)

@app.route("/concert")
def concert():
    """ Afficher les concerts """
    dataActualites = read_json("concert")
    return render_template("concert.html", data=dataActualites)

@app.route("/commentaire", methods=["POST"])
def commentaire():
    """ Valider et écrire un commentaire """
    write_json("commentaire", {'actu': request.form['actu'], 'name': request.form['name'], 'commentaire': request.form['commentaire']})
    return redirect(url_for('actualite'))


@app.route("/Liste_Actu")
def Liste_Actu():
    """ Afficher les actualités sous forme de tableau """
    dataActualites = read_json("actualites")
    return render_template("Liste_Actu.html", actualites=dataActualites)

@app.route("/delete_actualite/<title>", methods=["POST"])
def delete_actualite(title):
    """ Supprimer une actualité """
    dataActualites = read_json("actualites")
    updated_dataActualites = [actualite for actualite in dataActualites if actualite['title'] != title]
    with open("actualites.json", "w") as f:
        json.dump(updated_dataActualites, f, indent=4)
    flash("Actualité supprimée avec succès!", "success")
    return redirect(url_for('liste_actu'))


@app.route("/liste_concerts")
def liste_concerts():
    """ Afficher la liste des concerts """
    dataConcerts = read_json("concert")
    return render_template("liste_concerts.html", concerts=dataConcerts)

@app.route("/delete_concert/<key>", methods=["POST"])
def delete_concert(key):
    """ Supprimer un concert """
    dataConcerts = read_json("concert")
    updated_dataConcerts = [concert for concert in dataConcerts if concert['key'] != key]
    with open("concert.json", "w") as f:
        json.dump(updated_dataConcerts, f, indent=4)
    flash("Concert supprimé avec succès!", "success")
    return redirect(url_for('liste_concerts'))



@app.route("/Ajoutactu", methods=["GET", "POST"])
def Ajoutactu():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        
        new_actualite = {
            'title': title,
            'content': content,
            'category': category
        }
        
        write_json("actualites", new_actualite)
        return redirect(url_for('actualite'))
    
    return render_template('Ajoutactu.html')

@app.route("/Ajoutconcert", methods=["GET", "POST"])
def Ajoutconcert():
    if request.method == "POST":
        dateConcert = request.form['Date']
        title = request.form['description']
        id = request.form['id']
        
        new_concert = {
            'title': title,
            'dateConcert': dateConcert,
            'id' : id,
        }
        
        write_json("concert", new_concert)
        return redirect(url_for('actualite'))
    
    return render_template('Ajoutconcert.html')

def read_json(name):
    """ Lire dans un fichier Json """
    with open(name + '.json') as f:
        data = json.load(f)
    return data

def write_json(name, data):
    """ Ecrire dans un fichier Json existant """
    dataFromFile = read_json(name)
    dataFromFile.append(data)
    with open(name + '.json', "w") as f:
        f.write(json.dumps(dataFromFile, indent=4))
    return data

if __name__ == "__main__":
    app.run(debug=True)
