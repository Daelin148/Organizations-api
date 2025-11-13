from sqlalchemy import Table, ForeignKey, Column, Integer

from core.db import Base


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
