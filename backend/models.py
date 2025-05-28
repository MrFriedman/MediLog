from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

# Association table for the many-to-many relationship between patients and healthcare providers
patient_provider_association = db.Table('patient_provider_association',
    db.Column('patient_id', db.String(32), db.ForeignKey('patients.id'), primary_key=True),
    db.Column('provider_id', db.String(32), db.ForeignKey('providers.id'), primary_key=True),
)
   
class User(db.Model):
    __tablename__ = "base_users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    accountType = db.Column(db.String(10), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': accountType,
        'polymorphic_identity': 'base_user'
    }

class Patient(User):
    __tablename__ = "patients" 
    id = db.Column(db.String(32), db.ForeignKey('base_users.id'), primary_key=True)
    full_name = db.Column(db.String(345), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy=True)
    
    # Many-to-many relationship with healthcare providers
    providers = db.relationship('Provider', secondary=patient_provider_association, 
                              lazy='subquery', backref=db.backref('patients', lazy=True))

    __mapper_args__ = {
        'polymorphic_identity': 'patient'
    }

class Admin(User):
    __tablename__ = "admins"
    id = db.Column(db.String(32), db.ForeignKey('base_users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    
class Provider(User):  # New model for healthcare providers
    __tablename__ = "providers"
    id = db.Column(db.String(32), db.ForeignKey('base_users.id'), primary_key=True)
    name = db.Column(db.String(345), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    medical_records = db.relationship('MedicalRecord', backref='provider', lazy=True)
    prescriptions = db.relationship('Prescription', backref='prescriber', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'provider'
    }
    
class MedicalRecord(db.Model):  # Replaces "story"
    __tablename__ = "medical_records"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(32), db.ForeignKey('patients.id'), nullable=False)
    provider_id = db.Column(db.String(32), db.ForeignKey('providers.id'), nullable=False)
    consultation_date = db.Column(db.DateTime, default=datetime.now)
    symptoms = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment_plan = db.Column(db.Text, nullable=False)
    consultation_transcript = db.Column(db.Text, nullable=True)
    prescriptions = db.relationship('Prescription', backref='medical_record', lazy=True)
    health_metrics = db.relationship('HealthMetric', backref='medical_record', lazy=True)
    
class Prescription(db.Model):  # New model
    __tablename__ = "prescriptions"
    id = db.Column(db.Integer, primary_key=True)
    medical_record_id = db.Column(db.Integer, db.ForeignKey('medical_records.id'), nullable=False)
    provider_id = db.Column(db.String(32), db.ForeignKey('providers.id'), nullable=False)
    medication_name = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    frequency = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.now)
    notes = db.Column(db.Text, nullable=True)

class HealthMetric(db.Model):  # Replaces "statistic"
    __tablename__ = "health_metrics"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(32), db.ForeignKey('patients.id'), nullable=False)
    medical_record_id = db.Column(db.Integer, db.ForeignKey('medical_records.id'), nullable=False)
    blood_pressure = db.Column(db.String(20), nullable=True)
    heart_rate = db.Column(db.Integer, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    oxygen_saturation = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    recorded_date = db.Column(db.DateTime, default=datetime.now)
    notes = db.Column(db.Text, nullable=True)

class TranscriptionMetadata(db.Model):  # New model to track transcription quality/metrics
    __tablename__ = "transcription_metadata"
    id = db.Column(db.Integer, primary_key=True)
    medical_record_id = db.Column(db.Integer, db.ForeignKey('medical_records.id'), nullable=False)
    transcription_duration = db.Column(db.Float, nullable=False)  # Length of audio in seconds
    confidence_score = db.Column(db.Float, nullable=False)  # Overall confidence in transcription
    noise_level = db.Column(db.Float, nullable=True)  # Estimated background noise
    speaker_count = db.Column(db.Integer, nullable=True)  # Estimated number of speakers
    processing_time = db.Column(db.Float, nullable=False)  # How long processing took
    created_at = db.Column(db.DateTime, default=datetime.now)