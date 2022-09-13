# fonction principale
from flask import Flask, render_template, redirect, request, session
import random as random
from fonctions_annexes import * # faire plutot un import de chacune des fonctions annexes

app = Flask(__name__)

app.secret_key = "key"




@app.route('/')
def index(): 
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")



@app.route('/valid_login',methods = ['GET','POST'])

def valid_login() :
    if request.form['pwd'] == 'gsea': #mot de passe correct
        session['login'] = request.form['login']
        session["nbjoueur"]=-1
        return "Bienvenue "+ session['login'] +  render_template("index.html")

    else :
        return redirect('/login')


@app.route('/logout')
def logout() :
    session.pop('login', None)
# ou bien del session[‘login’]
    return "Vous êtes bien déconnecté"+  render_template("index.html")




@app.route('/jouer', methods = ['GET','POST'])
def yams():
    if 'login' in session : # on ne peut jouer que si on est connecté
        # initialisation nombre de joueurs
        if request.method =='GET':
            valeur_des = False
            n = request.args.get('nbjoueurs') # n est le nombre de joueurs
        else:
            n = request.form['nbjoueurs']
            n = int(n)
    
        # fin de l'initialisation nombre joueurs

        # initialisation score joueurs
            scores=[]
            for i in range(n):   # PROBLEME
                scores.append([0]*18)  # création d'une liste de joueurs contenant la liste de leurs scores (13) + 1 bonus + 3 totals + 1 total total
            session["scores"] = scores
        # création d'une liste contenant le score des joueurs, le joueur 1 a son score en SCORE [0]

        # boucle principale, les joueurs lancent les dés
            for tour in range(13): # il y a 13 tours en tout
                
                for joueur in range(n): # il y a n joueurs 
                    valeur_des = []
                    for de in range (5):
                        valeur_des.append(random.randint(1,6))
                    session["valeur_des"] = valeur_des
                    # 1 er lancer terminé

            
                    # on récupère la liste des itérations des dés à relancer
                    for id_de in request.form.getlist('choix des a changer'):# mettre 01234 dans velues
                        valeur_des = [id_de] = random.randint(1,6) # on relance ces dés
                    session["valeur_des"] = valeur_des
                    # 2 eme lancer terminé

                    # on récupère la liste des itérations des dés à relancer
                    for id_de in request.form.getlist('choix des a changer'):# mettre 01234 dans velues
                        valeur_des = [id_de] = random.randint(1,6) # on relance ces dés
                    session["valeur_des"] = valeur_des

                    # 3 eme lancer terminé

                   # choix d'une figure dans une liste déroulant
                    """figure = request.form['choix_figure']
                    session["choix_figure"] = 'choix figure'"""
                
                    figure = '1'
                    # utilisation des fonctions annexes pour calculer le score
                    # partie supérieure
                    if figure == '1':
                        scores[joueur][0]+= sup(valeur_des,1) # c'est le 1 er score de la liste du joueur ( ordre arbitraire choisi par moi )
                    elif figure == '2':
                        scores[joueur][1]+= sup(valeur_des,2)
                    elif figure == '3':
                        scores[joueur][2]+= sup(valeur_des,3)
                    elif figure == '4':
                        scores[joueur][3]+= sup(valeur_des,4)
                    elif figure == '5':
                        scores[joueur][4]+= sup(valeur_des,5)
                    elif figure == '6':
                        scores[joueur][5]+= sup(valeur_des,6)
                    # partie intermédiaire A FAIRE D ABORD DNS ANNEXES
                    elif figure == 'intermédiairesup':
                        scores[joueur][6]+= intermediaire(valeur_des)
                    elif figure == 'intermédiaireinf':
                        scores[joueur][7]+= intermediaire(valeur_des)
                    
                    # partie inférieure A FAIRE D'ABORD DANS ANNEXES
                    elif figure == 'carre':
                        scores[joueur][8]+= carre(valeur_des)
                    elif figure == 'full':
                        scores[joueur][9]+= full(valeur_des)
                    elif figure == 'petite suite':
                        scores[joueur][10]+= petitesuite(valeur_des)
                    elif figure == 'grande suite':
                        scores[joueur][11]+= grandesuite(valeur_des)
                    elif figure == 'yams':
                        scores[joueur][12]+= yams(valeur_des)
                    # actualiser le tableau  des scores
                    scores[joueur][13]+= total_partie_sup(scores,joueur) # total avec bonus de la partie 1 
                    scores[joueur][14]+=0 # total 1             A FAIRE
                    scores[joueur][15]+=0 # total 2
                    scores[joueur][16]+= 0# total 3
                    scores[joueur][17]+=0 # total total"""
                    session["scores"] = scores
                
                # fin du tour 
        print("oto")
        
        # calcul des bonus et du total des scores de chaque joueur à partir de score_i
        # fin tableau score calcul total ( pt bonus = )
        
    else :
        return "Page réservée aux membres authentifiés, veuiller vous connecter" +  render_template("index.html")
   
    return  render_template("jouer.html", valeur_des=valeur_des)


@app.route('/regle')
def regle():
    return render_template("regle.html")


@app.route('/score')
def score():
    if 'login' in session :
        scores = []
        fic = open("./data/scores.txt", "r")
        for ligne in fic:
            infos = ligne.split()
            scores.append(infos)
        fic.close()
        return render_template("score.html")
    else :
        return "Page réservée aux membres authentifiés, veuillez vous connecter"+  render_template("index.html")

@app.route('/nouvelle_partie', methods = ['POST'])
def nouvelle_partie():
    
    session['nbjoueur']=0
    session['lancer']=0
    session['joueur en cours']=0
    session['valeur_des']=valeur_des
    session['nombre_joueurs']=0
    session['choix_figure']=[[True,True,True,True,True,True], [True,True], [True,True,True,True,True]]
    session['jouer']=0
    session['fin']=False
    session['reset']=False
    return redirect("/jouer")

@app.route('/nombre_de_joueurs', methods = ['POST'])
def nombre_de_joueurs():
    session['nbjoueur']="nbjoueur"
    
    return redirect("/jouer")

@app.route('/jouer', methods = ['POST'])
def jouer():
    session['jouer']+=1
    session['lancer']+=1


if __name__ == '__main__':
    app.run(debug=True) # avec debug =True toute modif est immédiatement vue par le serveur




    # {% if session["jouer"] >=1 %}