from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Property(Base):
    __tablename__ = 'property'

    id = Column(Integer, primary_key=True)
    streetAddress = Column(String(250), nullable=False)
    unitNumber = Column(String(250))
    city = Column(String(250), nullable=False)
    zipCode = Column(Integer, nullable=False)
    state = Column(String(2), nullable=False)
    title = Column(String(250))


class Tenant(Base):
    __tablename__ = 'tenant'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    phone = Column(Integer())
    email = Column(String(250), nullable=False)
    property_id = Column(Integer, ForeignKey('property.id'))
    property = relationship(Property)


engine = create_engine("sqlite:///rentalmanagement.db")

Base.metadata.create_all(engine)
