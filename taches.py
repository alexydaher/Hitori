
# ------------ Premier tâche --------------

def lire_grille(nom_fichier):
    """
    Fonction lis un fichier de grille et transforme en une liste de grille (ligne par ligne) et renvoie cette liste.
    Si le fichier contient une grille qui n'est pas optimale pour le jeu alors elle renvoie None.

    :param string nom_fichier: nom du fichier.
    :return: une liste ou None.
    """
    grille = []
    file = open(nom_fichier, 'r')
    
    for line in file.readlines():
        line = line.split()
        line_valeur = []
        for count in range(0, len(line)):
            try:
                line_valeur.append(int(line[count])) 
            except:
                return None
        grille.append(line_valeur) 
        
    liste_acceptable = []
    for liste in range(len(grille) - 2):
        if len(grille[liste]) != len(grille[liste + 1]):

            return None

    for nombre in range(1, len(grille[0]) + 1):
        liste_acceptable.append(str(nombre))

    for ligne in range(0, len(grille) - 1):
        for colonne in range(0, len(grille[0])):
            if str(grille[ligne][colonne]) not in liste_acceptable:
                return None

    return grille

def affiche_grille(grille):
    '''
    Fonction qui transforme la grille en tableau et le retourne.

    :param liste grille: liste de listes des valeurs de la grille.
    :return string tableau: tableau representant la grille.
    '''
    if grille == None:
        return None

    aire = len(grille)

    tableau = ''
    for liste in range(aire):
        for valeur in range(len(grille[liste]) - 1):
            tableau += str(grille[liste][valeur]) + ' '

        tableau += str(grille[liste][valeur + 1])
        if liste < aire - 1:
            tableau += '\n'
    
    return tableau

def ecrire_grille(grille, nom_fichier):
    '''
    Fonction qui ecrit la grille en forme de tableau dans le fichier.

    :param liste grille: liste de listes des valeurs de la grille.
    :param string nom_fichier: le nom du fichier à ecrire dessus.
    '''
    tableau = affiche_grille(grille)
    if tableau == None:
        return None

    tableau = tableau.split('\n')

    file = open(nom_fichier , 'w')
    for line in tableau:
        file.write(line)
        file.write('\n')
    file.close()



# ------------ Deuxième tâche --------------

def sans_conflit(grille, noircies):
    """
    Première regle.
    Si la grille ne respecte pas le première règle alors elle renvoie une liste des cases qui sont en conflit.
    Sinon, elle renvoie True.

    :param liste grille: liste des valeurs.
    :param liste noircies: liste des cases noircies.
    :return: liste ou True.
    """
    liste_conflit = []
    for colonne in range(len(grille[0])):
        liste_colonne = []
        for ligne in range(len(grille)):
            if (ligne, colonne) not in noircies:
                liste_colonne.append(grille[ligne][colonne])
            else:
                liste_colonne.append(0)

        for ligne in range(len(liste_colonne)):
            if liste_colonne[ligne] != 0:
                liste_colonne_copy = liste_colonne.copy()
                liste_colonne_copy.pop(ligne)
                if liste_colonne[ligne] in liste_colonne_copy:
                    liste_conflit.append((ligne, colonne))
    for ligne in range(len(grille)):
        liste_ligne = []
        for colonne in range(len(grille[0])):
            if (ligne, colonne) not in noircies:
                liste_ligne.append(grille[ligne][colonne])
            else:
                liste_ligne.append(0)
        for colonne in range(len(liste_ligne)):
            if liste_ligne[colonne] != 0:
                liste_ligne_copy = liste_ligne.copy()
                liste_ligne_copy.pop(colonne)
                if liste_ligne[colonne] in liste_ligne_copy:
                        liste_conflit.append((ligne, colonne))
    if liste_conflit == []:
        return True
    return liste_conflit

def sans_voisines_noircies(grille, ligne, colonne, piece, noircies):
    ''' 
    Fonction récursive qui retourne une piece des cases noirs connectées.
    
    :param liste grille:liste des valeurs.
    :param int ligne: identificateur de la ligne.
    :param int colonne: identificateur de la colonne.
    :param set piece: les cases noirs qui sont en voisinage.
    :param liste noircies: liste des cases noircies.
    :return set piece: les cases noirs qui sont en voisinage.
    '''
    piece.add((ligne, colonne))
    if colonne + 1 < len(grille[ligne]) and (ligne, colonne + 1) not in piece and (ligne, colonne + 1) in noircies :
        
        sans_voisines_noircies(grille, ligne, colonne + 1, piece, noircies)

    if colonne - 1 >= 0 and (ligne, colonne - 1) not in piece and (ligne, colonne - 1) in noircies :
    
        sans_voisines_noircies(grille, ligne, colonne - 1, piece, noircies)

    if ligne + 1 < len(grille) and (ligne + 1, colonne) not in piece and (ligne + 1, colonne) in noircies :

        sans_voisines_noircies(grille, ligne + 1, colonne, piece, noircies)

    if ligne - 1 >= 0 and (ligne - 1, colonne) not in piece and (ligne - 1, colonne) in noircies:

        sans_voisines_noircies(grille, ligne - 1, colonne, piece, noircies)

    return piece


def connexe(grille, ligne, colonne, piece, noircies):
    """
    Fonction récursive qui retourne une piece des cases blanches connectées. 
    
    :param liste grille:liste des valeurs.
    :param int ligne: identificateur de la ligne.
    :param int colonne: identificateur de la colonne.
    :param set piece: les cases blanches qui sont connectées.
    :param liste noircies: liste des cases noircies.
    :return set piece: les cases blanches qui sont connectées.
    """
    piece.add((ligne, colonne))
    if colonne + 1 < len(grille[ligne]) and (ligne, colonne + 1) not in piece and (ligne, colonne + 1) not in noircies :

        connexe(grille, ligne, colonne + 1, piece, noircies)

    if colonne - 1 >= 0 and (ligne, colonne - 1) not in piece and (ligne, colonne - 1) not in noircies :
    
        connexe(grille, ligne, colonne - 1, piece, noircies)
    
    if ligne + 1 < len(grille) and (ligne + 1, colonne) not in piece and (ligne + 1, colonne) not in noircies :

        connexe(grille, ligne + 1, colonne, piece, noircies)
    
    if ligne - 1 >= 0 and (ligne - 1, colonne) not in piece and (ligne - 1, colonne) not in noircies:

        connexe(grille, ligne - 1, colonne, piece, noircies)
    
    return piece