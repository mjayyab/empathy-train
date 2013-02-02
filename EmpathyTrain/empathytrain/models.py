import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    UnicodeText,
    Date,
    DateTime,
    func,
    ForeignKey
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    relationship,
    scoped_session,
    sessionmaker,
    backref
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Person(Base):
  __tablename__ = 'people'
  id = Column(Integer, primary_key=True)
  email = Column(UnicodeText, unique=True)

  date_created = Column(DateTime, default=func.now())
  date_modified = Column(DateTime, default=func.now(), onupdate=func.utc_timestamp())

  def __init__(self, email):
    self.email = email

  def __repr__(self):
    return '<Person id={id} email={email}>'.format(**self.__dict__)

class Listing(Base):
  __tablename__= 'listings'
  id = Column(Integer, primary_key=True)
  type = Column(UnicodeText, nullable=False)
  when = Column(Date, nullable=False)
  where = Column(UnicodeText, nullable=False)
  what = Column(UnicodeText, nullable=False)
  email_token = Column(UnicodeText)
  edit_token = Column(UnicodeText)

  who_id = Column(Integer, ForeignKey('people.id'), nullable=False)
  who = relationship('Person', backref='listings')

  date_created = Column(DateTime, default=func.now())
  date_modified = Column(DateTime, default=func.now(), onupdate=func.utc_timestamp())

  def __init__(self, type, what, when, where, who):
    assert type in ('SORRY', 'THANKYOU')
    self.type = type
    self.what = what
    self.when = when
    self.where = where
    self.who_id = who.id

  def __repr__(self):
    return '<Listing when={when} where={where} who={who}>, what={what}'.format(**self.__dict__)
