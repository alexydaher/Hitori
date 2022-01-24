from taches import*
from random import randint

# ------------ Menu -------------

from upemtk import*
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def menu():
    """
    Fonction affiche la fenêtre Menu et renvoie le nom du fichier.

    :return: le nom du fichier.
    """

    taille_x=700
    taille_y=400
    cree_fenetre(taille_x,taille_y)

    #Fond de Menu
    image(taille_x/2, taille_y/2, 'back.png')

    #Items du menu
    tableaux={
        1:["Tableau de N1", "niveau1.txt"],
        2:["Tableau de N2", "niveau2.txt"],
        3:["Tableau de N3", "niveau3.txt"],
        4:["Tableau de N4", "niveau4.txt"],
        5:["Tableau de N5", "niveau5.txt"],
        6:["Choisir un fichier","None"]
    }


    rx = 85
    ry = 276
    rx2 = rx+100
    ry2 = ry+40

    for i in range(5):
        tableaux[i+1].append((rx,rx2,ry,ry2))
        # rectangle(rx,ry,rx2,ry2, couleur='white')
        rx = rx2+6
        rx2 = rx+101

    cx = 463
    cy = 325
    cx2 = cx+150
    cy2 = cy+40
    tableaux[6].append((cx,cx2,cy,cy2))


    #Detection du clique gauche
    while True:
        mise_a_jour()
        ev = donne_ev()

        if ev is not None and type_ev(ev) == 'ClicGauche':
            clique_gauche=(abscisse(ev),ordonnee(ev))

            for elem in tableaux:
                ax = tableaux[elem][2][0]
                bx = tableaux[elem][2][1]
                ay = tableaux[elem][2][2]
                by = tableaux[elem][2][3]
                
                if ax < clique_gauche[0] < bx and ay < clique_gauche[1] < by:
                    ferme_fenetre()
                    if elem == len(tableaux):
                        Tk().withdraw()
                        filename = askopenfilename()
                        return filename #Retourne le nom du fichier de l'utilisateur
                    else:
                        return tableaux[elem][1] #Retourne le nom du fichier
                    
        elif type_ev(ev) == 'Quitte':
            quitte = True
            break
        
    if quitte:
        
        ferme_fenetre()
        return None


def retour_menu_button(return_menu, menu_button, ev):
    """
    Detecte si le bouton menu a été cliqué et renvoir un booléen.

    :param booléen return_menu : True ou False.
    :param liste menu_button : liste des coordonnée du bouton menu.
    :param booléen ev : événement de l'utilisateur.
    :return: True ou False.
    """

    if ev is not None and type_ev(ev) == 'ClicGauche':
        clique_gauche=(abscisse(ev),ordonnee(ev))

        if menu_button[0] < clique_gauche[0] < menu_button[2] and menu_button[1] < clique_gauche[1] < menu_button[3]:
            return True
    
    return return_menu

def retour_menu_action(return_menu, backmenu, retour_option, ev):
    """
    Detection du menu retour (Oui ou Non) et renvoie un couple booléen.

    :param booléen return_menu : True ou False.
    :param booléen backmenu : True ou False.
    :param dict retour_option : coordonées des boutons Oui et Non.
    :param booléen ev : événement de l'utilisateur.
    :return : couple booléen.
    """
    if return_menu:
        oui = retour_option['oui']
        non = retour_option['non']
        if ev is not None and type_ev(ev) == 'ClicGauche':
            clique_gauche=(abscisse(ev),ordonnee(ev))

            if oui[0] < clique_gauche[0] < oui[2] and oui[1] < clique_gauche[1] < oui[3]:
                return True,True
            elif non[0] < clique_gauche[0] < non[2] and non[1] < clique_gauche[1] < non[3]:
                return False,False
    
    return return_menu,backmenu

