import cv2
import numpy as np

def jeu(haut, bas, gauche, droite):
    width, height = 1000, 1000
    pas = 30
    blanc = (255, 255, 255)
    rouge = (0, 0, 255)
    vert = (0, 255, 0)
    radius = 20

    # Position initiale de la boule (variable statique pour conserver la position)
    if not hasattr(jeu, "x"):
        jeu.x, jeu.y = width // 2, height // 2

    # Déplacer la boule en fonction des booléens
    if haut:
        jeu.y = max(jeu.y - pas, radius)
    if bas:
        jeu.y = min(jeu.y + pas, height - radius)
    if gauche:
        jeu.x = max(jeu.x - pas, radius)
    if droite:
        jeu.x = min(jeu.x + pas, width - radius)

    # Créer une image blanche
    frame = np.full((height, width, 3), blanc, dtype=np.uint8)

    # Dessiner la boule rouge
    cv2.circle(frame, (jeu.x, jeu.y), radius, rouge, -1)

    # Afficher l'image
    cv2.imshow("Jeu", frame)

    # Attendre une touche (si nécessaire) ou fermer avec 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
