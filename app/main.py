from flask import Flask, request, jsonify, send_from_directory, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os
import csv
import io
from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = Flask(__name__, static_folder="../static")
app.config['SECRET_KEY'] = 'super-secret-key-for-development'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

def get_password_hash(password):
    return generate_password_hash(password)

def verify_password(plain_password, hashed_password):
    return check_password_hash(hashed_password, plain_password)

def create_access_token(data, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, app.config['SECRET_KEY'], algorithm=ALGORITHM)
    return encoded_jwt

def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({"message": "Token is missing"}), 401
            
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[ALGORITHM])
            db = next(get_db())
            current_user = db.query(models.User).filter_by(username=data['sub']).first()
            if not current_user:
                return jsonify({"message": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"message": "Token is invalid"}), 401
            
        return f(current_user, db, *args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

@app.route('/token', methods=['POST'])
def login():
    if request.content_type == 'application/x-www-form-urlencoded':
        username = request.form.get('username')
        password = request.form.get('password')
    else:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
    db = next(get_db())
    user = db.query(models.User).filter_by(username=username).first()
    
    if not user or not verify_password(password, user.password_hash):
        return jsonify({"message": "Incorrect username or password"}), 401
        
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role, "assigned_year": user.assigned_year},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return jsonify({
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username,
        "assigned_year": user.assigned_year
    })

@app.route('/students', methods=['GET'])
@token_required
def get_students(current_user, db):
    year = request.args.get('year')
    if current_user.role == 'Rep':
        year = current_user.assigned_year
        
    query = db.query(models.Student)
    if year:
        query = query.filter(models.Student.year == year)
        
    students = query.all()
    return jsonify([{
        "id": s.id,
        "register_no": s.register_no,
        "name": s.name,
        "year": s.year,
        "semester": s.semester,
        "batch": s.batch
    } for s in students])

@app.route('/logs', methods=['POST'])
@token_required
def create_logs(current_user, db):
    data = request.get_json()
    student_logs = data.get('student_logs', [])
    
    logs_to_add = []
    for s_log in student_logs:
        s_id = s_log.get('student_id')
        try:
            time_obj = datetime.strptime(s_log.get('time'), '%H:%M:%S').time()
            date_obj = datetime.strptime(s_log.get('date'), '%Y-%m-%d').date()
        except Exception:
            return jsonify({"message": "Invalid date or time format"}), 400
            
        student = db.query(models.Student).filter_by(id=s_id).first()
        if not student:
            continue
        if current_user.role == 'Rep' and student.year != current_user.assigned_year:
            continue
            
        db_log = models.LateLog(
            student_id=s_id,
            date=date_obj,
            time=time_obj,
            session=data.get('session'),
            logged_by_id=current_user.id
        )
        logs_to_add.append(db_log)
        
    db.add_all(logs_to_add)
    db.commit()
    return jsonify({"message": f"Successfully logged {len(logs_to_add)} students"}), 201

@app.route('/logs', methods=['GET'])
@token_required
def get_logs(current_user, db):
    year = request.args.get('year')
    date_str = request.args.get('date')
    session = request.args.get('session')
    
    query = db.query(models.LateLog).join(models.Student)
    
    if current_user.role == 'Rep':
        query = query.filter(models.Student.year == current_user.assigned_year)
    elif year:
        query = query.filter(models.Student.year == year)
        
    if date_str:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        query = query.filter(models.LateLog.date == date_obj)
        
    if session:
        query = query.filter(models.LateLog.session == session)
        
    logs = query.all()
    return jsonify([{
        "id": l.id,
        "date": l.date.strftime('%Y-%m-%d'),
        "time": l.time.strftime('%H:%M:%S'),
        "session": l.session,
        "student": {
            "register_no": l.student.register_no,
            "name": l.student.name,
            "year": l.student.year
        },
        "logged_by_user": {
            "username": l.logged_by_user.username
        }
    } for l in logs])

@app.route('/export/csv', methods=['GET'])
@token_required
def export_csv(current_user, db):
    if current_user.role not in ['HOD', 'Staff']:
        return jsonify({"message": "Not authorized"}), 403
        
    year = request.args.get('year')
    date_str = request.args.get('date')
    session = request.args.get('session')
    
    query = db.query(models.LateLog).join(models.Student).join(models.User)
    if year:
        query = query.filter(models.Student.year == year)
    if date_str:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        query = query.filter(models.LateLog.date == date_obj)
    if session:
        query = query.filter(models.LateLog.session == session)
        
    logs = query.all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Time', 'Session', 'Register No', 'Name', 'Year', 'Logged By'])
    
    for log in logs:
        writer.writerow([
            log.date, log.time, log.session, 
            log.student.register_no, log.student.name, log.student.year,
            log.logged_by_user.username
        ])
        
    output.seek(0)
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    
    return send_file(
        mem,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f"late_logs.csv"
    )

@app.route('/stats', methods=['GET'])
@token_required
def get_stats(current_user, db):
    thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
    query = db.query(models.LateLog.student_id, func.count(models.LateLog.id).label('late_count')).filter(models.LateLog.date >= thirty_days_ago)
    
    if current_user.role == 'Rep':
        query = query.join(models.Student).filter(models.Student.year == current_user.assigned_year)
        
    stats = query.group_by(models.LateLog.student_id).all()
    return jsonify([{"student_id": stat[0], "late_count": stat[1]} for stat in stats])

@app.route('/logs/<int:log_id>', methods=['DELETE'])
@token_required
def delete_log(current_user, db, log_id):
    if current_user.role != 'HOD':
        return jsonify({"message": "Not authorized to delete logs"}), 403
        
    log = db.query(models.LateLog).filter_by(id=log_id).first()
    if not log:
        return jsonify({"message": "Log not found"}), 404
        
    db.delete(log)
    db.commit()
    return jsonify({"message": "Log deleted successfully"}), 200

@app.route('/')
def serve_spa():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
