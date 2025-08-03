import numpy as np
import cv2
from scipy import ndimage

def segmentation(image_rotated, palm_segmented):
    fingers_segmented = (np.where(image_rotated > 0,1,0) - np.where(palm_segmented > 0,1,0))
    fingers_segmented = np.where(fingers_segmented < 0 , 0,fingers_segmented).astype(np.uint8)

    return fingers_segmented

def labelisation(fingers_segmented,pixels_of_hand):
    num_labels, labeled_image, stats, centroids = cv2.connectedComponentsWithStats(fingers_segmented, connectivity=4)

    # Création d'un dictionnaire pour stocker les tailles par label
    label_sizes = {}

    # Seuil minimal pour la taille d'un doigt en pixels (à ajuster selon tes observations)
    MIN_FINGER_SIZE = 0.02  # Par exemple, 5% de la taille de la main totale
    MAX_FINGER_SIZE = 0.30
    # Parcours des objets et filtrage
    for label in range(1, num_labels):  # Commence à 1 car 0 est le fond
        size = stats[label, cv2.CC_STAT_AREA]  # Taille de l'objet
        relative_size = size / pixels_of_hand  # Calcul de la taille relative par rapport à la taille totale de la main

        if MAX_FINGER_SIZE >relative_size > MIN_FINGER_SIZE:  # Conserver uniquement les objets dont la taille relative est supérieure au seuil
            label_sizes[label] = size
        else:  # Supprimer les objets trop petits
            labeled_image[labeled_image == label] = 0  # Remplacer cet objet par 0 (fond)

    # Re-labellisation des objets restants pour éviter des indices non consécutifs
    num_labels, labeled_image, stats, centroids = cv2.connectedComponentsWithStats(labeled_image.astype(np.uint8))

    centroids = []

    # Trouver les coordonnées du centre de masse de chaque objet et afficher la taille en pixels
    for i in range(1, num_labels + 1):
        # Extraire l'objet i
        obj = np.where(labeled_image == i, 1, 0)

        # Vérifier si l'objet n'est pas un pixel seul
        if obj.sum() > 200:
            # Trouver le centre de masse de l'objet i
            centroid = ndimage.center_of_mass(obj)
            # Inverser les coordonnées pour les afficher correctement
            centroid = (int(centroid[1]), int(centroid[0]))
            centroids.append(centroid)

            # Calcul de la taille de l'objet en pixels (aire de l'objet)
            size_in_pixels = obj.sum()  # Nombre de pixels de l'objet

    return num_labels, labeled_image, stats, centroids


def filter_background(num_labels, labeled_image):
    centroids = []
    # Trouver les coordonnées du centre de masse de chaque objet et afficher la taille en pixels
    for i in range(1, num_labels + 1):
        # Extraire l'objet i
        obj = np.where(labeled_image == i, 1, 0)

        # Vérifier si l'objet n'est pas un pixel seul
        if obj.sum() > 200:
            # Trouver le centre de masse de l'objet i
            centroid = ndimage.center_of_mass(obj)
            # Inverser les coordonnées pour les afficher correctement
            centroid = (int(centroid[1]), int(centroid[0]))
            centroids.append(centroid)

    return centroids

