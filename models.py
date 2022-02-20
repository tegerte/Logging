# models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, nullable=False, default=datetime.datetime.now)
    level_id = Column(Integer, ForeignKey('levels.id'))
    module = Column(String(200), nullable=True)
    thread_name = Column(String(200), nullable=True)
    file_name = Column(String(200), nullable=True)
    func_name = Column(String(200), nullable=True)
    line_no = Column(Integer, nullable=True)
    process_name = Column(String(200), nullable=True)
    message = Column(Text)
    last_line = Column(Text)

    level = relationship('Levels')


class Levels(Base):
    __tablename__ = "levels"
    id = Column(Integer, primary_key=True)
    level_name = Column(String(20), unique=True, nullable=False)
