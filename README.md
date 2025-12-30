# Face Recognition Attendance System

A secure, real-time attendance system using Flask and Face-API.js.

## Features
- **Real-time Face Recognition**: Uses `face-api.js` to detect and recognize faces in the browser.
- **Attendance Marking**: Automatically marks attendance when a registered student is matched.
- **Admin Dashboard**: View statistics, recent attendance, and manage students.
- **Reporting**: Export attendance logs to CSV.
- **Secure Authentication**: Login system for administrators/teachers.

## Technlogies
- **Backend**: Flask (Python), SQLAlchemy
- **Frontend**: HTML5, Tailwind CSS, JavaScript (face-api.js)
- **Database**: SQLite (default)

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Models**
   The system requires AI models. Run the included script:
   ```bash
   python download_models.py
   ```
   *Note: This downloads weights to `static/models/`*

3. **Run the Application**
   ```bash
   python app.py
   ```
   The app will start at `http://127.0.0.1:5000`.

## Usage
1. Login with default credentials:
   - **Username**: `admin`
   - **Password**: `admin123`
2. Go to **Students** to add a new student. You will need to capture their face data.
3. Go to **Mark Attendance** to start the camera and mark attendance.

## Deployment
This project is ready for deployment on platforms like Vercel or Heroku.
- Ensure `requirements.txt` is up to date.
- Set a secure `SECRET_KEY` in `app.py`.

## License
MIT
