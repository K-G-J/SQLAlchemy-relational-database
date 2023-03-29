# Animals
# ID | Name | Habitat

# Zookepper Log
# ID | Animal ID (Foreign Key) | Notes
from sqlalchemy import (create_engine, Column, Integer,
                        String, ForeignKey)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///zoo.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Animal(Base):
    __tablename__ = 'animals'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    habitat = Column(String)
    # LogBook that has all notes with foreign key related to id
    # Classname + back_populates column on relationship class
    logs = relationship('Logbook', back_populates='animal')

    def __repr__(self):
        return f"""
    \nAnimal {self.id}\r
    Name = {self.name}\r
    Habitat = {self.habitat}
    """


class Logbook(Base):
    __tablename__ = 'logbook'

    id = Column(Integer, primary_key=True)
    # column of Ids from the 'animals' table
    # ForeignKey = tablename + column
    animal_id = Column(Integer, ForeignKey('animals.id'))
    notes = Column(String)
    # Animal that relates to foreign key on animal_id
    # Classname + back_populates column on relationship class
    # Cascade
    # - all, delete - delete children when parent is deleted
    # (i.e logs will be deleted when Animal is deleted)
    # - delete-orphan - if deleted on parent table, will be deleted from child table
    # (i.e if logs[0] is deleted from Animal, will be deleted in Logbook table)
    animal = relationship('Animal', back_populates='logs',
                          cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f"""
    \nLogbook {self.id}\r
    Animal ID = {self.animal_id}\r
    Notes = {self.notes}
    """


if __name__ == '__main__':
    Base.metadata.create_all(engine)
