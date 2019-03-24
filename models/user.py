from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    )

from .meta import Base


upvotes = Table(
    'upvotes', Base.metadata,
    Column('company_id', Integer,
           ForeignKey('companies.id', onupdate='CASCADE', ondelete='CASCADE')),
    Column('user_id', Integer,
           ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))
)
