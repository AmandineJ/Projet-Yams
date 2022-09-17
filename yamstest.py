# fonction principale
from flask import Flask, render_template, redirect, request, session
import random as random
from fonctions_annexes import * # faire plutot un import de chacune des fonctions annexes

app = Flask(__name__)

app.secret_key = "key"


##-------------------------PAGES DU SITE-------------------------------##

@app.route('/')
def index(): 
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout() :
    session.pop('login', None)
# ou bien del session['login']
    return "Vous êtes bien déconnecté"+  render_template("index.html")

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


@app.route('/jouer', methods = ['GET','POST'])
def yams():
    if 'login' in session : # on ne peut jouer que si on est connecté
        return  render_template("jouer.html")
    else :
        return "Page réservée aux membres authentifiés, veuiller vous connecter" +  render_template("index.html")
    
    

##-------------------------COMPLEMENT DE PAGES-------------------------------##


#--------------COMPLEMENT LOGIN---------------#
@app.route('/valid_login',methods = ['GET','POST'])

def valid_login() :
    if request.form['pwd'] == 'gsea': #mot de passe correct
        session['login'] = request.form['login']
        session["nbjoueur"]= -1
        return "Bienvenue "+ session['login'] +  render_template("index.html")

    else :
        return redirect('/login')
    

#--------------COMPLEMENT JOUER---------------#   
    
@app.route('/nouvelle_partie', methods = ['POST'])
def nouvelle_partie():
    
    session['nbjoueur']=0
    session['tour en cours']=0  # peut aller jusqu'à 13
    session['joueur en cours']=0
    session['valeur_des']=[]
    session['choix_figure']=[]
    session['score']=[]
    session['etape'] = 0 # etape 0 : nombre de joueur, etapes 1: c'est au joueur x de jouer, etapes 234: lancers de des, etape5: selection figure
    session['fin']=False
    session['fin_lancer']=False
    return redirect("/jouer")

@app.route('/nombre_de_joueurs', methods = ['POST'])
def nombre_de_joueurs():
    session['nbjoueur']=int(request.form['nbjoueurs'])
    # initialisation de la liste des scores
    scores=session['score']
    choix_figure=session['choix_figure']
    for i in range(session['nbjoueur']):   
        scores.append([0]*18)# création d'une liste de joueurs contenant la liste de leurs scores (13) + 1 bonus + 3 totals + 1 total total
        choix_figure.append([True]*18)
    session['etape']+=1 # on a terminé l'étape 0, passons à l'étape 1
    print("nombre de joueurs ok")
    return redirect("/jouer")



@app.route('/lancer_des1', methods = ['POST'])
def lancer_des():
    print("lancer des 1 ok")
    for de in range (5):
        session["valeur_des"].append(random.randint(1,6))
    session['etape']+=1
    return redirect("/jouer")                    # 1 er lancer terminé
    

@app.route('/lancer_des23', methods = ['POST'])
def lancer_des23():
    print("lancer des 2 et 3 ok")
 # on récupère la liste des itérations des dés à relancer
    session['desrelancer']= list(map(int, request.form.getlist("selectde")))
    print(session["valeur_des"])
    for id_de in list(map(int, request.form.getlist('selectde'))):# mettre 01234 dans names   
        session["valeur_des"][id_de] = random.randint(1,6) # on relance ces dés
        print(session["valeur_des"])
        print(id_de)         # 2 eme ou 3 eme lancer terminé
    session['etape']+=1
    return redirect("/jouer")   



@app.route('/choixdes', methods = ['POST'])
def choixdes():
    session['desrelancer']= list(map(int, request.form.getlist("selectde")))
    return redirect("/jouer")


@app.route('/finir_lancer', methods = ['POST'])
def finir_lancer():
    session['fin_lancer']=True
    return redirect("/jouer")



@app.route('/choix_figure', methods = ['POST'])
def choix_figure():
      # on est a l'étape 5
