from sut.base import PluginFather, login_typing
from sut.chrome import Page
from bs4 import BeautifulSoup


class Plugin(PluginFather):
    start_url = "https://abema.tv/video/episode/174-18_s1_p1"
    platform = "AbemaTV"

    def request(self, page: Page, login: login_typing = None) -> str:
        page.fetch(self.start_url)
        try:
            # GDPRContainer
            page.wait_for("#main > div")
            page.click(
                "#main > div > div > div.c-application-GDPRContainer__foot > div.c-application-GDPRContainer__check_area > label > label > svg"
            )
            page.click(
                "#main > div > div > div.c-application-GDPRContainer__foot > div.c-application-GDPRContainer__button_area > button"
            )
            page.reload()
        except:
            pass

        return page.html()

    def check(self, page_source: str) -> bool:
        soup = BeautifulSoup(page_source, "lxml")
        check_node = soup.find(
            "div", {"class": "c-vod-EpisodePlayerContainer-reject-by-region"}
        )
        if isinstance(check_node, type(None)):
            return True
        else:
            return False