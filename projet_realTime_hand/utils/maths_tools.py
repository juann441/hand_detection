import cv2
import math
import numpy as np

# Calculer la distance entre deux points
def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def rotation_main(wrist_points, center_hand,hand_segmented_original):
    center_hand = (int(center_hand[0]), int(center_hand[1])) 
    # Points du poignet
    wrist_point1 = np.array(wrist_points[0])
    wrist_point2 = np.array(wrist_points[1])

    # Point central de la main
    center_hand = np.array(center_hand)

    # Calculer le vecteur directeur de la wrist line
    wrist_vector = wrist_point2 - wrist_point1

    # Milieu de la wrist line
    mid_wrist = (wrist_point1 + wrist_point2) / 2
    #coordonates_mid_wrist = np.zeros_like(hand_crop)
    #coordonates_mid_wrist[int(mid_wrist[1]),int(mid_wrist[0])] = 1


    # Calculer le vecteur entre le centre de la main et le milieu du poignet
    center_to_mid_wrist = mid_wrist - center_hand

    # Calculer l'angle entre les deux vecteurs
    dot_product = np.dot(wrist_vector, center_to_mid_wrist)
    norm_wrist = np.linalg.norm(wrist_vector)
    norm_center_to_mid = np.linalg.norm(center_to_mid_wrist)

    angle = math.degrees(math.acos(dot_product / (norm_wrist * norm_center_to_mid)))

    # Afficher l'orientation
    print(f"Angle entre la wrist line et le centre de la main : {angle:.2f}°")

        # Calculer le milieu de la wrist line
    mid_wrist = (
        (wrist_point1[0] + wrist_point2[0]) // 2,
        (wrist_point1[1] + wrist_point2[1]) // 2
    )

    # Dessiner la flèche partant du centre de la main vers le milieu de la wrist line
    vector_arrow = (mid_wrist[0] - center_hand[0], mid_wrist[1] - center_hand[1])

    # Calculer l'angle entre la flèche et l'axe vertical (vers le bas)
    vertical_axis = np.array([0, -1])  # Direction de l'axe Y négatif (vers le bas)

    # Calcul du produit scalaire entre les deux vecteurs
    dot_product = np.dot(vector_arrow, vertical_axis)

    # Calcul des normes des vecteurs
    norm_arrow = np.linalg.norm(vector_arrow)
    norm_y = np.linalg.norm(vertical_axis)

    # Calcul de l'angle entre les deux vecteurs en radians
    cos_angle = dot_product / (norm_arrow * norm_y)
    angle_radians = math.acos(cos_angle)

    # Convertir l'angle en degrés
    angle_degrees = math.degrees(angle_radians)

    # Vérifier le sens (trigo ou horaire) en utilisant le produit vectoriel 2D
    # Si le produit vectoriel est positif, le vecteur flèche est dans le sens trigonométrique (antihoraire)
    cross_product = vector_arrow[0] * vertical_axis[1] - vector_arrow[1] * vertical_axis[0]

    if cross_product > 0:
        print(f"L'angle dans le sens trigonométrique est {angle_degrees:.2f}°")
        hand_orientation = "Left"
    else:
        print(f"L'angle dans le sens trigonométrique est {-angle_degrees:.2f}°")
        angle_degrees = -angle_degrees
        hand_orientation = "Right"
    
    # Convertir l'angle en degrés
    if angle_degrees > 0 :
        rotation_angle = 180 - angle_degrees
    else: 
        rotation_angle = -180 - angle_degrees  # Si la flèche pointe vers le haut, la rotation doit être dans ce sens
    # Obtenir les dimensions de l'image
    (h, w) = hand_segmented_original.shape[:2]

    # Calculer le centre de l'image
    center = (w // 2, h // 2)

    # Créer la matrice de rotation
    M = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)

    # Ajouter une dimension pour les points et appliquer la matrice de rotation
    points = np.array([wrist_point1, wrist_point2,  center_hand])  # (N, 2)
    points_rotated = np.dot(
        np.hstack([points, np.ones((3, 1))]), 
        M.T
    ) 

    # Points après rotation
    wrist_point1 = points_rotated[0].astype(int)
    wrist_point2 = points_rotated[1].astype(int)
    center_hand = points_rotated[2].astype(int)

    return  mid_wrist, wrist_points, center_hand, M
    
def apply_rotation(flux_video, image_binaire, paume,  mid_wrist, wrist_points, h, w,center_hand,M):
    # Calculer le centre de l'image

    image_rotated = cv2.warpAffine(image_binaire, M, (w, h))
    image_rotated = np.where(image_rotated > 0,1,0).astype(np.uint8)
    

    palm_segmented = cv2.warpAffine(paume, M, (w, h))
    flux_video = cv2.warpAffine(flux_video, M, (w, h))
    # Appliquer la rotation directement sur mid_wrist
    coordonates_mid_wrist = np.dot(M[:, :2], mid_wrist) + M[:, 2]
    image_rotated[int(coordonates_mid_wrist[1]):h,:] = 0
    image_rotated = np.where(image_rotated == 1 , 1,0).astype(np.uint8)

    return flux_video, image_rotated, palm_segmented, coordonates_mid_wrist, wrist_points, center_hand
