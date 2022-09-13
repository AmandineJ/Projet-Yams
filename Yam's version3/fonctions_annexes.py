# fonctions annexes
valeur_des = [1,2,1,3,1]


# Partie supérieure

def sup(valeur_des,A): # A est 1,2,3,4,5 ou 6 
    somme = 0
    for i in valeur_des:
        if i == A:
            somme +=1
    return(somme)

def total_partie_sup(scores,joueur):
    total_partie_sup = 0
    somme_sous_total_partie_sup = scores[joueur][0] + scores[joueur][1]+ scores[joueur][2]+ scores[joueur][3]+ scores[joueur][4]+ scores[joueur][5]
    if somme_sous_total_partie_sup >= 60:
        total_partie_sup+= 30
    total_partie_sup+= somme_sous_total_partie_sup
    return total_partie_sup

# Partie intermédiaire

def intermediaire(valeur_des):  # que ce soit intermédiaire supérieur ou inférieur, le calcul est le même
    sommeintermediaire = 0
    for i in valeur_des:
        sommeintermediaire += valeur_des[i]
    return sommeintermediaire

def total_partie_intermediaire(scores,joueur,valeur_des):
    s = 0
    for valeur in valeur_des: # on compte le nombre d'as
        if valeur_des[valeur]==1:
            s+=1
    total_partie_intermediaire = (scores[joueur][6] - scores[joueur][7])*s
    if total_partie_intermediaire < 0: # le score ne peut pas être nul
        return 0
    else:
        return total_partie_intermediaire
    

# Partie inférieure


def carre(valeur_des):
    somme_carre = 0
    valeur_des.sort()
    S = 0
    for i in valeur_des:
        S += valeur_des[i]
    if valeur_des[0]==valeur_des[1] and valeur_des[1]==valeur_des[2]==valeur_des[3]:
        somme_carre  = somme_carre + 40  + S
    elif valeur_des[1]==valeur_des[2]==valeur_des[3] and valeur_des[3]==valeur_des[4]:
        somme_carre  = somme_carre + 40 + S
    return somme_carre

def full(valeur_des):
    somme_full = 0
    valeur_des.sort()
    S = 0
    for i in valeur_des:
        S += valeur_des[i]
    if valeur_des[0]==valeur_des[1] and valeur_des[2]==valeur_des[3]==valeur_des[4]:
        somme_full  = somme_full + 30  + S
    elif valeur_des[0]==valeur_des[1] ==valeur_des[2] and valeur_des[3]==valeur_des[4]:
        somme_full  = somme_full + 30 + S
    return somme_full


def petitesuite(valeur_des):
    somme_petite_suite = 0
    valeur_des.sort()
    if valeur_des[0]==valeur_des[1] + 1 and valeur_des[1]==valeur_des[2] + 1 and valeur_des[2]==valeur_des[3] + 1:
        somme_petite_suite  = somme_petite_suite + 45 
    elif valeur_des[1]==valeur_des[2] + 1 and valeur_des[2]==valeur_des[3] + 1 and valeur_des[3]==valeur_des[4] + 1:
        somme_petite_suite  = somme_petite_suite + 45 
    return somme_petite_suite

def grandesuite(valeur_des):
    somme_grande_suite = 0
    valeur_des.sort()
    if valeur_des[0]==valeur_des[1] + 1 and valeur_des[1]==valeur_des[2] + 1 and valeur_des[2]==valeur_des[3] + 1 and valeur_des[3]==valeur_des[4] + 1:
        somme_grande_suite  = somme_grande_suite + 50 

def yams(valeur_des):
    somme_yams = 0
    S = 0
    for i in valeur_des:
        S += valeur_des[i]
    if valeur_des[0]==valeur_des[1] and valeur_des[1]==valeur_des[2] and valeur_des[2]==valeur_des[3] and valeur_des[3]==valeur_des[4]:
        somme_yams = somme_yams + 50 + S


def total_partie_inferieure(scores,joueur):
    return scores[joueur][8]+scores[joueur][9]+scores[joueur][10]+scores[joueur][11]+scores[joueur][12]


