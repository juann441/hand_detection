import cv2
from scipy import ndimage
import numpy as np

def process_frame(frame, target_width=531, target_height=531):

    # Obtenir les dimensions originales de l'image
    height, width = frame.shape[:2]

    # Calculer le ratio de redimensionnement pour la largeur ou la hauteur
    if width > height:
        ratio = target_width / width  # Si l'image est plus large que haute
    else:
        ratio = target_height / height  # Si l'image est plus haute que large

    # Calculer les nouvelles dimensions
    new_width = int(width * ratio)
    new_height = int(height * ratio)

    # Redimensionner l'image en maintenant les proportions
    resized_frame = cv2.resize(frame, (new_width, new_height))
    # Retourne l'image traitée
    return resized_frame, new_height, new_width

def segMain(img,lower_skin,upper_skin):
    # Convertir l'image en espace de couleurs HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Définir la plage de couleur pour le noir
    # lower_black = np.array([0, 56, 50])        # Plage basse pour le noir
    # upper_black = np.array([28, 255, 255])  # Plage haute pour le noir

    # Créer un masque pour isoler les objets noirs
    mask = cv2.inRange(hsv, lower_skin, upper_skin)


    # Inverser le masque pour obtenir l'objet sans le fond (si vous voulez isoler l'objet)
    mask_inv = 255 - cv2.bitwise_not(mask)
    # Création d'un petit élément structurant (par exemple, un carré 3x3)
    

    # Remplir les trous avec binary_fill_holes
    mask_inv = ndimage.binary_fill_holes(mask_inv).astype(np.uint8)

    dist = cv2.distanceTransform(mask_inv, cv2.DIST_L2, 3)
    distance_max = (np.max(dist))
    centre_main = np.where(dist == distance_max)
    centre_main = [centre_main[1][0],centre_main[0][0]]
    distance_max = int(distance_max)

    return mask_inv,centre_main,distance_max,dist # Retourner le masque inverse
