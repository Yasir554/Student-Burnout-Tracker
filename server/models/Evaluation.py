from db.Burnout_Tracker import db
from datetime import datetime

class Evaluation(db.Model):
    __tablename__ = 'evaluations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    q1 = db.Column(db.Integer, nullable=False)
    q2 = db.Column(db.Integer, nullable=False)
    q3 = db.Column(db.Integer, nullable=False)
    q4 = db.Column(db.Integer, nullable=False)
    q5 = db.Column(db.Integer, nullable=False)
    q6 = db.Column(db.Integer, nullable=False)
    q7 = db.Column(db.Integer, nullable=False)
    q8 = db.Column(db.Integer, nullable=False)
    q9 = db.Column(db.Integer, nullable=False)
    q10 = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    needs_support = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='evaluations')
    
    def calculate_total_score(self):
        self.total_score = sum([
            self.q1, self.q2, self.q3, self.q4, self.q5,
            self.q6, self.q7, self.q8, self.q9, self.q10
        ])
        self.needs_support = self.total_score >= 35

    def to_dict(self):
        return {
            "id": self.id,
            "submitted_at": self.submitted_at.isoformat(),
            "date": self.submitted_at.strftime("%Y-%m-%d"),
            "total_score": self.total_score,
            "needs_support": self.needs_support,
            "user": {
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email
            },
            "answers": {
                "q1": self.q1,
                "q2": self.q2,
                "q3": self.q3,
                "q4": self.q4,
                "q5": self.q5,
                "q6": self.q6,
                "q7": self.q7,
                "q8": self.q8,
                "q9": self.q9,
                "q10": self.q10
            }
        }
