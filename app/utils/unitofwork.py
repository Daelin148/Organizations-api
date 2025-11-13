from core.db import AsyncSessionLocal
from crud import ScopeRepository, OrganizationRepository, BuildingRepository, PhoneRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = AsyncSessionLocal

    async def __aenter__(self):
        self.session = self.session_factory()
        self.organizations = OrganizationRepository(self.session)
        self.scopes = ScopeRepository(self.session)
        self.phones = PhoneRepository(self.session)
        self.buildings = BuildingRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def refresh(self, *args, **kwargs):
        await self.session.refresh(*args, **kwargs)