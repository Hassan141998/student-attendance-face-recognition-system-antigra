import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Student, Attendance
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
database_url = os.environ.get('DATABASE_URL', 'sqlite:///attendance.db')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_view = 'login'

# Enable error propagation to see errors in Vercel logs
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.errorhandler(500)
def internal_error(error):
    return f"GLOBAL 500 ERROR: {str(error)}", 500

@app.errorhandler(Exception)
def unhandled_exception(e):
    return f"UNHANDLED EXCEPTION: {str(e)}", 500

@app.route('/debug')
def debug():
    return jsonify({
        'status': 'online',
        'db_url': app.config.get('SQLALCHEMY_DATABASE_URI', '').split('@')[-1] if app.config.get('SQLALCHEMY_DATABASE_URI') else 'None',
        'models_loaded': True
    })

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables manually first time if deemed necessary, 
# or use flask shell. For now, we'll do it on first request or main.

# Database creation logic moved to main block

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('dashboard'))
            flash('Invalid username or password')
        except Exception as e:
            flash(f"System Error: {str(e)}")
    try:
        return render_template('login.html')
    except Exception as e:
        return f"CRITICAL RENDER ERROR: {str(e)}", 500

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    today = datetime.utcnow().date()
    total_students = Student.query.count()
    present_today = Attendance.query.filter_by(date=today, status='Present').count()
    # Assuming absent = total - present for simplicity, or complex query if we track 'Absent' explicitly
    absent_today = total_students - present_today 
    attendance_rate = 0
    if total_students > 0:
        attendance_rate = round((present_today / total_students) * 100, 1)

    recent_attendance = Attendance.query.order_by(Attendance.time.desc()).limit(10).all()
    
    return render_template('dashboard.html', 
                           total_students=total_students, 
                           present_today=present_today, 
                           absent_today=absent_today,
                           attendance_rate=attendance_rate,
                           recent_attendance=recent_attendance)

@app.route('/students')
@login_required
def students():
    all_students = Student.query.all()
    return render_template('students.html', students=all_students)

@app.route('/api/students', methods=['POST'])
@login_required
def add_student():
    data = request.json
    name = data.get('name')
    roll_number = data.get('roll_number')
    email = data.get('email')
    face_descriptor = data.get('face_descriptor') # List/Array from JS
    profile_image = data.get('profile_image')  # Base64 encoded image

    if Student.query.filter_by(roll_number=roll_number).first():
        return jsonify({'error': 'Roll number already exists'}), 400
    
    new_student = Student(
        name=name, 
        roll_number=roll_number, 
        email=email,
        face_encoding=json.dumps(face_descriptor),
        profile_image=profile_image
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student added successfully'})

@app.route('/api/students/all', methods=['GET'])
def get_all_students_descriptors():
    # Public or protected endpoint to get descriptors for face matching on client
    # For security, you might want to protect this, but client-side matching needs access
    students = Student.query.all()
    data = []
    for s in students:
        if s.face_encoding:
            data.append({
                'id': s.id,
                'name': s.name,
                'descriptor': json.loads(s.face_encoding)
            })
    return jsonify(data)

@app.route('/attendance')
@login_required
def attendance_page():
    return render_template('attendance.html')

@app.route('/api/attendance', methods=['POST'])
@login_required
def mark_attendance():
    data = request.json
    student_id = data.get('student_id')
    photo = data.get('photo')  # Base64 encoded photo
    detected_objects = data.get('detected_objects')  # JSON array of objects
    
    # Check if already marked for today
    today = datetime.utcnow().date()
    existing = Attendance.query.filter_by(student_id=student_id, date=today).first()
    
    if existing:
        return jsonify({'message': 'Attendance already marked', 'status': 'duplicate'}), 200

    new_attendance = Attendance(
        student_id=student_id, 
        status='Present', 
        date=today, 
        time=datetime.utcnow().time(),
        photo=photo,
        detected_objects=json.dumps(detected_objects) if detected_objects else None
    )
    db.session.add(new_attendance)
    db.session.commit()
    
    return jsonify({'message': 'Attendance marked successfully', 'status': 'success'})

@app.route('/reports')
@login_required
def reports():
    date_str = request.args.get('date')
    if date_str:
        filter_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        records = Attendance.query.filter_by(date=filter_date).all()
    else:
        records = Attendance.query.all()
    return render_template('reports.html', records=records)

from sqlalchemy import text

# Special endpoint for one-time database initialization
@app.route('/init-db')
def init_database():
    """Call this endpoint once to initialize database tables and admin user"""
    try:
        with app.app_context():
            db.create_all()
            
            # Manually add new columns if they don't exist (SQLAlchemy won't add them to existing tables)
            try:
                db.session.execute(text('ALTER TABLE student ADD COLUMN IF NOT EXISTS profile_image TEXT'))
                db.session.execute(text('ALTER TABLE attendance ADD COLUMN IF NOT EXISTS photo TEXT'))
                db.session.execute(text('ALTER TABLE attendance ADD COLUMN IF NOT EXISTS detected_objects TEXT'))
                db.session.commit()
            except Exception as sql_e:
                print(f"Migration note: {str(sql_e)}")
                # If IF NOT EXISTS is not supported or other issue, we continue
                db.session.rollback()

            # Create default admin user if not exists
            if not User.query.filter_by(username='admin').first():
                admin = User(username='admin', password=generate_password_hash('admin123'))
                db.session.add(admin)
                db.session.commit()
                return jsonify({'message': 'Database initialized successfully! Admin user created (admin/admin123)'}), 200
            return jsonify({'message': 'Database tables updated. Admin user already exists.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
