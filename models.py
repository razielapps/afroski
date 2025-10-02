from app import db
from datetime import datetime


from extensions import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    

    # Relationships
    listings = db.relationship("Listing", backref="owner", lazy=True)
    messages_sent = db.relationship("Message", 
                                    foreign_keys="Message.sender_id", 
                                    backref="sender", lazy=True)
    messages_received = db.relationship("Message", 
                                        foreign_keys="Message.recipient_id", 
                                        backref="recipient", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(200))  # path to uploaded image
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FK
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Listing {self.title}>"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # FKs
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Message from {self.sender_id} to {self.recipient_id}>"




class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1–5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviewer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    artisan_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    reviewer = db.relationship("User", foreign_keys=[reviewer_id])
    artisan = db.relationship("User", foreign_keys=[artisan_id], backref="reviews")



class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)



class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reporter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey("listing.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # if reporting a user
