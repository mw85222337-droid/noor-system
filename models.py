from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, ForeignKey, Enum
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    national_id = Column(String(14), unique=True, index=True)
    face_img = Column(Text)
    current_level = Column(Integer, default=1)
    total_points = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

class Episode(Base):
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True, index=True)
    audio_url = Column(Text)
    text_transcript = Column(Text)
    difficulty_level_ai = Column(String(50))
    level_number = Column(Integer)

class Exam(Base):
    __tablename__ = 'exams'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50)) # quiz_1, medium_5, comprehensive_10, final
    questions_json_ai = Column(Text)

class PointsLog(Base):
    __tablename__ = 'points_log'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    episode_id = Column(Integer, ForeignKey('episodes.id'), nullable=True)
    points = Column(Integer)
    reason = Column(String(255))
    timestamp = Column(TIMESTAMP, default=datetime.utcnow)

class Donor(Base):
    __tablename__ = 'donors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    balance = Column(DECIMAL(10, 2), default=0.0)
    preferences = Column(Text)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey('users.id'))
    donor_id = Column(Integer, ForeignKey('donors.id'))
    points = Column(Integer)
    cash_value = Column(DECIMAL(10, 2))
    transaction_date = Column(TIMESTAMP, default=datetime.utcnow)