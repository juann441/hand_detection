
import numpy as np

def detection_doigts(bases, pouce_droit_anterieur, pouce_gauche_anterieur, deux_doigts, trois_doigts, deux_trois, D,center_hand):
    nb_doigts = len(bases)
    current_pouce = False
    pouce_droit = pouce_droit_anterieur
    pouce_gauche = pouce_gauche_anterieur
    doigt_angle = {}

    # Initialiser les variables pour le jeu
    haut, bas, gauche, droite = False, False, False, False

    if nb_doigts !=0 :
        
        # Calculer l'angle entre chaque centre de massse et le centre de la main
        angles = []
        for centroid in bases:
            # Calculer le vecteur entre le centre de la main et le centre de masse
            angle = np.arctan2(center_hand[1] - centroid[1], centroid[0] - center_hand[0]) * 180 / np.pi
            # angle = np.abs(angle)
            angle = int(angle)
            angles.append(int(angle))
            doigt_angle[angle] = centroid
            if  150 < angle <= 180 or -180 <= angle < -150 :
                pouce_gauche = True
                pouce_droit = False
                current_pouce = True
                print('Pouce gauche')
            if  0 <= angle < 20 or -20 <= angle <= 0 :
                pouce_droit = True
                pouce_gauche = False
                current_pouce = True
                print('Pouce droit')

        if pouce_gauche == False and pouce_droit == False :
            print('Pas de pouce')

        print('Nombre de doigts :', nb_doigts)
        print('Pouce Gauche :', pouce_gauche)
        print('Pouce Droit :', pouce_droit)
        print('Pouce Actuel :', current_pouce)
        print('Doigts collés :', D)

    # dictionnaire doit contenir les valeurs des angles et des centroides
    doigts = {}

    if nb_doigts == 5:
        "On a tous les doigts, donc les doigts suivent l'ordre logique du pouce"
        if pouce_droit == True:
            # Ordre croissant des angles
            doigts['POUCE'] = bases[4]
            doigts['INDEX'] = bases[3]
            doigts['MAJEUR'] = bases[2]
            doigts['ANNULAIRE'] = bases[1]
            doigts['AURICULAIRE'] = bases[0]

        if pouce_gauche == True:
            # Ordre décroissant des angles
            doigts['POUCE'] = bases[0]
            doigts['INDEX'] = bases[1]
            doigts['MAJEUR'] = bases[2]
            doigts['ANNULAIRE'] = bases[3]
            doigts['AURICULAIRE'] = bases[4]
            # Variable jeu
            bas = True

    if nb_doigts == 4:
        "On a tous les doigts sauf le pouce mais sachant que le code a été calibré avant on peut utiliser la valeur du pouce"
        if pouce_droit == True and current_pouce == False and D == 0:
            # Ordre croissant des angles
            doigts['INDEX'] = bases[3]
            doigts['MAJEUR'] = bases[2]
            doigts['ANNULAIRE'] = bases[1]
            doigts['AURICULAIRE'] = bases[0]
        
        if pouce_gauche == True and current_pouce == False and D == 0:
            # Ordre décroissant des angles
            doigts['INDEX'] = bases[0]
            doigts['MAJEUR'] = bases[1]
            doigts['ANNULAIRE'] = bases[2]
            doigts['AURICULAIRE'] = bases[3]

        "On a qautre doigt avec le pouce compris à gauche"
        if pouce_gauche == True and current_pouce == True and D == 0:
            doigts['POUCE'] = bases[0]
            doigts['INDEX'] = bases[1]
            doigts['MAJEUR'] = bases[2]
            doigts['ANNULAIRE'] = bases[3]

        "On a qautre doigt avec le pouce compris à droite"
        if pouce_droit== True and current_pouce == True and D == 0:
            doigts['POUCE'] = bases[3]
            doigts['INDEX'] = bases[2]
            doigts['MAJEUR'] = bases[1]
            doigts['ANNULAIRE'] = bases[0]

        if pouce_gauche == True and current_pouce == True and D == 1:
            doigts['POUCE'] = bases[0]
            if deux_trois[1][0] == True:
                doigts['INDEX-MAJEUR'] = bases[1]
                doigts['ANNULAIRE'] = bases[2]
                doigts['AURICULAIRE'] = bases[3]
            if deux_trois[2][0] == True : 
                doigts['INDEX'] = bases[1]
                doigts['MAJEUR-ANNULAIRE'] = bases[2]
                doigts['AURICULAIRE'] = bases[3]
            if deux_trois[3][0] == True:
                doigts['INDEX'] = bases[1]
                doigts['MAJEUR'] = bases[2]
                doigts['ANNULAIRE-AURICULAIRE'] = bases[3]

        if pouce_droit == True and current_pouce == True and D == 1:
            if deux_trois[0][0] == True:
                doigts['AURICULAIRE-ANNULAIRE'] = bases[0]
                doigts['MAJEUR'] = bases[1]
                doigts['INDEX'] = bases[2]
            if deux_trois[1][0] == True : 
                doigts['AURICULAIRE'] = bases[0]
                doigts['ANNULAIRE-MAJEUR'] = bases[1]
                doigts['INDEX'] = bases[2]
            if deux_trois[2][0] == True:
                doigts['AURICULAIRE'] = bases[0]
                doigts['ANNULAIRE'] = bases[1]
                doigts['MAJEUR-INDEX'] = bases[2]
            doigts['POUCE'] = bases[3]

    if nb_doigts == 3:
        "On a trois doigts"
        if pouce_droit == True and current_pouce == True and D == 0:
            if np.abs(bases[1][0] - bases[0][0]) < 70 :
                doigts['MAJEUR'] = bases[0]
                doigts['INDEX'] = bases[1]
                doigts['POUCE'] = bases[2]
            if np.abs(bases[1][0] - bases[0][0]) >= 70 :
                doigts['AURICULAIRE'] = bases[0]
                doigts['INDEX'] = bases[1]
                doigts['POUCE'] = bases[2]
        
        if pouce_gauche == True and current_pouce == True and D == 0:
            if np.abs(bases[2][0] - bases[1][0]) < 70 :
                doigts['POUCE'] = bases[0]
                doigts['INDEX'] = bases[1]
                doigts['MAJEUR'] = bases[2]
            if np.abs(bases[2][0] - bases[1][0]) >= 70 :
                doigts['POUCE'] = bases[0]
                doigts['INDEX'] = bases[1]
                doigts['AURICULAIRE'] = bases[2]
        
        if pouce_droit == True and current_pouce == False and D == 0:
            doigts['INDEX'] = bases[2]
            doigts['MAJEUR'] = bases[1]
            doigts['ANNULAIRE'] = bases[0]
        
        if pouce_gauche == True and current_pouce == False and D == 0:
            doigts['INDEX'] = bases[0]
            doigts['MAJEUR'] = bases[1]
            doigts['ANNULAIRE'] = bases[2]

        if pouce_gauche == True and current_pouce == False and D == 1:
            if deux_trois[0][0] == True:
                doigts['INDEX-MAJEUR'] = bases[0]
                doigts['ANNULAIRE'] = bases[1]
                doigts['AURICULAIRE'] = bases[2]
            if deux_trois[1][0] == True : 
                doigts['INDEX'] = bases[0]
                doigts['MAJEUR-ANNULAIRE'] = bases[1]
                doigts['AURICULAIRE'] = bases[2]
            if deux_trois[2][0] == True:
                doigts['INDEX'] = bases[0]
                doigts['MAJEUR'] = bases[1]
                doigts['ANNULAIRE-AURICULAIRE'] = bases[2]

        if pouce_droit == True and current_pouce == False and D == 1:
            if deux_trois[0][0] == True:
                doigts['AURICULAIRE-ANNULAIRE'] = bases[0]
                doigts['MAJEUR'] = bases[1]
                doigts['INDEX'] = bases[2]
            if deux_trois[1][0] == True : 
                doigts['AURICULAIRE'] = bases[0]
                doigts['ANNULAIRE-MAJEUR'] = bases[1]
                doigts['INDEX'] = bases[2]
            if deux_trois[2][0] == True:
                doigts['AURICULAIRE'] = bases[0]
                doigts['ANNULAIRE'] = bases[1]
                doigts['MAJEUR-INDEX'] = bases[2]

        if pouce_gauche == True and current_pouce == True and D == 2:
            doigts['POUCE'] = bases[0]
            doigts['INDEX-MAJEUR'] = bases[1]
            doigts['ANNULAIRE-AURICULAIRE'] = bases[2]

        if pouce_droit == True and current_pouce == True and D == 2:
            doigts['AURICULAIRE-ANNULAIRE'] = bases[0]
            doigts['MAJEUR-INDEX'] = bases[1]
            doigts['POUCE'] = bases[2]
        
        if pouce_gauche == True and current_pouce == False and D == 2:
            if deux_trois[0][0] == True:
                doigts['INDEX-MAJEUR'] = bases[0]
                doigts['ANNULAIRE'] = bases[1]
                doigts['AURICULAIRE'] = bases[2]
            if deux_trois[1][0] == True : 
                doigts['INDEX'] = bases[0]
                doigts['MAJEUR-ANNULAIRE'] = bases[1]
                doigts['AURICULAIRE'] = bases[2]
            if deux_trois[2][0] == True:
                doigts['INDEX'] = bases[0]
                doigts['MAJEUR'] = bases[1]
                doigts['ANNULAIRE-AURICULAIRE'] = bases[2]

        if pouce_droit == True and current_pouce == False and D == 2:
            if deux_trois[0][0] == True:
                doigts['AURICULAIRE-ANNULAIRE'] = bases[0]
                doigts['MAJEUR'] = bases[1]
                doigts['INDEX'] = bases[2]
            if deux_trois[1][0] == True : 
                doigts['AURICULAIRE'] = bases[0]
                doigts['ANNULAIRE-MAJEUR'] = bases[1]
                doigts['INDEX'] = bases[2]
            if deux_trois[2][0] == True:
                doigts['AURICULAIRE'] = bases[0]
                doigts['ANNULAIRE'] = bases[1]
                doigts['MAJEUR-INDEX'] = bases[2]
        
        if pouce_gauche == True and current_pouce == False and D == 3:
            doigts['POUCE'] = bases[0]
            if deux_trois[1][1] == True:
                doigts['INDEX-MAJEUR-ANNULAIRE'] = bases[1]
                doigts['AURICULAIRE'] = bases[2]
            
            if deux_trois[1][1] == False:
                doigts['INDEX'] = bases[1]
                doigts['MAJEUR-ANNULAIRE-AURICULAIRE'] = bases[2]     

        if pouce_droit == True and current_pouce == False and D == 3:
            if deux_trois[0][1] == True:
                doigts['AURICULAIRE-ANNULAIRE-MAJEUR'] = bases[0]
                doigts['INDEX'] = bases[1]
            
            if deux_trois[0][1] == False:
                doigts['AURICULAIRE'] = bases[0]
                doigts['ANNULAIRE-MAJEUR-INDEX'] = bases[1]

            doigts['POUCE'] = bases[2]
        
    if nb_doigts == 2:
        "On a deux doigts"
        if pouce_droit == True and current_pouce == True and D == 0:
            doigts['POUCE'] = bases[1]
            doigts['INDEX'] = bases[0]
        
        if pouce_gauche == True and current_pouce == True and D == 0:
            doigts['POUCE'] = bases[0]
            doigts['INDEX'] = bases[1]
        
        if pouce_droit == True and current_pouce == False and D == 0:
            if np.abs(bases[1][0] - bases[0][0]) < 70 :
                doigts['MAJEUR'] = bases[0]
                doigts['INDEX'] = bases[1]
            if np.abs(bases[1][0] - bases[0][0]) >= 70 :
                doigts['AURICULAIRE'] = bases[0]
                doigts['INDEX'] = bases[1]
        
        if pouce_gauche == True and current_pouce == False and D == 0:
            if np.abs(bases[1][0] - bases[0][0]) < 70 :
                doigts['INDEX'] = bases[0]
                doigts['MAJEUR'] = bases[1]
            if np.abs(bases[1][0] - bases[0][0]) >= 70 :
                doigts['INDEX'] = bases[0]
                doigts['AURICULAIRE'] = bases[1]


        if pouce_gauche == True and current_pouce == False and D == 2:
            doigts['INDEX-MAJEUR'] = bases[0]
            doigts['ANNULAIRE-AURICULAIRE'] = bases[1]

        if pouce_droit == True and current_pouce == False and D == 2:
            doigts['AURICULAIRE-ANNULAIRE'] = bases[0]
            doigts['MAJEUR-INDEX'] = bases[1]

        if pouce_gauche == True and current_pouce == False and D == 3:
            if deux_trois[0][1] == True:
                doigts['INDEX-MAJEUR-ANNULAIRE'] = bases[0]
                doigts['AURICULAIRE'] = bases[1]
            
            if deux_trois[0][1] == False:
                doigts['INDEX'] = bases[0]
                doigts['MAJEUR-ANNULAIRE-AURICULAIRE'] = bases[1]

        if pouce_droit == True and current_pouce == False and D == 3:
            if deux_trois[0][1] == True:
                doigts['AURICULAIRE-ANNULAIRE-MAJEUR'] = bases[0]
                doigts['INDEX'] = bases[1]
            
            if deux_trois[0][1] == False:
                doigts['AURICULAIRE'] = bases[0]
                doigts['ANNULAIRE-MAJEUR-INDEX'] = bases[1]
        
        if pouce_droit == True and current_pouce == True and D == 1:
            doigts['MAJEUR-INDEX'] = bases[0]
            doigts['POUCE'] = bases[1]

        if pouce_gauche == True and current_pouce == True and D == 1:
            doigts['POUCE'] = bases[0]
            doigts['INDEX-MAJEUR'] = bases[1]
        
    if nb_doigts == 1:
        if current_pouce == True:
            doigts['POUCE'] = bases[0]
            # Variable jeu
            droite = True
            
        if current_pouce == False and pouce_gauche == True and 120 <= angles[0] <= 140 and D == 0:
            doigts['INDEX'] = bases[0]
            # Variable jeu
            haut = True
        
        if current_pouce == False and pouce_gauche == True and 30 <= angles[0] < 60 and D ==0:
            doigts['AURICULAIRE'] = bases[0]
            # Variable jeu
            gauche = True

        if current_pouce == False and pouce_droit == True and 40 <= angles[0] <= 100 and D == 0:
            doigts['INDEX'] = bases[0]
        
        if current_pouce == False and pouce_droit == True and 120 <= angles[0] <= 160 and D == 0:
            doigts['AURICULAIRE'] = bases[0]
        
        if current_pouce == False and pouce_gauche == True and D == 1:
            doigts['INDEX-MAJEUR'] = bases[0]

        if current_pouce == False and pouce_droit == True and D == 1:
            doigts['MAJEUR-INDEX'] = bases[0]



    return doigts, doigt_angle, pouce_droit, pouce_gauche, haut, bas, gauche, droite
