# 🏥 OPRA Health — AI-Powered Women's Health & Wellness Platform

> A full-stack Django web application with an Android mobile backend that combines **facial emotion recognition**, **AI-based disease prediction**, **personalized diet planning**, and **real-time chat** — all focused on women's health and well-being.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [AI & ML Models](#-ai--ml-models)
- [API Endpoints](#-api-endpoints)
- [Database Models](#-database-models)
- [Installation & Setup](#-installation--setup)
- [Configuration](#-configuration)
- [Admin Panel](#-admin-panel)
- [Mobile App Integration](#-mobile-app-integration)
- [Notes & Limitations](#-notes--limitations)

---

## 🌟 Overview

**OPRA Health** is an intelligent health monitoring platform built with Django. It serves as the backend for both a web admin panel and a Flutter/Android mobile application. The system leverages multiple AI/ML models to provide:

- **Real-time facial emotion analysis** from uploaded images
- **Symptom-based disease prediction** using classical ML algorithms
- **Personalized diet plan recommendations** using a RandomForest model
- **Text-based sentiment/emotion detection** using a fine-tuned RoBERTa transformer model
- **In-app chat**, complaint management, and feedback systems

---

## ✨ Features

### 👩 User (Mobile App)
| Feature | Description |
|---|---|
| 📝 Registration & Login | Email-based user registration with group-based auth |
| 👤 Profile Management | View and edit personal profile including photo upload |
| 😊 Facial Emotion Detection | Upload a photo → AI predicts one of 7 emotions |
| 🤒 Disease Prediction | Select symptoms → ML model predicts likely disease |
| 🥗 Diet Planning | Health parameters → Personalized meal plan (morning/noon/evening/night) |
| 💬 Real-time Chat | Chat with admin/support (bidirectional message history) |
| 📣 Complaints | Submit complaints and view admin replies |
| ⭐ Feedback | Submit feedback to the admin |
| 🔑 Forgot Password | Reset password via email (OTP sent via Gmail SMTP) |

### 🛡️ Admin (Web Panel)
| Feature | Description |
|---|---|
| 🏠 Dashboard | Admin home overview |
| 👥 User Management | View all registered users |
| 📋 Complaint Management | View complaints and send replies |
| 💬 Feedback Viewer | Browse all user feedback |
| 🔐 Password Management | Change admin password, forgot password via email |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | Django 5.2.4 |
| **Database** | MySQL |
| **Authentication** | Django Auth with Group-based roles (`admin`, `users`) |
| **Computer Vision** | OpenCV (`cv2`), PyTorch, TorchVision, PIL |
| **Facial Emotion Model** | ResNet-18 (fine-tuned, `.pth`) — 7 emotion classes |
| **Text Emotion Model** | RoBERTa (`RobertaForSequenceClassification`) — 7 emotion classes |
| **Disease Prediction** | scikit-learn (Decision Tree, Random Forest, KNN, SVM, Naive Bayes) |
| **Diet Prediction** | scikit-learn MultiOutputClassifier + RandomForest |
| **Email** | Gmail SMTP (smtplib) |
| **Frontend (Admin)** | HTML, Bootstrap 5, SCSS, jQuery, OwlCarousel |
| **Mobile Backend** | REST-style JSON APIs (for Flutter/Android) |
| **Static Assets** | Bootstrap 5, WOW.js, Animate.css, jQuery |

---

## 📁 Project Structure

```
opra/
├── manage.py                        # Django management script
├── .gitignore                       # Git ignore rules
│
├── opra/                            # Django project settings
│   ├── settings.py                  # Project configuration (DB, media, static)
│   ├── urls.py                      # Root URL configuration
│   ├── asgi.py
│   └── wsgi.py
│
├── myapp/                           # Main Django application
│   ├── models.py                    # Database models
│   ├── views.py                     # All view logic + AI inference
│   ├── urls.py                      # URL routing
│   ├── admin.py                     # Django admin registration
│   ├── apps.py
│   │
│   ├── emotion.py                   # Webcam-based FER emotion detector (standalone script)
│   ├── facial_emo.py                # ResNet-18 training script for facial emotion
│   ├── facial_emo_predict.py        # Prediction utility using trained ResNet-18
│   ├── health.py                    # Diet plan RandomForest training + prediction
│   │
│   ├── emotion_model/               # Fine-tuned RoBERTa model (text emotion)
│   │   ├── config.json              # Model architecture config
│   │   ├── tokenizer.json           # Tokenizer vocabulary
│   │   ├── vocab.json               # BPE vocabulary
│   │   ├── merges.txt               # BPE merge rules
│   │   ├── model.safetensors        # ⚠️ Model weights (313 MB — excluded from Git)
│   │   ├── checkpoint-56/           # ⚠️ Training checkpoint (excluded from Git)
│   │   └── checkpoint-84/           # ⚠️ Training checkpoint (excluded from Git)
│   │
│   ├── saved_models/
│   │   └── facial_emotion_model.pth # ⚠️ ResNet-18 weights (43 MB — excluded from Git)
│   │
│   ├── static/                      # Static files
│   │   ├── ad/                      # Admin theme (Bootstrap 5, WOW.js, OwlCarousel, SCSS)
│   │   └── chat_style/              # Chat UI static files
│   │
│   ├── migrations/                  # Database migrations
│   ├── captured_faces/              # Runtime: saved face images
│   └── logs/                        # Runtime: application logs
│
├── templates/                       # HTML templates (admin web UI)
│   ├── login.html
│   ├── adminhome.html
│   ├── view_users.html
│   ├── view_complaints.html
│   ├── view_feedback.html
│   ├── send_reply.html
│   ├── change_password.html
│   ├── forgottenpassword.html
│   └── view_review.html
│
└── media/                           # User-uploaded files (profile photos, facial images)
    └── facial_images/
```

---

## 🤖 AI & ML Models

### 1. Facial Emotion Recognition (ResNet-18)
- **Architecture**: `torchvision.models.resnet18` with custom fully-connected layer
- **Classes**: `angry`, `disgust`, `fear`, `happy`, `neutral`, `sad`, `surprise`
- **Input**: 64×64 RGB image
- **Training**: [`facial_emo.py`](myapp/facial_emo.py) — 10 epochs, Adam optimizer, CrossEntropyLoss
- **Inference**: [`views.py`](myapp/views.py) — `predict_emotion()` and `save_facial_emotion()` endpoint
- **Model file**: `myapp/saved_models/facial_emotion_model.pth` *(not in repo — too large)*

### 2. Text Emotion Detection (RoBERTa)
- **Architecture**: `RobertaForSequenceClassification` (HuggingFace Transformers)
- **Classes**: `anger`, `disgust`, `fear`, `joy`, `neutral`, `sadness`, `surprise`
- **Hidden size**: 768, 6 attention layers, 12 heads
- **Config**: [`myapp/emotion_model/config.json`](myapp/emotion_model/config.json)
- **Model weights**: `myapp/emotion_model/model.safetensors` *(not in repo — too large)*

### 3. Disease Prediction (scikit-learn)
- **Algorithms**: Decision Tree, Random Forest (default), KNN (k=3), SVM, Naive Bayes
- **Input**: Binary symptom vector (132 symptoms)
- **Output**: Disease prognosis label
- **Dataset**: `training.csv` (standard medical symptom dataset)
- **Endpoint**: `POST /myapp/predictdiseasebysymptoms/`

### 4. Diet Plan Prediction (RandomForest)
- **Model**: `MultiOutputClassifier(RandomForestClassifier(n_estimators=100))`
- **Input features**: Age, gender, BMI, blood pressure, cholesterol, blood sugar, activity level, dietary preference, medications, allergies, etc.
- **Output**: 4 meals — `morning_diet`, `noon_diet`, `evening_diet`, `night_diet`
- **Training**: [`myapp/health.py`](myapp/health.py)

---

## 🔗 API Endpoints

### Authentication
| Method | URL | Description |
|---|---|---|
| `GET` | `/myapp/login_get/` | Admin login page |
| `POST` | `/myapp/login_post/` | Admin login submit |
| `GET` | `/myapp/logout1/` | Admin logout |
| `POST` | `/myapp/user_login/` | Mobile user login (JSON) |
| `GET` | `/myapp/and_forget_password/` | Web forgot password page |
| `POST` | `/myapp/and_forget_password_post/` | Web password reset via email |
| `POST` | `/myapp/android_forget_password_post/` | Mobile password reset via email |

### Admin Panel
| Method | URL | Description |
|---|---|---|
| `GET` | `/myapp/adminhome/` | Admin dashboard |
| `GET` | `/myapp/view_users/` | View all users |
| `GET` | `/myapp/view_complaints/` | View all complaints |
| `GET` | `/myapp/send_reply/<id>` | Reply to complaint page |
| `POST` | `/myapp/send_reply_post/` | Submit complaint reply |
| `GET` | `/myapp/view_feedback/` | View all feedback |
| `GET` | `/myapp/admin_change_password/` | Change password page |
| `POST` | `/myapp/admin_change_password_post/` | Submit password change |

### Mobile / Flutter APIs (JSON)
| Method | URL | Description |
|---|---|---|
| `POST` | `/myapp/user_register/` | Register new user |
| `POST` | `/myapp/user_view_profile/` | View user profile |
| `POST` | `/myapp/user_edit_profile/` | Edit user profile |
| `POST` | `/myapp/add_complaint/` | Submit a complaint |
| `POST` | `/myapp/woman_view_complaints/` | View user's complaints |
| `POST` | `/myapp/add_feedback/` | Submit feedback |
| `POST` | `/myapp/User_sendchat/` | Send a chat message |
| `POST` | `/myapp/User_viewchat/` | View chat history |
| `POST` | `/myapp/User_sendchat1/` | Send message (alternate) |
| `POST` | `/myapp/User_viewchat1/` | View chat history (alternate) |
| `POST` | `/myapp/save_facial_emotion/` | Upload photo → detect & save emotion |
| `GET` | `/myapp/user_view_symptoms/` | Get full symptom list (132 symptoms) |
| `POST` | `/myapp/predictdiseasebysymptoms/` | Predict disease from symptoms |

---

## 🗄️ Database Models

```python
Users          # Extended user profile (name, email, phone, dob, gender, place, pin, post)
Complaint      # User complaints with admin reply and status
Feedback       # User feedback with date
Workouts       # Workout plans (cardiac, BMI, BP, sugar level, cholesterol filters)
Facial_emotion # Emotion detection logs (date, time, emotion, photo path)
Chat           # Chat messages (from/to user IDs, message, date)
Posts          # User posts (content + photo)
Comments       # Comments on posts
```

**User Roles (Django Groups):**
- `admin` — Web panel access
- `users` — Mobile app access

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- MySQL Server
- pip

### 1. Clone the repository
```bash
git clone https://github.com/FathimaDiyaMuhammedCM/OPRA-HEALTH.git
cd OPRA-HEALTH
```

### 2. Create & activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install django mysqlclient torch torchvision pillow opencv-python \
            scikit-learn pandas numpy transformers joblib seaborn matplotlib
```

### 4. Set up the database
```sql
CREATE DATABASE opra;
```

### 5. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Django groups
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import Group
Group.objects.create(name='admin')
Group.objects.create(name='users')
exit()
```

### 7. Create superuser / admin
```bash
python manage.py createsuperuser
```
Then assign the created user to the `admin` group via Django Admin (`/admin/`).

### 8. Download model weights
The large model files are excluded from this repository. You must obtain and place them manually:

| File | Path | Size |
|---|---|---|
| Facial emotion model | `myapp/saved_models/facial_emotion_model.pth` | ~43 MB |
| RoBERTa weights | `myapp/emotion_model/model.safetensors` | ~313 MB |

### 9. Run the development server
```bash
python manage.py runserver
```

Access the app at: **http://127.0.0.1:8000/myapp/login_get/**

---

## 🔧 Configuration

### `opra/settings.py`

**Database** — Update credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'opra',
        'USER': 'root',
        'PASSWORD': 'your_password',
    }
}
```

**Model Path** — Update in [`views.py`](myapp/views.py) line 432:
```python
MODEL_PATH = "path/to/your/myapp/saved_models/facial_emotion_model.pth"
```

**Disease Dataset Path** — Update in [`views.py`](myapp/views.py) line 525:
```python
data = pd.read_csv('path/to/your/myapp/training.csv')
```

**Email (Gmail SMTP)** — Update credentials in [`views.py`](myapp/views.py):
```python
server.login("your_email@gmail.com", "your_app_password")
```
> ⚠️ Use a Gmail [App Password](https://myaccount.google.com/apppasswords), not your regular password.

---

## 🖥️ Admin Panel

Navigate to **http://127.0.0.1:8000/myapp/login_get/** and log in with admin credentials.

| Page | URL |
|---|---|
| Dashboard | `/myapp/adminhome/` |
| Users | `/myapp/view_users/` |
| Complaints | `/myapp/view_complaints/` |
| Feedback | `/myapp/view_feedback/` |
| Change Password | `/myapp/admin_change_password/` |

---

## 📱 Mobile App Integration

This backend is designed to serve a **Flutter/Android** mobile app. All mobile endpoints return JSON responses in the format:

```json
{ "status": "ok", "data": ... }
{ "status": "error", "message": "..." }
```

CSRF middleware is **disabled** in settings to allow mobile API calls:
```python
# 'django.middleware.csrf.CsrfViewMiddleware',  # disabled
```

> For production, re-enable CSRF and use token-based authentication (e.g., DRF Token Auth or JWT).

---

## ⚠️ Notes & Limitations

- **Large model files** (`*.pth`, `*.safetensors`, `*.pt`) are excluded from this repository due to GitHub's 100 MB file size limit. Place them manually as described above.
- **Hardcoded paths** in `views.py` and `health.py` (e.g., `C:\\Riss\\mithra\\...`) must be updated to your local paths.
- **Debug mode** is currently `True` — set to `False` for production.
- **SECRET_KEY** in `settings.py` should be rotated before any deployment.
- `training.csv` (disease symptom dataset) is required for disease prediction but is not included in the repo.
- `synthetic_health_dataset_with_diet.xlsx` is required for retraining the diet model.

---

## 📄 License

This project is for academic/educational purposes.

---

<p align="center">Built with ❤️ using Django, PyTorch & scikit-learn</p>
