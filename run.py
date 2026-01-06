import os
from app import create_app, db
from app.models import Student, Subject, Grade

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Student': Student, 'Subject': Subject, 'Grade': Grade}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # In Docker, we want 0.0.0.0, locally 127.0.0.1 is fine but 0.0.0.0 works for both usually.
    # The Dockerfile sets FLASK_RUN_HOST to 0.0.0.0 but app.run needs it explicitly passed if not using 'flask run'
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    app.run(debug=True, host=host, port=port)
