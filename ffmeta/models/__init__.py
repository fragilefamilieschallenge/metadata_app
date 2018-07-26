from sqlalchemy import Column, Integer, Text, String, ForeignKey
from sqlalchemy.orm import relationship

from ffmeta.models.db import Base


class Variable(Base):
    __tablename__ = "variable2"

    # Define table fields
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    label = Column(Text)
    old_name = Column(Text)
    data_type = Column(Text)
    warning = Column(Integer)
    group_id = Column(Text)
    group_subid = Column(Text)
    data_source = Column(Text)
    respondent = Column(Text)
    wave = Column(Text)
    scope = Column(Text)
    section = Column(Text)
    leaf = Column(Text)
    measures = Column(Text)
    probe = Column(Text)
    qText = Column(Text)
    survey = Column(Text)

    fp_fchild = Column(Integer)
    fp_mother = Column(Integer)
    fp_father = Column(Integer)
    fp_PCG = Column(Integer)
    fp_partner = Column(Integer)
    fp_other = Column(Integer)

    focal_person = Column(Text)

    responses = relationship('Response', backref='variable')

    topic1 = Column(String)
    subtopic1 = Column(String)
    topic2 = Column(String)
    subtopic2 = Column(String)
    topics = Column(String)  # Concatenation of topic1/topic2, calculated field stored for convenience
    subtopics = Column(String)  # Concatenation of subtopic1/subtopic2, calculated field stored for convenience

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
    name = Column(Text, ForeignKey("variable2.name"))
    label = Column(Text)
    value = Column(Integer)

    def __init__(self, name, label, value):
        self.name = name
        self.label = label
        self.value = value

    def __repr__(self):
        return "<Response %r>" % self.label