from app.configs.database import db
from dataclasses import dataclass
from sqlalchemy import Column, String, DateTime, Integer
from datetime import date, datetime

@dataclass
class LeadsModel(db.Model):

    name = str
    email = str
    phone = str
    creation_date = date
    last_visit = date
    visits = int

    __tablename__ = "leads"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow())
    last_visit = Column(DateTime, default=datetime.utcnow())
    visits = Column(Integer, nullable=True, default=1)

    
    