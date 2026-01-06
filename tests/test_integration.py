import pytest
from app import db
from app.models import Student, Subject, Grade

@pytest.fixture
def seeded_app(app):
    """Fixture to provide an app with pre-populated data"""
    with app.app_context():
        # Create Subjects
        maths = Subject(name="Mathématiques", coefficient=2.0) # Coef 2
        english = Subject(name="Anglais", coefficient=1.0)     # Coef 1
        sport = Subject(name="Sport", coefficient=1.0)         # Coef 1
        db.session.add_all([maths, english, sport])
        
        # Create Students
        alice = Student(first_name="Alice", last_name="Merveille", email="alice@test.com")
        bob = Student(first_name="Bob", last_name="Eponge", email="bob@test.com")
        charlie = Student(first_name="Charlie", last_name="Outils", email="charlie@test.com") # No grades
        db.session.add_all([alice, bob, charlie])
        
        db.session.commit()
        
        # Add Grades for Alice
        # Moyenne Alice: (15*2 + 10*1) / (2+1) = 40 / 3 = 13.333...
        g1 = Grade(value=15.0, student_id=alice.id, subject_id=maths.id)
        g2 = Grade(value=10.0, student_id=alice.id, subject_id=english.id)
        
        # Add Grades for Bob
        # Moyenne Bob: (8*2 + 12*1) / 3 = 28 / 3 = 9.333...
        g3 = Grade(value=8.0, student_id=bob.id, subject_id=maths.id)
        g4 = Grade(value=12.0, student_id=bob.id, subject_id=english.id)
        
        db.session.add_all([g1, g2, g3, g4])
        db.session.commit()
        
    return app

def test_global_average_calculation(client, seeded_app):
    """Integration Test: Verify calculated averages on the dashboard"""
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    
    # Alice: 13.33
    assert "Alice Merveille" in html
    assert "13.33/20" in html
    
    # Bob: 9.33
    assert "Bob Eponge" in html
    assert "9.33/20" in html
    
    # Charlie: N/A
    assert "Charlie Outils" in html
    assert "N/A" in html

def test_add_grade_updates_average(client, seeded_app):
    """Integration Test: Adding a grade should strictly update the student's average"""
    # Get Charlie's ID
    with seeded_app.app_context():
        charlie = Student.query.filter_by(email="charlie@test.com").first()
        charlie_id = charlie.id
        sport = Subject.query.filter_by(name="Sport").first()
        sport_id = sport.id

    # Add 20/20 in Sport (Coef 1) -> Average should become 20
    response = client.post('/grades/add', data={
        'student_id': charlie_id,
        'subject_id': sport_id,
        'value': '20'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"20.00" in response.data

    # Add another grade: 10/20 in Sport -> (20+10)/2 = 15
    response = client.post('/grades/add', data={
        'student_id': charlie_id,
        'subject_id': sport_id,
        'value': '10'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"15.00" in response.data

def test_user_journey_create_student_to_grade(client, app):
    """Integration Test: Full flow from creating student to ensuring they appear on dashboard"""
    # 1. Dashboard empty-ish (from fixture)
    
    # 2. Add Student
    client.post('/students/add', data={
        'first_name': 'New', 'last_name': 'Kid', 'email': 'new@kid.com'
    })
    
    # 3. Add Subject
    client.post('/subjects/add', data={
        'name': 'Science', 'coefficient': '2'
    })
    
    # Refresh context to get IDs
    with app.app_context():
        s = Student.query.filter_by(email="new@kid.com").first()
        sub = Subject.query.filter_by(name="Science").first()
        s_id = s.id
        sub_id = sub.id

    # 4. Add Grade
    client.post('/grades/add', data={
        'student_id': s_id, 'subject_id': sub_id, 'value': '18'
    })
    
    # 5. Check Dashboard
    response = client.get('/')
    assert b"New Kid" in response.data
    assert b"18.00" in response.data

