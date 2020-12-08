import re
from typing import Dict

from sut.base import PluginFather
from sut.chrome import Page


class Netfilx(PluginFather):
    start_url = "https://www.netflix.com/login"

    def request(self, page: Page, login: Dict) -> str:
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
