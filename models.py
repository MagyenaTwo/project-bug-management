from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Open')

    def __repr__(self):
        return f'<Bug {self.title}>'
