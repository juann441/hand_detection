
import cv2
import numpy as np
from .maths_tools import * 

def boites(num_labels, labeled_image, stats,center_hand):
    # Liste pour stocker les surfaces des boîtes orientées et les bases des doigts
    bounding_box_areas = []
    bases = []  # Liste pour stocker les bases des doigts
    deux_doigts_colles = False
    trois_doigts_colles = False
    deux_trois = []
    largeurs = []
    D = 0 # Nombre de doigts collés, si 3 c'est trois doigts collés

    # Étape 3 : Parcourir les régions détectées
    for label in range(1, num_labels):  # Commencer à 1 pour ignorer le fond
        area = stats[label, cv2.CC_STAT_AREA]
        
        # Masque binaire pour la région actuelle
        region_mask = (labeled_image == label).astype(np.uint8)

        # Trouver les contours de la région
        contours, _ = cv2.findContours(region_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculer la boîte englobante orientée
        for contour in contours:
            if len(contour) >= 5:  # Minimum de points pour un rectangle valide
                rect = cv2.minAreaRect(contour) # ((50.0, 60.0) "centre du rect", (80.0, 40.0) "largeur, hauteur", 30.0 "inclinaison")
                box = cv2.boxPoints(rect)
                box = np.intp(box)  # Convertir en entier

                # Calculer la surface de la boîte orientée (largeur * hauteur)
                h, l = rect[1] # hauteur, largeur
                largeur = np.min((h,l))
                largeur = int(largeur)
                largeurs.append(largeur)
                
                if largeur < 49: 
                    deux_doigts_colles = False
                    trois_doigts_colles = False
                if 90 > largeur >= 40:
                    deux_doigts_colles = True
                    trois_doigts_colles = False
                    D = D + 1
                if largeur >= 90:
                    trois_doigts_colles = True
                    deux_doigts_colles = False
                    D = 3

                deux_trois.append((deux_doigts_colles,trois_doigts_colles))

                # Trouver le segment le plus proche du center_hand
                distances = []
                for i in range(4):  # Boîte a 4 coins
                    segment_start = box[i]
                    segment_end = box[(i + 1) % 4]  # Le prochain coin (circularité)
                    mid_point = ((segment_start[0] + segment_end[0]) // 2, (segment_start[1] + segment_end[1]) // 2)
                    distances.append((mid_point, distance(center_hand, mid_point)))  # Calculer distance au center_hand

                # Trouver le segment le plus proche
                closest_segment = min(distances, key=lambda x: x[1])
                base_point = closest_segment[0]  # Le point médian du segment le plus proche

                # Ajouter la base à la liste
                bases.append(base_point)

                # Tri des listes dans l'ordre croissant des x des bases
                for i in range(len(bases)):
                    # Trouver l'index du minimum en fonction de x
                    min_index = i
                    for j in range(i + 1, len(bases)):
                        if bases[j][0] < bases[min_index][0]:  # Comparaison sur la coordonnée x
                            min_index = j
                    
                    # Échanger les bases
                    bases[i], bases[min_index] = bases[min_index], bases[i]
                    
                    # Échanger les éléments correspondants dans deux_trois
                    deux_trois[i], deux_trois[min_index] = deux_trois[min_index], deux_trois[i]
                    largeurs[i], largeurs[min_index] = largeurs[min_index], largeurs[i]
                
                print(largeurs, " (largeurs)")
                print(bases, " (bases)")
                print(deux_trois, "(deux ou trois)")
                

    return bases, bounding_box_areas, deux_doigts_colles, trois_doigts_colles, deux_trois, D
