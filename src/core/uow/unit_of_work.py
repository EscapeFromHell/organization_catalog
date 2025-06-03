import functools
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from types import TracebackType
from typing import Any, Never

from src.core.db import async_session
from src.core.repository import ActivitiesRepository, BuildingsRepository, OrganizationsRepository

AsyncFunc = Callable[..., Awaitable[Any]]


class AbstractUnitOfWork(ABC):
    activities: ActivitiesRepository
    buildings: BuildingsRepository
    organizations: OrganizationsRepository

    @abstractmethod
    def __init__(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> Never:
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    """The class responsible for the atomicity of transactions."""

    def __init__(self) -> None:
        self.session_factory = async_session

    async def __aenter__(self) -> None:
        self.session = self.session_factory()
        self.activities = ActivitiesRepository(self.session)
        self.buildings = BuildingsRepository(self.session)
        self.organizations = OrganizationsRepository(self.session)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


def transaction_mode(func: AsyncFunc) -> AsyncFunc:
    """Decorate a function with transaction mode."""

    @functools.wraps(func)
    async def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        async with self.uow:
            return await func(self, *args, **kwargs)

    return wrapper
