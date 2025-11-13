from core.db import Base
from sqlalchemy import Column, ForeignKey, Integer, Table

organization_scope = Table(
    'organization_scope',
    Base.metadata,
    Column(
        'organization_id',
        Integer,
        ForeignKey('organizations.id'),
        primary_key=True,
        index=True
    ),
    Column(
        'scope_id',
        Integer,
        ForeignKey('scopes.id'),
        primary_key=True,
        index=True
    )
)
