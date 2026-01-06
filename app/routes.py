from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Student, Subject, Grade

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    students = Student.query.all()
    # Calculate average for each student
    student_data = []
    for student in students:
        grades = student.grades.all()
        if grades:
            # Weighted average
            total_points = sum(g.value * g.subject.coefficient for g in grades)
            total_coeff = sum(g.subject.coefficient for g in grades)
            average = total_points / total_coeff if total_coeff > 0 else 0
        else:
            average = None
        student_data.append({
            'student': student,
            'average': average,
            'grade_count': len(grades)
        })
    return render_template('index.html', students=student_data)

@bp.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        
        new_student = Student(first_name=first_name, last_name=last_name, email=email)
        try:
            db.session.add(new_student)
            db.session.commit()
            flash('Élève ajouté avec succès!', 'success')
            return redirect(url_for('main.index'))
        except:
            db.session.rollback()
            flash('Erreur lors de l\'ajout. L\'email existe peut-être déjà.', 'danger')
            
    return render_template('add_student.html')

@bp.route('/subjects/add', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        name = request.form['name']
        coefficient = float(request.form['coefficient'])
        
        new_subject = Subject(name=name, coefficient=coefficient)
        try:
            db.session.add(new_subject)
            db.session.commit()
            flash('Matière ajoutée avec succès!', 'success')
            return redirect(url_for('main.index'))
        except:
            db.session.rollback()
            flash('Erreur lors de l\'ajout de la matière.', 'danger')

    return render_template('add_subject.html')

@bp.route('/grades/add', methods=['GET', 'POST'])
def add_grade():
    students = Student.query.all()
    subjects = Subject.query.all()
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        subject_id = request.form['subject_id']
        value = float(request.form['value'])
        
        if not (0 <= value <= 20):
             flash('La note doit être comprise entre 0 et 20.', 'danger')
        else:
            new_grade = Grade(student_id=student_id, subject_id=subject_id, value=value)
            db.session.add(new_grade)
            db.session.commit()
            flash('Note ajoutée avec succès!', 'success')
            return redirect(url_for('main.student_detail', id=student_id))
            
    return render_template('add_grade.html', students=students, subjects=subjects)

@bp.route('/student/<int:id>')
def student_detail(id):
    student = db.get_or_404(Student, id)
    grades = student.grades.all()
    
    # Organize grades by subject might be useful for display, but simple list is okay for now
    # Let's compute average
    if grades:
        total_points = sum(g.value * g.subject.coefficient for g in grades)
        total_coeff = sum(g.subject.coefficient for g in grades)
        average = total_points / total_coeff if total_coeff > 0 else 0
    else:
        average = None
        
    return render_template('student_detail.html', student=student, grades=grades, average=average)
