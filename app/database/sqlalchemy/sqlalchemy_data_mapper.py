import abc


class SqlAlchemyDataMapper(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def configure_mappings(cls):
        pass
