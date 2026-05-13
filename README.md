# CareerPulse AI 🚀
### Automated Placement Assistance for Training Institutes

CareerPulse AI is a full-stack platform designed to automate the process of finding and notifying students about relevant job opportunities in AI and Data Science.

## 🌟 Features
- **Admin Dashboard**: Manage HR personnel and oversee platform activity.
- **HR Dashboard**: Enroll students and manage their skill profiles.
- **Student Dashboard**: Discover curated job opportunities matched to individual skills.
- **Automated Scraping**: Daily job aggregation from top remote job boards.
- **Personalized Alerts**: Automated email notifications sent to students based on their skills.
- **Cloud Automation**: GitHub Actions workflow for daily scraping and mailing at 1:00 PM IST.

## 🛠️ Tech Stack
- **Frontend**: React (Vite), Tailwind CSS, Framer Motion, Lucide React.
- **Backend**: FastAPI (Python), MongoDB (Motor/AsyncIO).
- **Automation**: GitHub Actions, BeautifulSoup4.
- **Styling**: Modern, premium design with dark mode and glassmorphism.

## 📂 Project Structure
```text
├── backend/            # FastAPI application
│   ├── routers/        # API endpoints (Auth, Admin, HR, Jobs)
│   ├── core/           # Security and config
│   └── database.py     # MongoDB connection logic
├── frontend/           # React + Vite application
│   └── src/            # Components, Pages, and Hooks
├── automation/         # Scraping and Mailing scripts
└── .github/workflows/  # Daily automation schedule
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js & NPM
- MongoDB (Local or Atlas)

### Backend Setup
1. Navigate to the backend or root.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example`:
   ```env
   MONGO_URI=mongodb://localhost:27017
   SECRET_KEY=your_secret_key
   SMTP_USER=your_email@gmail.com
   SMTP_PASS=your_app_password
   ```
4. Start the server:
   ```bash
   python -m backend.main
   ```

### Frontend Setup
1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

### Automation
To run the scraper manually:
```bash
python automation/daily_job.py
```

## 📝 License
This project is for training institute placement automation.

---
Built with ❤️ for CareerPulse AI.
