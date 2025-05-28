# 👋 GestureIQ — Gesture-Based Presentation Control System

**GestureIQ** is a smart, contact-free presentation controller that uses real-time hand gesture recognition to navigate slides. It eliminates the need for traditional hardware like remote clickers or keyboards, providing a seamless and professional experience — perfect for classrooms, boardrooms, and public speaking events.

---

## 🚀 Overview

In traditional presentation setups, speakers rely on physical tools like keyboards or clickers, which can disrupt flow, limit movement, and introduce hygiene concerns. GestureIQ solves this with:

- 📷 **Webcam-based gesture detection**  
- 🧠 **ML-powered intent classification**  
- 🌐 **Interactive Flask web interface**

### ✋ Supported Gestures
- **Swipe Left** → Next Slide  
- **Swipe Right** → Previous Slide  
- **Zoom In** → Magnify Content  
- **Pointing** → Highlight or Focus

---

## 🛠️ Built With

- **Python**
- **MediaPipe** – for hand tracking & gesture detection  
- **Scikit-learn** / **TensorFlow** – for gesture classification  
- **Flask** – to serve the web interface  
- **HTML/CSS/JavaScript** – responsive UI 

---

## 📂 Project Structure
```
├── app.py # Flask backend and gesture processing
├── models/ # Trained ML models
├── static/ # CSS, JS, and assets
├── templates/ # HTML templates (index.html, etc.)
├── requirements.txt # Dependencies
```


---

## ⚙️ Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2️⃣ Install Dependencies
Make sure you have Python 3.8+ and pip installed.

```bash

pip install -r requirements.txt
```
### 3️⃣ Run the App
```bash

python app.py
```
---

## 🎯 Use Cases
Teachers & lecturers in smart classrooms

Corporate speakers in touchless environments

Tech demos and AI-based interactions

Enhanced accessibility for people with mobility limitations

---

## 📸 Demo Preview
A clean, responsive web interface powered by Flask.

---

## ✅ Future Improvements
Add more customizable gestures

Expand to support other languages and platforms

Improve classification accuracy with deeper ML models

---

## 🙌 Acknowledgments
MediaPipe

Flask

OpenCV, Scikit-learn, and the open-source community ❤️
