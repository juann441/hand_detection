# 🖐️ Hand Segmentation and Gesture Recognition

> Final-year engineering project | CPE Lyon – Major Project 2024–2025  
> Authors: Guillaume Brussieux, Juan Reyes-Ortiz  
> Supervisor: Marion Foare

## 📌 Project Overview

This project aims to implement a robust **hand segmentation and gesture recognition** system based on traditional image processing techniques. The application can serve various use cases, including:

- Gesture-controlled interfaces  
- Sign language translation  
- Lightweight alternatives to AI-based detectors

The pipeline focuses on precise **geometric segmentation** of the hand and identification of **key anatomical parts** (fingers, palm, wrist), followed by **gesture classification** based on these structural features.

---

## 🛠️ Technologies Used

- **Python 3**
- **OpenCV** – for image processing and real-time camera capture  
- **NumPy** – for matrix operations  
- **Tkinter** – for the GUI interface

---

## 📷 Pipeline Summary

1. **HSV Thresholding**: Detect hand by color segmentation from a uniform background  
2. **Distance Map + Palm Circle**: Locate the palm center  
3. **Wrist Line Detection**: Separate wrist from palm  
4. **Finger Detection**: Use contour analysis and bounding boxes  
5. **Rotation Correction**: Normalize hand orientation  
6. **Gesture Recognition**: Based on number of fingers, thumb angle, symmetry

---

## 💡 Key Features

- Real-time camera feed processing  
- User-adjustable HSV thresholds for calibration  
- Detection of hand parts: wrist, palm, fingers  
- Gesture classification based on geometric rules  
- Lightweight algorithm, no deep learning required

---

## ⚠️ Limitations

- Requires **uniform background** for HSV-based segmentation  
- Cannot handle **deformed hands** or **multiple axes of rotation**  
- Performance decreases when multiple fingers are **stuck together**  
- Not robust to extreme variations in lighting or hand size (e.g. children, laborers)

---

## 🚀 Future Improvements

- Integrate custom **calibration step** for each user  
- Replace HSV segmentation with **machine learning-based skin detection**  
- Add **temporal smoothing** to improve gesture stability  
- Improve robustness to background and lighting

---

## 📂 Repository Structure

