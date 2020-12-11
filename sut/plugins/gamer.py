from sut.base import PluginFather, login_typing
from sut.chrome import Page
from bs4 import BeautifulSoup


class Plugin(PluginFather):
    start_url = "https://ani.gamer.com.tw/animeVideo.php?sn=19526"
    platform = "巴哈姆特動畫瘋"

    def request(self, page: Page, login: login_typing = None) -> str:
        page.fetch(self.start_url)
        return page.html()

    def check(self, page_source: str) -> bool:
        soup = BeautifulSoup(page_source, "lxml")
        check_node = soup.find(
            "div", {"class": "vjs-modal-dialog-content"}
        ).text.strip()
        if check_node == "本服務授權範圍僅限台灣地區，如果您為外國用戶或使用變更IP的插件或軟體，將無法正常使用本服務。":
            return False
        else:
            return True