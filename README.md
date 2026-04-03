# PDMS — Predictive Donor Management System

<p align="center">
  <img src="https://img.shields.io/badge/Django-4.x-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Database-SQLite3-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" />
  <img src="https://img.shields.io/badge/UI-TailwindCSS-38B2AC?style=for-the-badge&logo=tailwindcss&logoColor=white" />
</p>

> A full-stack donor management platform for non-profit organisations. Features real-time fundraising dashboards, AI-powered donor propensity scoring, automated tax receipt emails, campaign management, and volunteer tracking — all wrapped in a modern glassmorphism UI.

---

## Table of Contents

- [System Overview](#system-overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Running the System](#running-the-system)
- [Accessing the System](#accessing-the-system)
- [Sample Login Credentials](#sample-login-credentials)
- [URL Reference](#url-reference)
- [Data Models](#data-models)
- [AI Propensity Engine](#ai-propensity-engine)
- [Environment Notes](#environment-notes)

---

## System Overview

PDMS is a Django web application built to intelligently manage donor relationships using predictive AI. It helps non-profit organisations manage fundraising campaigns, track donor giving patterns, and forecast future donations — all from a single operational platform.

The system has two distinct access layers:

| Layer | Audience | URL |
|---|---|---|
| **Public Donation Portal** | Donors, general public | `http://127.0.0.1:8000/` |
| **Admin Management Console** | Staff / administrators | `http://127.0.0.1:8000/admin-dashboard/` |

---

## Key Features

### 🏛️ Admin Console
- **Real-time KPI Dashboard** — Total funds raised, active campaigns, donor count, retention rate
- **Donor Management** — Full CRUD with profile pages, lifetime value tracking, and communication preferences
- **Campaign Management** — Create and track fundraising campaigns with live progress bars
- **Volunteer Tracking** — Manage volunteer profiles, skill sets, campaign assignments, and hours worked
- **Manual Donation Entry** — Record cash/cheque donations with automatic receipt trigger
- **Administrator Accounts** — Invite and manage staff users with role-based access
- **Toast Notifications** — System-wide slide-in success/error messages on all actions

### 🌐 Public Donation Portal
- **Live Campaign Cards** — Browse active campaigns with real-time progress bars
- **Secure Online Donations** — Donate by card or bank transfer, with instant email receipt
- **Donation History Lookup** — Donors can view their contribution history by email
- **Volunteer Registration** — Public sign-up form for new volunteers
- **Contact Channels** — WhatsApp and email integration
- **Fully Mobile-Responsive** — Hamburger nav, responsive grid layouts

### 🤖 AI Propensity Scoring Engine
- Uses **CRISP-DM methodology** with RFM (Recency, Frequency, Monetary) feature extraction
- Trained scikit-learn model stored as `ml_engine/propensity_model.joblib`
- Produces a score from **0.0 (unlikely)** to **1.0 (high likelihood)** of future donation
- Triggered per-donor via the admin dashboard with a "Re-score AI" button
- Scores categorised as: 🔥 High (≥0.8) | Medium (0.5–0.8) | Low (<0.5) | Unscored

---

## Project Structure

```
PDMS/
│
├── manage.py                    # Django management entry point
├── requirements.txt             # Python dependencies
├── db.sqlite3                   # SQLite database (auto-created)
│
├── pdms_config/                 # Django project configuration
│   ├── settings.py              # App settings (DB, auth, sessions, email)
│   ├── urls.py                  # Root URL dispatcher
│   └── wsgi.py                  # WSGI entry point for production
│
├── core_app/                    # Main application module
│   ├── models.py                # Data models: Donor, Campaign, Donation, Volunteer
│   ├── views.py                 # All view logic (donor, campaign, volunteer, auth)
│   ├── forms.py                 # Django ModelForms
│   ├── urls.py                  # App-level URL patterns
│   └── migrations/              # Database migration history
│
├── ml_engine/                   # AI Propensity Scoring Module
│   ├── model_training.py        # Trains and saves the scikit-learn model
│   ├── feature_engineering.py   # RFM feature extraction from donation history
│   ├── scoring_api.py           # Django view wrapper for scoring predictions
│   └── propensity_model.joblib  # Pre-trained model file
│
└── templates/                   # Django HTML templates
    ├── base.html                # ★ Shared admin base (nav, toast, footer)
    ├── public_portal.html       # Public-facing donation page
    ├── admin_dashboard.html     # Main KPI + targeted appeal dashboard
    ├── campaign_dashboard.html  # Campaign list with progress
    ├── campaign_detail.html     # Individual campaign + donor list
    ├── campaign_form.html       # Create/edit campaign form
    ├── campaign_confirm_delete.html
    ├── donor_detail.html        # Donor profile + transaction history
    ├── donor_form.html          # Create/edit donor form
    ├── donor_confirm_delete.html
    ├── volunteer_dashboard.html # Volunteer roster
    ├── volunteer_form.html      # Create/edit volunteer
    ├── admin_user_dashboard.html
    ├── admin_user_form.html     # Create new admin user
    ├── manual_donation.html     # Manual cash/cheque entry form
    └── registration/
        └── login.html           # Premium dark split-screen login
```

---

## Requirements

### System Requirements
- **Python** 3.10 or higher
- **pip** (comes with Python)
- **Git** (optional, for cloning)
- A modern web browser (Chrome, Firefox, Edge)

### Python Dependencies

All dependencies are listed in `requirements.txt`:

```
django>=4.0
pandas>=2.0.0
scikit-learn>=1.2.0
joblib>=1.2.0
```

Install all at once:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install django pandas scikit-learn joblib
```

> **Note:** No virtual environment is strictly required but is recommended for isolation (see setup instructions below).

---

## Installation & Setup

### Option A — With a Virtual Environment (Recommended)

```bash
# 1. Clone or download the project
cd C:\Users\DAVIS\Desktop\PDMS

# 2. Create a virtual environment
python -m venv venv

# 3. Activate it
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
# On Windows (CMD):
venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Apply database migrations
python manage.py migrate

# 6. Create the first superuser (admin account)
python manage.py createsuperuser
```

### Option B — Without a Virtual Environment

```bash
# 1. Navigate to project directory
cd C:\Users\DAVIS\Desktop\PDMS

# 2. Install dependencies globally
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Create a superuser account
python manage.py createsuperuser
```

---

## Running the System

```bash
# Start the development server
python manage.py runserver

# The server will start at:
# http://127.0.0.1:8000/
```

To run on a custom port:

```bash
python manage.py runserver 8080
# Access at: http://127.0.0.1:8080/
```

To allow access from other devices on the same network:

```bash
python manage.py runserver 0.0.0.0:8000
# Access from other devices via your machine's local IP
```

To stop the server, press `Ctrl + C` in the terminal.

---

## Accessing the System

Once the server is running, navigate to any of the following:

### Public Portal
```
http://127.0.0.1:8000/
```
No login required. Visitors can:
- Browse active campaigns and their funding progress
- Make a donation (credit card or bank transfer)
- Look up their personal donation history by email
- Register as a volunteer

### Admin Login
```
http://127.0.0.1:8000/accounts/login/
```
All admin pages require authentication. After login, users are redirected to the dashboard.

> **Session Security:** Admin sessions automatically expire after **15 minutes of inactivity** and on browser close.

---

## Sample Login Credentials

> ⚠️ These are development-only credentials. **Change them before any production deployment.**

### Superuser (Full Access)

| Field | Value |
|---|---|
| **URL** | `http://127.0.0.1:8000/accounts/login/` |
| **Username** | `admin` |
| **Password** | `admin1234` |
| **Access Level** | Superuser — full system access |

### Creating Additional Admins

**Method 1 — Via the Admin Console (recommended):**
1. Log in as superuser
2. Navigate to `http://127.0.0.1:8000/admins/`
3. Click **"Invite Administrator"**
4. Fill in username and password

**Method 2 — Via Terminal:**
```bash
python manage.py createsuperuser
# Follow the prompts for username, email, and password
```

**Method 3 — Create a regular staff user via shell:**
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
User.objects.create_user('staffuser', 'staff@pdms.local', 'securepassword123', is_staff=True)
```

---

## URL Reference

### Public Routes (No Login Required)
| URL | Description |
|---|---|
| `/` | Public donation portal |

### Admin Routes (Login Required)
| URL | Description |
|---|---|
| `/accounts/login/` | Admin login page |
| `/accounts/logout/` | Log out |
| `/admin-dashboard/` | Main KPI dashboard + targeted appeal list |
| `/donors/create/` | Add a new donor |
| `/donors/<id>/` | View donor profile + transaction history |
| `/donors/<id>/update/` | Edit donor record |
| `/donors/<id>/delete/` | Delete donor |
| `/donations/manual/` | Log a manual cash/cheque donation |
| `/campaigns/` | Campaign management list |
| `/campaigns/create/` | Launch a new campaign |
| `/campaigns/<id>/` | View campaign details + contributing donors |
| `/campaigns/<id>/update/` | Edit campaign |
| `/campaigns/<id>/delete/` | Delete campaign |
| `/volunteers/` | Volunteer personnel list |
| `/volunteers/create/` | Register a new volunteer |
| `/volunteers/<id>/update/` | Update volunteer details |
| `/admins/` | Administrator account list |
| `/admins/create/` | Create a new admin user |

### API Routes
| URL | Description |
|---|---|
| `/api/score/<donor_id>/` | Trigger AI propensity score for a donor (returns JSON) |

---

## Data Models

### `Donor`
| Field | Type | Description |
|---|---|---|
| `DonorID` | AutoField (PK) | Primary key |
| `Email` | EmailField (unique) | Donor email — used as identifier |
| `Phone` | CharField | Contact phone number |
| `Address` | TextField | Mailing address |
| `Total_Donated` | DecimalField | Lifetime sum of completed donations |
| `Preferred_Communication` | CharField | EMAIL, PHONE, or MAIL |
| `Propensity_Score` | FloatField (nullable) | AI-generated giving likelihood (0.0–1.0) |

### `Campaign`
| Field | Type | Description |
|---|---|---|
| `CampaignID` | AutoField (PK) | Primary key |
| `Name` | CharField | Campaign name |
| `Target_Amount` | DecimalField | Fundraising goal (Ksh) |
| `Start_Date` | DateField | Campaign start date |
| `End_Date` | DateField **`[indexed]`** | Campaign end date (indexed for active filter) |

### `Donation`
| Field | Type | Description |
|---|---|---|
| `DonationID` | AutoField (PK) | Primary key |
| `DonorID` | ForeignKey → Donor | Linked donor |
| `Amount` | DecimalField | Donation amount (Ksh) |
| `Status` | CharField **`[indexed]`** | PENDING / COMPLETED / FAILED |
| `Payment_Method` | CharField | CC (Credit Card) or BANK |
| `Date` | DateTimeField **`[indexed]`** | Auto-set timestamp |
| `CampaignID` | ForeignKey → Campaign | Campaign (nullable = General Fund) |

### `Volunteer`
| Field | Type | Description |
|---|---|---|
| `VolunteerID` | AutoField (PK) | Primary key |
| `Name` | CharField | Full name |
| `Skills` | TextField | Expertise description |
| `Hours_Worked` | IntegerField | Tracked volunteer hours |
| `CampaignID` | ForeignKey → Campaign | Assigned campaign (nullable) |

---

## AI Propensity Engine

The AI engine uses the **CRISP-DM** data mining methodology to predict which donors are most likely to give again.

### How It Works

```
Donor History → RFM Feature Extraction → Trained Model → Propensity Score (0–1)
```

1. **Feature Engineering** (`ml_engine/feature_engineering.py`)
   - **Recency** — Days since the donor's last donation
   - **Frequency** — Total number of donations made
   - **Monetary** — Average donation value

2. **Model** — Scikit-learn classifier saved as `propensity_model.joblib`

3. **Scoring API** — `GET /api/score/<donor_id>/` returns:
   ```json
   { "donor_id": 5, "propensity_score": 0.87 }
   ```

### Retraining the Model

If you have sufficient donation data, you can retrain the model:

```bash
python manage.py shell
```
```python
from ml_engine.model_training import train_model
train_model()
```

### Scoring All Donors at Once

```bash
python manage.py shell
```
```python
from ml_engine.scoring_api import score_all_donors
score_all_donors()
```

---

## Environment Notes

### Email Configuration

By default, emails (donation receipts) are printed to the terminal console — no SMTP server needed for development.

To configure a real email server for production, update `pdms_config/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your@email.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Production Checklist

Before deploying to a live server:

- [ ] Change `SECRET_KEY` in `settings.py` to a long random string
- [ ] Set `DEBUG = False`
- [ ] Add your domain to `ALLOWED_HOSTS`
- [ ] Switch from SQLite to PostgreSQL or MySQL
- [ ] Configure a real email backend
- [ ] Set up static file serving (whitenoise or Nginx)
- [ ] Use environment variables for all secrets (`.env` + `python-decouple`)

### Database

The system uses **SQLite** by default — the database file is `db.sqlite3` in the project root. It is auto-created when you run `migrate`. No additional database server installation is required for local development.

---

## Common Commands Reference

```bash
# Apply all pending database migrations
python manage.py migrate

# Create a new migration after model changes
python manage.py makemigrations

# Create a superuser interactively
python manage.py createsuperuser

# Open Django interactive shell
python manage.py shell

# Run the development server
python manage.py runserver

# Collect static files (production only)
python manage.py collectstatic

# Check for configuration issues
python manage.py check
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'django'` | Run `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'pandas'` | Run `pip install pandas scikit-learn joblib` |
| Login page shows 404 | Use `/accounts/login/` (not `/login/`) |
| Emails not sending | Expected in dev — receipts print to terminal console |
| Model file not found | Run `train_model()` from the Django shell (see AI section) |
| Port already in use | Run `python manage.py runserver 8080` to use a different port |

---

*Built with ❤️ for non-profit impact. Predictive Donor Management System (PDMS) © 2026.*
