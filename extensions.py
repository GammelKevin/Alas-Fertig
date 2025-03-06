from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_extensions(app):
    db.init_app(app)
    # Diese Einstellungen werden jetzt in app.py gesetzt