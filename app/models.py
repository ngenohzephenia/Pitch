from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#create pitch categories   
class PitchCategory(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    
    
    def save_category(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_categories(cls):
        categories = PitchCategory.query.all()
        return categories

class Pitch(db.Model):

    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    pitch = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship("Comments", backref="pitches", lazy = "dynamic")
    vote = db.relationship("Votes", backref="pitches", lazy = "dynamic")



    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_pitches(cls):
        Pitch.all_pitches.clear()
       
    def get_pitches(id):
        pitches = Pitch.query.filter_by(category_id=id).all()
        return pitches  
    
class Votes(db.Model):
    __tablename__='votes'

    id = db.Column(db. Integer, primary_key=True)
    vote = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))

    def save_vote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_votes(cls,user_id,pitches_id):
        votes = Votes.query.filter_by(user_id=user_id, pitches_id=id).all()
        return votes
    
class Comments(db.Model):
    __tablename__ = 'comments'

#adding columns

    id = db.Column(db. Integer, primary_key=True)
    comment = db.Column(db.String(255))
    time_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer, db.ForeignKey("pitches.id"))


    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comments.query.order_by(
        Comments.time_posted.desc()).filter_by(pitches_id=id).all()
        return comment        
class User(UserMixin,db.Model):
    __tablename__ = 'users'

    
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True, index =True)
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitches = db.relationship("Pitch", backref="user", lazy = "dynamic")
    comment = db.relationship("Comments", backref="user", lazy = "dynamic")
    vote = db.relationship("Votes", backref="user", lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password) 
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'