# choix d'une figure dans une liste déroulant
    figure = request.form['choix_figure']
    #session["choix_figure"] = 'choix figure' merci erreur de merde 
    # utilisation des fonctions annexes pour calculer le score
    # partie supérieure
    scores = session["score"]
    joueur = session["joueur en cours"]
    choix_figure = session['choix_figure']
    valeur_des = session['valeur_des']
    if figure == '1':
        scores[joueur][0]+= sup(valeur_des,1)# c'est le 1 er score de la liste du joueur ( ordre arbitraire choisi par moi ) # joueur -1 car la liste commence à 0 et pas à 1
        choix_figure[joueur][0] = False
    elif figure == '2':
        scores[joueur][1]+= sup(valeur_des,2)
        choix_figure[joueur][1] = False
    elif figure == '3':
        scores[joueur][2]+= sup(valeur_des,3)
        choix_figure[joueur][2] = False
    elif figure == '4':
        scores[joueur][3]+= sup(valeur_des,4)
        choix_figure[joueur][3] = False
    elif figure == '5':
        scores[joueur][4]+= sup(valeur_des,5)
        choix_figure[joueur][4] = False
    elif figure == '6':
        scores[joueur][5]+= sup(valeur_des,6)
        choix_figure[joueur][5] = False
    # partie intermédiaire A FAIRE D ABORD DNS ANNEXES
    elif figure == 'intermédiairesup':
        scores[joueur][6]+= intermediaire(valeur_des)
        choix_figure[joueur][6] = False
    elif figure == 'intermédiaireinf':
        scores[joueur][7]+= intermediaire(valeur_des)
        choix_figure[joueur][7] = False
    
    # partie inférieure A FAIRE D'ABORD DANS ANNEXES
    elif figure == 'carre':
        scores[joueur][8]+= carre(valeur_des)
        choix_figure[joueur][8] = False
    elif figure == 'full':
        scores[joueur][9]+= full(valeur_des)
        choix_figure[joueur][9] = False
        print(scores[joueur][9])
    elif figure == 'petite suite':
        scores[joueur][10]+= petitesuite(valeur_des)
        choix_figure[joueur][10] = False
    elif figure == 'grande suite':
        scores[joueur][11]+= grandesuite(valeur_des)
        choix_figure[joueur][11] = False
    else : #figure == 'yams'
        scores[joueur][12]+= calcul_yams(valeur_des)
        choix_figure[joueur][12] = False
    # actualiser le tableau  des scores
    scores[joueur][13]+= total_partie_sup(scores,joueur) # total avec bonus de la partie 1 
    scores[joueur][14]+=0 # total 1             
    scores[joueur][15]+=0 # total 2
    scores[joueur][16]+= 0# total 3
    scores[joueur][17]+=0 # total total
    print("fin choix figure")
    print("choix figure ok",session['score'],session['choix_figure'])
    if session['joueur en cours'] >= session['nbjoueur']-1:
        print("fin du tour ok ")
        if session['tour en cours'] == 13:
            session['etape']=99 # faire le tableau html des résultats avec condition if 99
            return "c'est la fin du jeu " + redirect("/jouer")  
        else:
            session['tour en cours']+=1
            session['joueur en cours']=0
    else: 
        session['joueur en cours']+=1
        print("on passe au joueur suivant, on reste au meme tour")
    session['etape']=1
    session['valeur_des']=[]
    print ("on est arrivé à la fin de la boucle")
    
    return redirect("/jouer")   

   
# a la fin de la partie, enregistrer les scores  

@app.route('/enregistrer', methods = ['GET','POST'])
def yams_enregistrer():
    fic  = open("./data/scores.txt","a")
    fic.write(session['scores'] +" \n")
    fic.close()
    return " Scores enregistrés" + redirect("/jouer") 

 




if __name__ == '__main__':
    app.run(debug=True) # avec debug =True toute modif est immédiatement vue par le serveur

    

###-----------------------------------IDEES---------------------------------------###
# Trucs à faire:
# - Faire  l'enregistrement 
# - Enlever les combinaisons déjà choisies avec des if false dans la partie jouer.html 
# - verifier les fonctions annexes ( faire des tests pour chacunes surtout pour full, j'ai l'impression qu'elle renvoie 0)
# - faire l'affichage du tableau des scores à la fin de la partie 

# idée bonus: mettre le tableau a chaque fin de tour
    
