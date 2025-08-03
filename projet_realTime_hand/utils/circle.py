import numpy as np

def find_inner_circle(image, center):
    """
    Trouve le rayon du cercle interne maximal dans une région binaire.

    Args:
        image (np.array): Image binaire (0 = noir, 1 = blanc).
        center (tuple): Coordonnées du point central (x, y).

    Returns:
        int: Rayon maximal du cercle interne.
    """
    x_c, y_c = center
    max_radius = 0
    height, width = image.shape

    # Augmenter graduellement le rayon
    while True:
        # Créer un masque circulaire pour le rayon actuel
        y, x = np.ogrid[:height, :width]
        mask = (x - x_c) ** 2 + (y - y_c) ** 2 <= max_radius ** 2

        # Vérifier si le masque intersecte des pixels noirs
        if np.any(image[mask] == 0):  # Si un pixel noir est trouvé
            break  # Arrêter la croissance du rayon

        max_radius += 1  # Augmenter le rayon

    return max_radius - 1  # Retourner le rayon maximal avant intersection

def sample_points_on_circle(center, radius, step):
    """
    Échantillonne des points uniformément espacés sur un cercle.

    Args:
        center (tuple): Coordonnées (x, y) du centre du cercle.
        radius (int): Rayon du cercle.
        step (int): Pas d'échantillonnage en degrés (par défaut 10).

    Returns:
        list: Liste des points (x, y) échantillonnés sur le cercle.
    """
    points = []
    for angle in range(0, 360, step):
        x = int(center[0] + radius * np.cos(np.radians(angle)))
        y = int(center[1] + radius * np.sin(np.radians(angle)))
        points.append((x, y))
    return points

def find_nearest_boundary_point(image, x, y):
    """
    Trouve le point de contour le plus proche pour un point donné.
    Args:
        image (np.array): Image binaire (0 = noir, 1 = blanc).
        x, y (int): Coordonnées du point de départ.

    Returns:
        tuple: Coordonnées (x, y) du point de contour trouvé.
    """
    height, width = image.shape
    rad = 1  # Rayon initial de recherche

    while rad < max(height, width):
        for angle in range(0, 360, 1):  # Parcours angulaire
            x_search = int(x + rad * np.cos(np.radians(angle)))
            y_search = int(y + rad * np.sin(np.radians(angle)))
            
            if 0 <= x_search < width and 0 <= y_search < height:
                # Vérifie si c'est un point de contour
                if image[y_search, x_search] == 0 and any(
                    0 <= y_search + dy < height and 0 <= x_search + dx < width and
                    image[y_search + dy, x_search + dx] == 1
                    for dx, dy in [(-1, -1), (-1, 0), (-1, 1),
                                   (0, -1),        (0, 1),
                                   (1, -1), (1, 0), (1, 1)]
                ):
                    return (x_search, y_search)

        rad += 1  # Augmenter le rayon de recherche
    return None  # Aucun point trouvé
