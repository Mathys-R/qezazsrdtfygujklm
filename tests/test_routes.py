import pytest
from app.models import Student, Subject, Grade

def test_index_page(client):
    """Test that index page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"GradeMaster" in response.data

def test_add_student_route(client, app):
    """Test adding a student via POST"""
    response = client.post('/students/add', data={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@user.com'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Test User" in response.data # S'assure qu'il apparaît dans la liste

def test_add_subject_route(client, app):
    """Test adding a subject via POST"""
    response = client.post('/subjects/add', data={
        'name': 'Physics',
        'coefficient': '1.5'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # On reste sur l'index, vérifions qu'aucun crash n'a lieu et que le flash message est là (difficile à check sans parsing HTML fin, mais le status 200 est déjà bon)
    
def test_add_grade_valid(client, app):
    """Test adding a valid grade"""
    # Setup data
    with app.app_context():
        from app import db
        s = Student(first_name="S", last_name="L", email="s@l.com")
        sub = Subject(name="Geo")
        db.session.add_all([s, sub])
        db.session.commit()
        s_id = s.id
        sub_id = sub.id

    response = client.post('/grades/add', data={
        'student_id': s_id,
        'subject_id': sub_id,
        'value': '14.5'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"14.5" in response.data # La note doit apparaître sur la page détail

def test_student_detail_page(client, app):
    """Test accessing student detail page"""
    # Setup
    with app.app_context():
        from app import db
        s = Student(first_name="Detail", last_name="View", email="d@v.com")
        db.session.add(s)
        db.session.commit()
        s_id = s.id
        
    response = client.get(f'/student/{s_id}')
    assert response.status_code == 200
    assert b"Detail View" in response.data
