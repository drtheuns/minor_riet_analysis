from datetime import datetime
import json

from sqlalchemy import (Column, Integer, String, DateTime, Text, Date, types,
                        create_engine, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


class StringyJSON(types.TypeDecorator):
    """
    Stores and retrieves JSON as TEXT
    """

    impl = types.TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


SqliteJSON = types.JSON().with_variant(StringyJSON, 'sqlite')


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=True)
    user_count = Column(Integer)
    date_created = Column(DateTime, default=datetime.utcnow)

    users = relationship('Person', back_populates='session', lazy='dynamic')
    video_sessions = relationship('VideoSession', back_populates='session')

    def __repr__(self):
        return f'<Session(id={self.id})>' # flake8: noqa

    def __str__(self):
        return f'{self.id}: people{self.user_count}, date({self.date_created})' # flake8: noqa


class Person(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birthdate = Column(Date, nullable=True)
    date_created = Column(DateTime, default=datetime.utcnow)
    session_id = Column(Integer, ForeignKey('sessions.id'))

    session = relationship('Session', back_populates='users')
    video_sessions = relationship('VideoSession', back_populates='person')

    def __repr__(self):
        return f'<Person(id={self.id}, name={self.name})>' # flake8: noqa


class Video(Base):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    length = Column(Integer) # video length in seconds
    date_created = Column(DateTime, default=datetime.utcnow)

    video_sessions = relationship('VideoSession', back_populates='video')

    def __repr__(self):
        return f'<Video(id={self.id})>' # flake8: noqa


class VideoSession(Base):
    __tablename__ = 'videosession'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    person_id = Column(Integer, ForeignKey('users.id'))
    video_id = Column(Integer, ForeignKey('video.id'))
    result = Column(SqliteJSON)

    session = relationship('Session', back_populates='video_sessions')
    person = relationship('Person', back_populates='video_sessions')
    video = relationship('Video', back_populates='video_sessions')

    def __repr__(self):
        return f'<VideoSession(id={self.id})>' # flake8: noqa


def load_session():
    engine = create_engine("sqlite:///main.db")
    Session = sessionmaker(bind=engine)
    return Session()
