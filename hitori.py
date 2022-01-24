from upemtk import*
from taches import*
from functions import*
from random import randint

while True:

    # Definir le fichier
    fichier = menu()

    # Creer la grille
    if fichier == None:
        break
    else:
        grille  = lire_grille(fichier)
    if grille == None:
        print("Le fichier n'st pas compatible pour le jeu Hitori.")
        break
    
    # --------- Partie Principale ---------------

    #Initialisation
    lignes=len(grille)
    colonnes=len(grille[0])

    fenetre_x = colonnes*70+200
    fenetre_y = lignes*70
    cree_fenetre(fenetre_x, fenetre_y)

    noircies = cases_noircies(fichier)

    tab_coord = tab_coordonnees(lignes, colonnes)

    # Differents Items

    # --- [ Boutons ] ---

    # note pour coordonnees : Clé : Ligne, Valeur : liste des colonnes

    # Annuler un coup [Bouton]
    annuler_ax_button = tab_coord[0][ len(tab_coord[0])-1 ][2]
    annuler_ay_button = tab_coord[0][ len(tab_coord[0])-1 ][1]
    annuler_bx_button = tab_coord[0][ len(tab_coord[0])-1 ][2]+100
    annuler_by_button = tab_coord[0][ len(tab_coord[0])-1 ][3]

    annuler_button = [annuler_ax_button, annuler_ay_button, annuler_bx_button, annuler_by_button]

    #Solver [Bouton]
    solver_ax_button = tab_coord[1][ len(tab_coord[1])-1 ][2]
    solver_ay_button = tab_coord[1][ len(tab_coord[1])-1 ][1]
    solver_bx_button = tab_coord[1][ len(tab_coord[1])-1 ][2]+100
    solver_by_button = tab_coord[1][ len(tab_coord[1])-1 ][3]

    solver_button = [solver_ax_button, solver_ay_button, solver_bx_button, solver_by_button]

    #Réinitialiser [Button]
    resetup_ax_button = tab_coord[ len(tab_coord)-1 ][ len(tab_coord[len(tab_coord)-1])-1 ][2]
    resetup_ay_button = tab_coord[ len(tab_coord)-1 ][ len(tab_coord[len(tab_coord)-1])-1 ][1]
    resetup_bx_button = tab_coord[ len(tab_coord)-1 ][ len(tab_coord[len(tab_coord)-1])-1 ][2]+100
    resetup_by_button = tab_coord[ len(tab_coord)-1 ][ len(tab_coord[len(tab_coord)-1])-1 ][3]

    resetup_button = [resetup_ax_button, resetup_ay_button, resetup_bx_button, resetup_by_button]


    # Aide [Button]
    aide_ax_button = resetup_ax_button
    aide_ay_button = resetup_ay_button-70
    aide_bx_button = resetup_bx_button
    aide_by_button = resetup_by_button-100

    aide_button = [aide_ax_button, aide_ay_button, aide_bx_button, aide_by_button]

    # Menu [Button]
    menu_ax_button = tab_coord[ len(tab_coord)-1 ][0][0]-100
    menu_ay_button = tab_coord[ len(tab_coord)-1 ][0][1]
    menu_bx_button = tab_coord[ len(tab_coord)-1 ][0][2]-70
    menu_by_button = tab_coord[ len(tab_coord)-1 ][0][3]

    menu_button = [menu_ax_button, menu_ay_button, menu_bx_button, menu_by_button]

    # Sauvegarder [Button]

    save_ax_button = menu_ax_button
    save_ay_button = menu_ay_button-70
    save_bx_button = menu_bx_button
    save_by_button = menu_by_button-100

    save_button = [save_ax_button, save_ay_button, save_bx_button, save_by_button]


    # Status des règles 1 2 et 3
    # Positiions
    r_position_x = fenetre_x-55
    r1_position_y = solver_by_button+50
    r2_position_y = r1_position_y+25
    r3_position_y = r2_position_y+25
    
    # Cercle coordonnées
    r_cercle_x = r_position_x+35
    r1_cercle_y = r1_position_y
    r2_cercle_y = r2_position_y
    r3_cercle_y = r3_position_y
    r_cercle_r = 5



    piece_cases = []
    cases_conflit = []

    piece = set()
    regle1 = None
    regle2 = None
    regle3 = None

    save_msg = 0
    resetup_msg = 0
    
    aide=False
    aide_count = 0

    solver = False
    
    return_menu=False
    backmenu=False
    retour_option={}
    quitte_partie=False
    quitte_jeu=False
    fin_jeu = None

    while True:
        efface_tout()

        # Aide
        if aide:
            if len(cases_conflit) != []:
                for elem in cases_conflit:
                    ligne = elem[0]
                    colonne = elem[1]

                    ax = tab_coord[ligne][colonne][0]
                    ay = tab_coord[ligne][colonne][1]
                    bx = tab_coord[ligne][colonne][2]
                    by = tab_coord[ligne][colonne][3]

                    cercle((ax + bx)/2 , (ay + by)/2, 25, couleur='red', remplissage='', epaisseur=2, tag='')

        affiche_tableau(tab_coord, grille)
        coloriage_case(noircies, tab_coord, 'black', grille)
        
        
        # Regle 2 Infraction
        if len(piece_cases) > 1:
            for elem in piece_cases:
                ligne = elem[0]
                colonne = elem[1]

                ax = tab_coord[ligne][colonne][0]
                ay = tab_coord[ligne][colonne][1]
                bx = tab_coord[ligne][colonne][2]
                by = tab_coord[ligne][colonne][3]

                rectangle(ax, ay, bx, by, couleur='Red', epaisseur=2)

        #Annuler un coup
        rectangle(annuler_ax_button, annuler_ay_button, annuler_bx_button, annuler_by_button, remplissage='navy')
        texte((annuler_ax_button+annuler_bx_button)/2, (annuler_ay_button+annuler_by_button)/2, "Annuler un coup", couleur='white', ancrage='center', taille=10 ) 
        
        #Solver
        rectangle(solver_ax_button, solver_ay_button, solver_bx_button, solver_by_button, remplissage='maroon')
        texte((solver_ax_button+solver_bx_button)/2, (solver_ay_button+solver_by_button)/2, "Solver", ancrage='center', couleur='white', taille='13')

        #Réinitialiser
        rectangle(resetup_button[0], resetup_button[1], resetup_button[2], resetup_button[3], remplissage='teal')
        texte((resetup_button[0] + resetup_button[2])/2, (resetup_button[1] + resetup_button[3])/2, "Réinitialiser", ancrage='center', couleur='white', taille='10')

        # Aide
        rectangle(aide_button[0], aide_button[1], aide_button[2], aide_button[3], remplissage='indigo')
        texte((aide_button[0] + aide_button[2])/2, (aide_button[1] + aide_button[3])/2, "Aide", ancrage='center', couleur='white', taille='10')

        #Message Gagné
        if regle1 == True and regle2  and regle3:
            ax = (fenetre_x/2)-75
            ay = (fenetre_y/2)-25
            bx = (fenetre_x/2)+75
            by = (fenetre_y/2)+25
            
            
            rectangle(ax, ay, bx, by, remplissage='gainsboro')
            texte(fenetre_x/2, fenetre_y/2, 'Bravo !', ancrage='center', couleur='Red')
            
        #Retour menu cadre
        rectangle(menu_button[0], menu_button[1], menu_button[2], menu_button[3], remplissage='teal')
        texte((menu_button[0] + menu_button[2])/2, (menu_button[1] + menu_button[3])/2, "Menu", ancrage='center', couleur='white', taille='14')
        
        #Retour menu message
        retour_menu_message(return_menu, fenetre_x, fenetre_y, 1)


        # Sauvegarder
        rectangle(save_button[0], save_button[1], save_button[2], save_button[3], remplissage='green')
        texte((save_button[0]+save_button[2])/2, (save_button[1]+save_button[3])/2, "Sauvegarder", couleur='white', ancrage='center', taille='10' )
    

        # Statut des regles
        texte(r_position_x,  r1_position_y, 'Regle 1', ancrage='center', taille='12')
        texte(r_position_x,  r2_position_y, 'Regle 2', ancrage='center', taille='12')
        texte(r_position_x,  r3_position_y, 'Regle 3', ancrage='center', taille='12')
        # Cercles
        if regle1 == True:
            cercle(r_cercle_x, r1_cercle_y, r_cercle_r, couleur='green', remplissage='green',)
        else:
            cercle(r_cercle_x, r1_cercle_y, r_cercle_r, couleur='red', remplissage='red',)
        
        if regle2:
            cercle(r_cercle_x, r2_cercle_y, r_cercle_r, couleur='green', remplissage='green',)
        else:
            cercle(r_cercle_x, r2_cercle_y, r_cercle_r, couleur='red', remplissage='red',)
        
        if regle3:
            cercle(r_cercle_x, r3_cercle_y, r_cercle_r, couleur='green', remplissage='green',)
        else:
            cercle(r_cercle_x, r3_cercle_y, r_cercle_r, couleur='red', remplissage='red',)

        # Message des actions
        if 0 < save_msg < 80:
            texte(10,10, "Sauvegardé", couleur='green', taille="10")
        if 0 < resetup_msg < 80:
            texte(10,30, "Réinitialisé", couleur='teal', taille="10")

        
        mise_a_jour()
        
        
        ev = donne_ev()
        ty = type_ev(ev)
        if ev is not None and ty == 'Quitte':
            quitte_jeu = True
            break
        
        if 0 < save_msg<80:
            save_msg += 1
        if 0 < resetup_msg < 80:
            resetup_msg += 1

        
        # Aide Fonction
        aide = aide_funct(aide, aide_button,ev)
        if aide:
            if aide_count < 60:
                aide_count += 1
            else:
                aide_count=0
                aide=False
        
    
        
        # Detection des cases qui ont été cliqués
        clique_cases_noircies(return_menu,fin_jeu, tab_coord, noircies,ev)

        # Supression de la dernière case noircie
        annule_coup(noircies, ev, annuler_button)

        # Supression de toutes les cases noircies
        resetup_msg = reinitialiser(fichier, noircies, ev, resetup_button, resetup_msg)
        
        # Detection du bouton Menu
        return_menu = retour_menu_button(return_menu, menu_button, ev) 
        
        # Dict de coordonnees pour Oui/Non
        retour_option = retour_menu_message(return_menu, fenetre_x, fenetre_y, 2)
        
        # Detection du Oui ou Non
        return_menu = retour_menu_action(return_menu, backmenu, retour_option, ev)[0]
        
        # Action buton Oui
        backmenu = retour_menu_action(return_menu, backmenu, retour_option, ev)[1] 

        # Sauvegarder la partie
        save_msg=save(fichier, noircies, ev, save_button, save_msg)
        




        # Première règle - Sans conflit
        regle1 = sans_conflit(grille, noircies)
        
        if regle1 != True and regle1 != None:
            cases_conflit = regle1 
        else:
            cases_conflit = []

        

        # Deuxiueme règle - sans voisinage noircies
        piece_cases = []
        piece2 = set()

        if len(noircies) > 1:
            for case in noircies:
                piece2 = sans_voisines_noircies(grille, case[0], case[1], piece2, noircies)
                if len(piece2) > 1:
                    for elem in piece2:
                        if elem not in piece_cases:
                            piece_cases.append(elem)
                piece2 = set()
        if piece_cases == []:
            regle2 = True
        else:
            regle2 = False
        
        # Troisieme Règle
        piece = set()
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

        #  -------- Solveur -----------

        # Detection du bouton Solveur
        solver = solveur(solver, ev, solver_button)

        if solver and fin_jeu != True:
            liste = resoudre(grille, [], tab_coord)
            if liste != None:
                noircies = liste
            else:
                print("Pas de Solution")
        solver = None
        # -----------------------------

        if regle1 == True and regle2 and regle3:
            fin_jeu = True
        else:
            fin_jeu = None

        if backmenu:
            quitte_partie = True
            break

    if quitte_partie:
        ferme_fenetre()
    if quitte_jeu:
        ferme_fenetre()
        break