def retour_menu_message(return_menu, fenetre_x, fenetre_y, option):
    """
    Affiche le message les options pour retourner au menu principal. (Option 1)
    Renvoie un dictionnaire de coordonnées pour les boutons Oui et Non. (Option 2)

    :param booléen return_menu : True ou False.
    :param int fenetre_x : largeur de la fenêtre du jeu.
    :param int fenetre_y : hauteur de la fenêtre du jeu.
    :param int option : 1 ou 2.
    :return(option 2) : un dictionnaire de coordonnées pour les boutons Oui et Non.
    """

    if return_menu:
        ax = (fenetre_x/2) - 150
        ay = (fenetre_y/2) - 70
        bx = (fenetre_x/2) + 150
        by = (fenetre_y/2) + 70

        oui_ax = ((ax + bx)/2) - 85
        oui_ay = ((ay + by)/2) + 10
        oui_bx = oui_ax + 50
        oui_by = oui_ay + 20

        non_ax = ((ax + bx)/2) + 35
        non_ay = ((ay + by)/2) + 10
        non_bx = non_ax + 50
        non_by = non_ay + 20

        if option == 1:
            
            rectangle(ax, ay, bx, by, remplissage='gainsboro')
            texte( (ax + bx)/2, ((ay + by)/2)-30, "Voulez-vous revenir au menu?", ancrage='center',police='Arial Black', taille='13' )
            
            rectangle(oui_ax, oui_ay, oui_bx, oui_by, remplissage='white')
            texte( (oui_ax + oui_bx)/2, ((oui_ay + oui_by)/2), "OUI",couleur='red', ancrage='center', taille='8' )

            rectangle(non_ax, non_ay, non_bx, non_by, remplissage='white')
            texte( (non_ax + non_bx)/2, ((non_ay + non_by)/2), "NON",couleur='green', ancrage='center', taille='8' )
        
        elif option == 2:

            retour_option={
                'oui':[oui_ax, oui_ay, oui_bx, oui_by],
                'non':[non_ax, non_ay, non_bx, non_by]
            }

            return retour_option

# -------------- Grille ----------------

import ast

def tab_coordonnees(lignes, colonnes):
    '''
    Fonction gènère les coordonnèes pour les rectangle en fonction des `lignes` et `colonnes`.

    :param int ligne : nombre de ligne.
    :param int colonne : nombre de colonne.
    :return : un dictionnaire (exemple: {0 : [ax, ay, bx by]} => clé : 0, listes des coordonnées ).

    '''
    tableau={}
    for ligne in range(lignes):

        tableau[ligne]=[]
        for colonne in range(colonnes):

            tableau[ligne].append([colonne * 70 + 100, ligne * 70, (colonne + 1) * 70 + 100, (ligne + 1) * 70 ] ) 
    
    return tableau



def affiche_tableau(coordonnees, grille):
    '''
    Fonction affiche le tableau et les valeurs dans la fenêtre grâce aux coordonnées fournis.

    :param dictionnaire coordonnees : coordonnées pours les cases.
    :param liste grille : liste des valuer de la grille.
    
    '''

    for ligne in coordonnees:

        for colonne in coordonnees[ligne]:
            ax = colonne[0]
            ay = colonne[1]
            bx = colonne[2]
            by = colonne[3]
            rectangle(ax, ay, bx, by)
            colonne_indice=coordonnees[ligne].index(colonne) #recupère l'indice de colonne
            texte((ax + bx)/2, (ay + by)/2, grille[ligne][colonne_indice], taille=15, ancrage='center')

def clique_cases_noircies(return_menu,fin_jeu, tab_coord, noircies,ev):
    """
    Detecte la case qui a été cliqué et s'ajoute la case à la liste des noircies sinon s'enlève si la cases existe déjà dans la noircies.

    :param booléen return_menu: True ou False.
    :param booléen fin_jeu : True ou False.
    :param dictionnaire tab_coordonées: coordonnées des cases.
    :param liste noircies : liste des couples.
    :param booléen ev :  événement de l'utilisateur.
    """
    if return_menu != True and fin_jeu != True and ev is not None and type_ev(ev) == 'ClicGauche':
        clique_gauche=(abscisse(ev),ordonnee(ev))

        for ligne in tab_coord:
            for colonne in range(len(tab_coord[ligne])):
                ax = tab_coord[ligne][colonne][0]
                ay = tab_coord[ligne][colonne][1]
                bx = tab_coord[ligne][colonne][2]
                by = tab_coord[ligne][colonne][3]


                if ax < clique_gauche[0] < bx and ay < clique_gauche[1] < by:
                    if (ligne, colonne) not in noircies:
                        noircies.append( (ligne, colonne) )
                    else:
                        indice=noircies.index((ligne,colonne))
                        noircies.pop( indice )
    return noircies

def coloriage_case(noircies, tab_coord, couleur,grille):
    """
    Fonction colories les cases qui sont dans la liste noircies.

    :param liste noircies : liste des couples.
    :param dictionnaire tab_coord : dictionnaire des coordonnées des cases.
    :param string couleur: couleur de remplissage des cases.
    :param liste grille : liste des valeurs des cases.
    """
    for elem in range(len(noircies)):
        ligne   = noircies[elem][0]
        colonne = noircies[elem][1]

        ax=tab_coord[ligne][colonne][0]
        ay=tab_coord[ligne][colonne][1]
        bx=tab_coord[ligne][colonne][2]
        by=tab_coord[ligne][colonne][3]
        
        rectangle(ax, ay, bx, by, couleur=couleur, remplissage='black', epaisseur=1, tag='cases_noirs')
        texte((ax + bx)/2,(ay + by)/2,grille[ligne][colonne], couleur='white', ancrage='center', taille='15', tag='cases_val')


