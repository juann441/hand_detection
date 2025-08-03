import cv2
import numpy as np
from tkinter import Tk, Label, Button, Scale, HORIZONTAL, Frame

def launch_hsv_adjuster_dynamic():
    lower_skin = np.array([0, 56, 50])
    upper_skin = np.array([28, 255, 255])
    running = True

    def update_image():
        """Mise à jour de l'image en fonction des curseurs."""
        nonlocal running, lower_skin, upper_skin

        if not running:
            return

        ret, frame = video_capture.read()
        if not ret:
            print("Erreur : Impossible de lire la caméra.")
            validate_settings()  # Arrêter proprement
            return

        # Conversion de l'image en HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, lower_skin, upper_skin)
        
        result = cv2.bitwise_and(frame, frame, mask=mask)
        mask_bin = np.where(mask > 0, 255, 0).astype(np.uint8)
        mask_bin = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        # Afficher l'image dans une seule fenêtre
        combined = np.hstack((mask_bin, result))  # Combine les deux images côte à côte
        cv2.imshow("Ajustement HSV (Appuyez sur 'q' pour quitter)", combined)

        # Quitter si 'q' est pressé
        if cv2.waitKey(1) & 0xFF == ord('q'):
            validate_settings()

        # Mise à jour continue
        root.after(30, update_image)

    def update_hsv(_):
        """Mise à jour des plages HSV en fonction des curseurs."""
        nonlocal lower_skin, upper_skin
        h = h_scale.get()
        s = s_scale.get()
        v = v_scale.get()
        h_range = h_range_scale.get()
        s_range = s_range_scale.get()
        v_range = v_range_scale.get()
        lower_skin = np.array([max(0, h), max(0, s), max(0, v)])
        upper_skin = np.array([min(180, h + h_range), min(255, s + s_range), min(255, v + v_range)])

    def reset_to_default():
        """Réinitialiser les curseurs et plages HSV aux valeurs par défaut."""
        nonlocal lower_skin, upper_skin
        h_scale.set(0)
        s_scale.set(56)
        v_scale.set(50)
        h_range_scale.set(28)
        s_range_scale.set(255)
        v_range_scale.set(255)
        lower_skin = np.array([0, 56, 50])
        upper_skin = np.array([28, 255, 255])

    def validate_settings():
        """Fermer proprement la fenêtre et la caméra."""
        nonlocal running
        running = False
        root.quit()
        root.destroy()

    # Initialisation de la caméra
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Erreur : Impossible d'ouvrir la caméra.")
        return None, None

    # Interface Tkinter
    root = Tk()
    root.title("Réglage dynamique HSV")

    slider_frame = Frame(root)
    slider_frame.pack(side="left", padx=10, pady=10)

    def create_slider(label, from_, to, command):
        Label(slider_frame, text=label).pack()
        scale = Scale(slider_frame, from_=from_, to=to, orient=HORIZONTAL, command=command)
        scale.pack()
        return scale

    # Curseurs HSV
    h_scale = create_slider("Hue", 0, 180, update_hsv)
    s_scale = create_slider("Saturation", 0, 255, update_hsv)
    v_scale = create_slider("Value", 0, 255, update_hsv)
    h_range_scale = create_slider("Hue Range", 0, 100, update_hsv)
    s_range_scale = create_slider("Saturation Range", 0, 255, update_hsv)
    v_range_scale = create_slider("Value Range", 0, 255, update_hsv)

    # Boutons
    Button(slider_frame, text="Réinitialiser", command=reset_to_default).pack(pady=10)
    Button(slider_frame, text="Valider", command=validate_settings).pack(pady=10)

    # Lancer la mise à jour des images
    update_image()
    root.mainloop()

    # Libérer les ressources
    video_capture.release()
    cv2.destroyAllWindows()

    return lower_skin, upper_skin

