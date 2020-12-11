from sut.base import PluginFather, login_typing
from sut.chrome import Page
from bs4 import BeautifulSoup


class Plugin(PluginFather):
    start_url = "https://www.kktv.me/play/01000406010001"
    platform = "KKTV"

    def request(self, page: Page, login: login_typing = None) -> str:
        page.fetch(self.start_url)
        return page.html()

    def check(self, page_source: str) -> bool:
        soup = BeautifulSoup(page_source, "lxml")
        check_node = soup.find("h2", {"class": "forbidden__message warning kktv"})
        if isinstance(check_node, type(None)):
            return True
        else:
            return False
