from sut.base import PluginFather, login_typing
from sut.chrome import Page
from bs4 import BeautifulSoup


class Plugin(PluginFather):
    start_url = "https://www.bilibili.com/bangumi/play/ep331109"
    platform = "Bilibili 港澳臺限定"

    def request(self, page: Page, login: login_typing = None) -> str:
        page.fetch(self.start_url)
        return page.html()

    def check(self, page_source: str) -> bool:
        soup = BeautifulSoup(page_source, "lxml")
        check_node = soup.find("div", {"class": "mask-body"})
        if isinstance(check_node, type(None)):
            return True
        else:
            return False