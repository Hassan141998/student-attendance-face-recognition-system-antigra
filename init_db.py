import os
from app import app, db, User
from werkzeug.security import generate_password_hash

# Use DATABASE_URL from environment or fallback to SQLite
database_url = os.environ.get('DATABASE_URL', 'sqlite:///attendance.db')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url

with app.app_context():
    # Create all tables
    db.create_all()
    print(f"✓ Database tables created successfully on: {database_url}")
    
    # Create default admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()
        print("✓ Default admin user created (username: admin, password: admin123)")
    else:
        print("✓ Admin user already exists")
    
    print("\nDatabase initialization complete!")
