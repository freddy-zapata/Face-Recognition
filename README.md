# 🧠 Identity Access Ecosystem with Facial Recognition

This repository contains the **source code, technical documentation, and auxiliary files** for a **facial recognition–based access control system**, developed as part of the **Bachelor’s Thesis in Information Technology Engineering – PUCE 2025**.  

The system integrates **Raspberry Pi**, **Flask**, **OpenCV**, **face_recognition**, and **PostgreSQL**, implementing a **three-tier client-server architecture** that enables real-time identification, data storage, and visualization of access events through biometric facial authentication.  

---

## 📁 Repository Structure
```
Repository/
├── Face Recognition/ # Main system module
│   ├── capture.py # Script for dataset creation
│   ├── training.py # Script for encoding and training
│   ├── recognition.py # Real-time facial recognition script
│   ├── database.py # PostgreSQL connection
│   │
│   ├── static/ # Static assets (JS, CSS, images)
│   │   ├── crud.js
│   │   ├── script_mejor.js
│   │   ├── style.css
│   │   ├── style_crud.css
│   │   └── default.png
│   └── templates/ # Web frontend (HTML files)
│       ├── index.html
│       └── crud.html
│    
├── Database/ # PostgreSQL database backup
│   └── backup.sql
│
├── Raw Data/ # Test results and datasets
│   └── raw_data.xlsx
│
├── README.md # This file
└── .gitignore # Git exclusions
```
## ⚙️ System Description

The system was designed using a **three-tier client-server architecture**, consisting of:  

- **Presentation Layer (Frontend):** Developed with **HTML, CSS, JavaScript, and Bootstrap**, providing a responsive web interface for real-time monitoring and user management (CRUD).  
- **Logic Layer (Backend):** Implemented with **Flask**, exposing a RESTful API that manages communication between the recognition module, the database, and the web interface.  
- **Data Layer:** Managed with **PostgreSQL**, storing personal data, facial encodings (BYTEA), and access logs including timestamps and images.  

---

## 🔧 Requirements

**Hardware:**  
- Raspberry Pi 4 (8 GB RAM)  
- PiCamera Module v1 or higher  

**Software & Libraries:**  
- Python 3.10+  
- Flask 3.1.0  
- OpenCV 4.11.0  
- face_recognition 1.3.0  
- psycopg2  
- NumPy 2.2.4  
- imutils 0.5.4  
- PostgreSQL 15+  
- Picamera2 0.3.24
---

## 🧩 Main Scripts

| Script | Description |
|--------|--------------|
| `capture.py.py` | Creates folders per person, captures face images, and builds the training dataset. |
| `training.py` | Generates facial encodings and stores them in the database. |
| `recognition.py` | Performs real-time facial recognition and records access events. |

---

## 🧪 Testing

The system was tested under various real-world conditions to evaluate its performance:  
- **Angular variations** of the face  
- **Variable lighting conditions**  
- **Accessories** such as glasses, hats, and masks  

Performance metrics include **recognition rate**, **average detection time**, and **false negative rate**, all available in the [`Raw Data/`](./Raw%20Data/) directory.  

---

## 🌐 Web Interface

The web interface updates automatically every few seconds, displaying:  
- Name, surname, role, and registered photo of the recognized individual  
- Date and time of access  
- Captured image of unknown individuals for logging and auditing  

All frontend resources can be found in the [`templates/`](./Face%20Recognition/templates) and [`static/`](./Face%20Recognition/static) directories.  

---

## 📎 Additional Files

- **Database Backup:** [`Database/backup_faceaccess.sql`](./Database/backup.sql)  
- **Test Data:** Results and metrics in [`Raw Data/`](./Raw%20Data/)  

---

## 🧠 Credits

Developed by **Freddy Alejandro Zapata Armas**  
**Pontificia Universidad Católica del Ecuador – Faculty of Engineering**  
Bachelor’s Thesis: *“Identity Access Ecosystem Prototype with Facial Recognition”*  
Quito, Ecuador – 2025  
