import cv2
import numpy as np

from utils.launch_hsv_adjuster import *
from utils.processing_tools import *
from utils.circle import *
from utils.palm import *
from utils.maths_tools import *
from utils.miscellanous import *
from utils.bounding_boxes import *
from utils.dictionnary import *



# Initilisation des variables
pouce_gauche = False
pouce_droit = False

# Étape 1 : Régler les paramètres HSV avec un retour dynamique
lower_skin, upper_skin = launch_hsv_adjuster_dynamic()

if lower_skin is None or upper_skin is None:
    print("Aucune plage HSV valide définie. Arrêt du programme.")
    exit()

# Étape 2 : Lancement du traitement vidéo
cap = cv2.VideoCapture(0)  # Ou utiliser 4 si 0 ne fonctionne pas

# Créer une seule fenêtre d'affichage avant la boucle
cv2.namedWindow('Flux vidéo traité', cv2.WINDOW_NORMAL)

if not cap.isOpened():
    print("Erreur d'ouverture de la caméra")
    exit()

while True:
    # Capture une image du flux vidéo
    ret, img = cap.read()

    if not ret:
        print("Erreur de lecture de la frame")
        break

    # Appeler la fonction pour traiter l'image
    img2, h, w = process_frame(img)
    print(lower_skin, upper_skin)
    hand_segmented_original, centre_main, distance_max, dist_transform = segMain(img2, lower_skin, upper_skin)
    pixels_of_hand = np.count_nonzero(hand_segmented_original)
    
    # Trouver le rayon maximal du cercle interne
    radius_max = find_inner_circle(np.copy(hand_segmented_original), centre_main)
    
    radius_max_ultra = int(radius_max * 1.3)

    # Échantillonnage des points sur le cercle de rayon `inner_max`
    sampled_points = sample_points_on_circle(centre_main, radius_max_ultra, step=10)
    
    # Générer le masque de la paume
    palm_mask_points,filled_palm_mask = generate_palm_mask(np.copy(hand_segmented_original), sampled_points)
    
    wrist_points = find_wrist_points(palm_mask_points)
    if wrist_points is not None :
            mid_wrist, wrist_points, center_hand, M = rotation_main(wrist_points,centre_main,hand_segmented_original)
            img2, image_rotated, palm_segmented, coordonates_mid_wrist, wrist_points, center_hand = apply_rotation(img2,np.copy(hand_segmented_original),filled_palm_mask,mid_wrist,wrist_points,h,w,center_hand,M)
            
            fingers_segmented = segmentation(image_rotated, palm_segmented)
             
            num_labels, labeled_image, stats, centroids = labelisation(fingers_segmented,pixels_of_hand)
            #centroids = filter_background(num_labels, labeled_image)
            bases, bouding_boxe_areas, deux_doigt_colles, trois_doigts_colles, deux_trois, D = boites(num_labels, labeled_image, stats,center_hand)
            doigts, doigt_angle, pouce_droit, pouce_gauche, haut, bas, gauche, droite = detection_doigts(bases, pouce_droit, pouce_gauche, deux_doigt_colles, trois_doigts_colles, deux_trois, D,center_hand)
                      # Affiche le résultat du traitement
            for base in bases:
                cv2.circle(img2, (base[0], base[1]), radius=5, color=(0, 0, 255), thickness=-1)  # Rouge

            # 2. Tracer le centre de la main en vert
            cv2.circle(img2, (center_hand[0], center_hand[1]), radius=7, color=(0, 255, 0), thickness=-1)  # Vert

            # 3. Tracer les lignes du centre de la main à chaque base
            for base in bases:
                cv2.line(img2, (center_hand[0], center_hand[1]), (base[0], base[1]), color=(255, 0, 0), thickness=2)  # Bleu

            # 4. Annoter les doigts détectés
            for doigt, base in doigts.items():
                cv2.putText(img2, doigt, (base[0] + 10, base[1] - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)  # Blanc

            # for angle, base in doigt_angle.items():
            #     cv2.putText(img2, f"{angle}", (base[0], base[1]), 
            #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)  # Blanc

            cv2.imshow('Flux vidéo traité', img2)

            #jeu(haut, bas, gauche, droite)


    cv2.imshow('Flux vidéo traité', img2)

    # Sortie avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libère les ressources et ferme les fenêtres
cap.release()
cv2.destroyAllWindows()

