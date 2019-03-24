import datetime

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Sequence,
    Integer,
    Unicode,
    DateTime,
    select,
    func,
    )

from sqlalchemy.orm import (
    relationship,
    backref,
    object_session,
    )

from .meta import Base
from .user import upvotes


companies_branches = Table(
    'companies_branches', Base.metadata,
    Column('company_id', Integer,
           ForeignKey('companies.id', onupdate='CASCADE', ondelete='CASCADE')),
    Column('branch_id', Integer,
           ForeignKey('branches.id', onupdate='CASCADE', ondelete='CASCADE'))
)

companies_persons = Table(
    'companies_persons', Base.metadata,
    Column('company_id', Integer,
           ForeignKey('companies.id', onupdate='CASCADE', ondelete='CASCADE')),
    Column('person_id', Integer,
           ForeignKey('persons.id', onupdate='CASCADE', ondelete='CASCADE'))
)


class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, Sequence('companies_id_seq', 1, 1), primary_key=True)
    name = Column(Unicode(100))
    city = Column(Unicode(100))
    voivodeship = Column(Unicode(2))
    phone = Column(Unicode(50))
    email = Column(Unicode(100))
    www = Column(Unicode(100))
    nip = Column(Unicode(20))
    regon = Column(Unicode(20))
    krs = Column(Unicode(20))
    branches = relationship('Branch', secondary=companies_branches,
                            backref='companies')
    people = relationship('Person', secondary=companies_persons,
                          cascade='all, delete-orphan',
                          single_parent=True, lazy='subquery',
                          backref=backref('companies', uselist=False))
    added = Column(DateTime, default=datetime.datetime.now)
    edited = Column(DateTime, default=datetime.datetime.now,
                    onupdate=datetime.datetime.now)

    def __init__(self, name, city, voivodeship,
                 phone, email, www, nip, regon, krs,
                 branches, people):
        self.name = name
        self.city = city
        self.voivodeship = voivodeship
        self.phone = phone
        self.email = email
        self.www = www
        self.nip = nip
        self.regon = regon
        self.krs = krs
        self.branches = branches
        self.people = people

    @property
    def upvote_count(self):
        return object_session(self).\
            scalar(
                select([func.count(upvotes.c.company_id)]).\
                    where(upvotes.c.company_id == self.id)
            )
