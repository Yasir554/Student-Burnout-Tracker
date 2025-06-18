'''

from db.Burnout_Tracker import db

class BurnoutAssessment(db.Model):
    __table__= 'burnout_assessment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date)
    score = db.Column(db.Integer)
    
'''