def annule_coup(noircies, ev, annuler_button):
    """
    Fonction enleve le dernier couple de la liste noircies.

    :param liste noircies : liste des couples.
    :param booléen ev: événement de l'utilisateur.
    :param liste annuler_button: liste des coordonnées du bouton annuler un coup.
    """
    if noircies != [] and ev is not None and touche(ev)=='r':
        noircies.pop()
    elif noircies != [] and ev is not None and type_ev(ev) == 'ClicGauche':
        clique_gauche=(abscisse(ev),ordonnee(ev))
        ax = annuler_button[0]
        ay = annuler_button[1]
        bx = annuler_button[2]
        by = annuler_button[3]

        if ax < clique_gauche[0] < bx and ay < clique_gauche[1] < by:
            noircies.pop()

def reinitialiser(nom_fichier,noircies, ev, resetup_button, resetup_msg):
    """
    Fonction enlève toutes les cases noircies ainsi dans le fichier 'log.txt' où les cases noircies ont été sauvegardé.

    :param string nom_fichier: nom du fichier.
    :param liste noircies: liste des couples des cases noircies.
    :param liste resetup_button: liste des coordonées du bouton reinitialiser.
    :param int resetup_msg: nombre.
    :return: nombre.
    """
    if noircies != [] and ev is not None and type_ev(ev) == 'ClicGauche':
        clique_gauche=(abscisse(ev),ordonnee(ev))
        ax = resetup_button[0]
        ay = resetup_button[1]
        bx = resetup_button[2]
        by = resetup_button[3]

        if ax < clique_gauche[0] < bx and ay < clique_gauche[1] < by:
            noircies.clear()

            # Supprimer la sauvegarde
            fichier = open('log.txt', "r")
            log_lines = []

            for line in fichier:
                log_lines.append(line.strip())
            fichier.close()

            if nom_fichier in log_lines:
                index_nom_fichier = log_lines.index(nom_fichier)
                del log_lines[index_nom_fichier]
                del log_lines[index_nom_fichier]

                fichier = open('log.txt', "w")
                if len(log_lines) > 0:
                    for elem in log_lines:
                        fichier.write(elem + "\n")
                else:
                    fichier.write("")
                fichier.close()
            
            return 1
    return resetup_msg

            
def solveur(solver, ev, solver_button):
    """
    Detecte si le bouton solveur a été cliqué et renvoie un booléen.

    :param booléen solver: True ou False.
    :param booléen ev: événement de l'utilisateur.
    :param liste solver_button: liste des coordonnées du button solveur.
    :return: True ou False. 
    """
    if solver != True:
        if ev is not None and type_ev(ev) == 'ClicGauche':
            clique_gauche = (abscisse(ev),ordonnee(ev))

            ax = solver_button[0]
            ay = solver_button[1]
            bx = solver_button[2]
            by = solver_button[3]

            if ax < clique_gauche[0] < bx and ay < clique_gauche[1] < by:
                return True

    return solver

def save(nom_fichier, noircies, ev, save_button, save_msg):

    """
    Fonction sauvegarde les cases noircies dans le fichier 'log.txt'.

    :param string nom_fichier: nom du fichier.
    :param liste noircies: liste des couples des cases noircies.
    :param booléen ev: événement de l'utilisateur.
    :param liste save_button: liste des coordonnées des bouton de sauvegarde.
    :param int save_msg: nombre.
    """
    if noircies != [] and ev is not None and type_ev(ev) == 'ClicGauche':
        clique_gauche=(abscisse(ev),ordonnee(ev))
        ax = save_button[0]
        ay = save_button[1]
        bx = save_button[2]
        by = save_button[3]
        
        if ax < clique_gauche[0] < bx and ay < clique_gauche[1] < by:
            fichier = open('log.txt', "r")
            

            log_lines = []

            for line in fichier:
                log_lines.append(line.strip())

            fichier.close()

            if nom_fichier not in log_lines:
                
                fichier = open('log.txt', "a")
                fichier.write(nom_fichier+"\n")
                
                tmp = ""
                for elem in range(len(noircies)):
                    if elem == len(noircies)-1:
                        elem = str(noircies[elem])
                        tmp += elem
                    else:
                        elem = str(noircies[elem])+","
                        tmp += elem
                
                fichier.write(tmp + "\n")
                fichier.close()
            elif nom_fichier in log_lines:
                
                tmp = ""
                for elem in range(len(noircies)):
                    if elem == len(noircies)-1:
                        elem = str(noircies[elem])
                        tmp+=elem
                    else:
                        elem = str(noircies[elem])+","
                        tmp+=elem

                index_nom_fichier = log_lines.index(nom_fichier)

                log_lines[index_nom_fichier+1] = tmp

                fichier = open('log.txt',"w")

                for elem in log_lines:
                    fichier.write(elem+"\n")
                
                fichier.close()
            return 1
        
    return save_msg
            
