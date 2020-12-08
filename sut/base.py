import abc
from typing import Dict, Union

from sut.chrome import Browser, Page

login_typing = Union[Dict, None]


class PluginFather:
    @abc.abstractmethod
    def request(self, page: Page, login: login_typing) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def check(self, page_source: str) -> bool:
        raise NotImplemented

    def start(self, page: Page, login: login_typing) -> bool:
        page_source = self.request(page, login)
        r = self.check(page_source=page_source)
        return r
