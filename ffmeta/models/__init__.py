from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship

from ffmeta.models.db import Base


class Variable(Base):
    __tablename__ = "variable3"

    # Define table fields
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    label = Column(Text)
    old_name = Column(Text)
    data_type = Column(Text)
    warning = Column(Integer)
    group_id = Column(Text)
    data_source = Column(Text)
    respondent = Column(Text)
    wave = Column(Text)
    n_cities_asked = Column(Text)
    section = Column(Text)
    leaf = Column(Text)
    scale = Column(Text)
    probe = Column(Text)
    qtext = Column(Text)
    survey = Column(Text)

    fp_fchild = Column(Integer)
    fp_mother = Column(Integer)
    fp_father = Column(Integer)
    fp_PCG = Column(Integer)
    fp_partner = Column(Integer)
    fp_other = Column(Integer)

    focal_person = Column(Text)

    responses = relationship('Response', backref='variable')

    topics = Column(String)
    subtopics = Column(String)

    in_FFC_file = Column(String)

    def __init__(self, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    def __repr__(self):
        return "<Variable %r>" % self.name

    def focal_people(self):
        """Return a list of focal person/people for this variable"""
        attr_to_str = {
            'fp_fchild': 'Focal Child',
            'fp_mother': 'Mother',
            'fp_father': 'Father',
            'fp_PCG': 'Primary Caregiver',
            'fp_partner': 'Partner',
            'fp_other': 'Other'
        }

        return [attr_to_str[attr] for attr in attr_to_str if getattr(self, attr) == 1]

    def focal_people_string(self):
        """A string representation of focal person/people, suitable for display in templates"""
        fp = self.focal_people()
        return ', '.join(fp) if fp else 'None'


class Response(Base):
    __tablename__ = "response2"

    id = Column(Integer, primary_key=True)
    name = Column(Text, ForeignKey("variable3.name"))
    label = Column(Text)
    value = Column(Integer)

    def __init__(self, name, label, value):
        self.name = name
        self.label = label
        self.value = value

    def __repr__(self):
        return "<Response %r>" % self.label