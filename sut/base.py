import abc

from sut.chrome import Browser, Page


class PluginFather:
    @abc.abstractmethod
    def request(self, page: Page) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def check(self, page_source: str) -> bool:
        raise NotImplemented

    @abc.abstractmethod
    def start(self) -> bool:
        raise NotImplemented
