import cv2
from .circle import *

def generate_palm_mask(image, sampled_points):
    """
    Génère le masque de la paume en connectant les points de contour les plus proches.
    Args:
        image (np.array): Image binaire de la main.
        sampled_points (list): Points échantillonnés sur le cercle.

    Returns:
        list: Liste des points du contour de la paume.
    """
    palm_mask_points = []
    for x, y in sampled_points:
        boundary_point = find_nearest_boundary_point(image, x, y)
        if boundary_point:
            palm_mask_points.append(boundary_point)
    
    # Connecter les points pour former le masque
    for i in range(len(palm_mask_points) - 1):
        cv2.line(image, palm_mask_points[i], palm_mask_points[i + 1], color=255, thickness=1)
    
    # Fermer la boucle
    if palm_mask_points:
        cv2.line(image, palm_mask_points[-1], palm_mask_points[0], color=255, thickness=1)
    
        # Convertir les points du masque en format requis pour fillPoly
    palm_mask_points_np = np.array([palm_mask_points], dtype=np.int32)

    # Créer une nouvelle image vide pour le masque rempli
    palm_filled = np.zeros_like(image)

    # Remplir le contour
    cv2.fillPoly(palm_filled, palm_mask_points_np, color=255)


    return palm_mask_points,palm_filled

def find_wrist_points(palm_mask_points):
    """
    Trouve les deux points du poignet en fonction de la distance maximale entre deux points consécutifs.
    Args:
        palm_mask_points (list): Liste des points du masque de la paume.

    Returns:
        tuple: Deux points du poignet.
    """
    max_distance = 0
    wrist_points = None

    for i in range(len(palm_mask_points) - 1):
        point1 = palm_mask_points[i]
        point2 = palm_mask_points[i + 1]
        distance = np.linalg.norm(np.array(point1) - np.array(point2))
        if distance > max_distance:
            max_distance = distance
            wrist_points = (point1, point2)
    
    return wrist_points