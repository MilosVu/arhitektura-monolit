"""Service abstrakcija — poslovna logika iznad repozitorijuma."""

from abc import ABC


class BaseService(ABC):
    """
    Bazna klasa za application servise.

    Servisi orkestriraju repozitorijume, Redis, RabbitMQ i eksterne portove.
    Ne sadrže HTTP/Celery detalje — to ostaje u router/task sloju.
    """

    pass