def cases_noircies(nom_fichier):
    """
    Fonction vérifie s'il éxiste une sauvegarde de la grille dans le fichier 'log.txt' et renvoie une liste des cases noircies,
    sinon une liste vide.

    :param string nom_fichier: nom du fichier.
    :return: une liste.
    """
    fichier = open('log.txt', "r")
    log_lines = []

    for line in fichier:
        log_lines.append(line.strip())

    fichier.close()

    if nom_fichier in log_lines:
        index_nom_fichier = log_lines.index(nom_fichier)
        cases_noirs = log_lines[index_nom_fichier+1]
        cases_noirs = "["+cases_noirs+"]"
        noircies = ast.literal_eval(cases_noirs)
        
    else:
        noircies = []
    
    
    return noircies

def aide_funct(aide,aide_button, ev):
    """
    Détection du bouton aide et renvoie un booléen.

    :param booléen aide:True ou False.
    :param liste aide_button: liste des coordonnées du bouton aide.
    :param booléen ev: événement de l'utilisateur.
    :return: True ou False.
    """
    if ev is not None and type_ev(ev) == 'ClicGauche':
        clique_gauche=(abscisse(ev),ordonnee(ev))
        ax = aide_button[0]
        ay = aide_button[1]
        bx = aide_button[2]
        by = aide_button[3]

        if ax < clique_gauche[0] < bx and ay < clique_gauche[1] < by:
            
            return True
    return aide


# ------------- Solveur ----------------

from time import sleep

def resoudre(grille, noircies,tab_coord, case__=0):
    """
    Fonction résout la grille et renvoie une liste des cases noircies.
    
    :param liste grille: liste des valeurs de la grille.
    :param liste noircies: liste des cases noircies.
    :param dictionnaire tab_coord: dictionnaires des coordonnées des cases.
    :param int case__ = nombre du case (initialisation au 0).
    :return: liste des cases noircies. 
    """

    regle1 = None
    regle2 = True
    regle3 = True

    # regle 1
    regle1 = sans_conflit(grille, noircies)
    
    # regle 2
    if len(noircies) > 1:
        for elem in noircies:
            case=elem
            piece_2 = set()
            sans_voisines_noircies(grille, case[0], case[1], piece_2, noircies)
            if len(piece_2) > 1:
                regle2 = False
            else:
                regle2 = True
    
    # regle 3
    piece=set()
    if 1 < len(noircies) < len(grille) * len(grille[0]):
        ligne = randint(0, len(grille) - 1)
        colonne = randint(0, len(grille[0])-1) 
        while (ligne, colonne) in noircies:
            ligne = randint(0, len(grille) - 1)
            colonne = randint(0, len(grille[0]) - 1)
        
        connexe(grille, ligne, colonne, piece, noircies)
        
        if len(piece) == (len(grille[0]) * len(grille) - len(noircies)):
            regle3 = True
        else:
            regle3 = False
    else:
        regle3 = True
    
    
    # Solveur - Partie principale
    if regle2 != True or regle3 != True:
        return None
    else:
        if regle1 == True:
            return noircies
        else:
            liste_conflit = regle1
            noircies_copy = noircies.copy()
            noircies_copy.append(liste_conflit[case__])

            efface('cases_noirs')
            efface('cases_val')
            coloriage_case(noircies, tab_coord, 'black', grille)
            mise_a_jour()
            sleep(0.1)

            liste_possible = resoudre(grille, noircies_copy,tab_coord, case__)
            if liste_possible != None:
                return liste_possible

            noircies.append(liste_conflit[case__ + 1])
            liste_possible = resoudre(grille, noircies,tab_coord,case__)
            if liste_possible != None:
                return liste_possible
    return None
