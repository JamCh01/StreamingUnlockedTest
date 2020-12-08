import re

from sut.base import PluginFather, login_typing
from sut.chrome import Page
from bs4 import BeautifulSoup


class Netfilx(PluginFather):
    start_url = "https://www.netflix.com/login"

    def request(self, page: Page, login: login_typing = dict()) -> str:
        page.fetch(url="https://netflix.com/clearcookies")
        page.fetch(self.start_url)
        page.input("#id_userLoginId", login.get("username"))
        page.input("#id_password", login.get("password"))
        page.keyboard(key="Enter")
        page.wait()
        if login.get("ext", {}).get("is_family", False):
            index = login.get("ext").get("role_index")
            page.wait_for(
                "#appMountPoint > div > div > div:nth-child(1) > div.bd.dark-background > div.profiles-gate-container > div > div"
            )
            page.click(
                "#appMountPoint > div > div > div:nth-child(1) > div.bd.dark-background > div.profiles-gate-container > div > div > ul > li:nth-child({index}) > div > a > div > div".format(
                    index=index
                )
            )
            page.wait()
        page.scroll()

        return page.content()

    def check(self, page_source: str) -> bool:
        regex = re.compile(r"今日.*排行榜 Top 10")
        return len(regex.findall(page_source)) > 0


class BilibiliTaiwanOnly(PluginFather):
    start_url = "https://www.bilibili.com/bangumi/play/ep268176"

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


class BilibiliHMT(PluginFather):
    start_url = "https://www.bilibili.com/bangumi/play/ep331109"

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
