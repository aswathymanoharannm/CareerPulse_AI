from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Student, Job
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///careerpulse.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Initial Setup ---
def init_db():
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        if not User.query.filter_by(email='admin@careerpulse.ai').first():
            # Support both email and the 'admin' identifier requested
            admin = User(
                name='admin',
                email='admin@careerpulse.ai',
                password=generate_password_hash('admin@123', method='pbkdf2:sha256'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('email')
        password = request.form.get('password')
        
        # Check by email or name (for the 'admin' requirement)
        user = User.query.filter((User.email == identifier) | (User.name == identifier)).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'hr':
                return redirect(url_for('hr_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- Admin Dashboard ---
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    hrs = User.query.filter_by(role='hr').all()
    return render_template('admin_dashboard.html', hrs=hrs)

@app.route('/admin/add_hr', methods=['POST'])
@login_required
def add_hr():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if User.query.filter_by(email=email).first():
        flash('HR with this email already exists')
    else:
        new_hr = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            role='hr'
        )
        db.session.add(new_hr)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_hr/<int:id>')
@login_required
def delete_hr(id):
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    hr = User.query.get(id)
    if hr and hr.role == 'hr':
        db.session.delete(hr)
        db.session.commit()
    return redirect(url_for('admin_dashboard'))

# --- HR Dashboard ---
@app.route('/hr')
@login_required
def hr_dashboard():
    if current_user.role not in ['hr', 'admin']:
        return redirect(url_for('index'))
    students = Student.query.filter_by(added_by_id=current_user.id).all()
    return render_template('hr_dashboard.html', students=students)

@app.route('/hr/add_student', methods=['POST'])
@login_required
def add_student():
    if current_user.role not in ['hr', 'admin']:
        return redirect(url_for('index'))
    name = request.form.get('name')
    email = request.form.get('email')
    skills = request.form.get('skills')
    
    if Student.query.filter_by(email=email).first():
        flash('Student already exists')
    else:
        new_student = Student(
            name=name,
            email=email,
            skills=skills,
            added_by_id=current_user.id
        )
        db.session.add(new_student)
        db.session.commit()
    return redirect(url_for('hr_dashboard'))

# --- Student Dashboard ---
@app.route('/jobs')
@login_required
def student_dashboard():
    search = request.args.get('search', '')
    if search:
        jobs = Job.query.filter(Job.skills.contains(search)).all()
    else:
        jobs = Job.query.order_by(Job.date_posted.desc()).limit(50).all()
    return render_template('student_dashboard.html', jobs=jobs)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
