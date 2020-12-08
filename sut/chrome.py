import asyncio
from typing import List, Union

import pyppeteer
from pyppeteer.launcher import Launcher

DEFAULT_ARGS = [
    "--no-sandbox",
    "--disable-gpu",
    "--no-sandbox",
    "--proxy-server=socks5://127.0.0.1:7890",
]
loop_typing = Union[
    asyncio.unix_events.SelectorEventLoop,
    # asyncio.windows_events.ProactorEventLoop,
    None,
]


class Browser:
    def __init__(self, args: List[str] = DEFAULT_ARGS) -> None:
        self.args = args

    def _init_browser(self, loop: loop_typing = None) -> Launcher:
        loop = loop or asyncio.get_event_loop()
        self.browser = loop.run_until_complete(
            pyppeteer.launch(
                headless=True,
                args=self.args,
                dumpio=True,
                executablePath="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            )
        )

        return self.browser

    def _close_browser(self, loop: loop_typing = None) -> None:
        loop = loop or asyncio.get_event_loop()
        loop.run_until_complete(self.browser.close())


class Page:
    def __init__(self, browser: Launcher) -> None:
        self.browser = browser

    def __close_dialog(self, dialog, loop: loop_typing = None) -> None:
        loop = loop or asyncio.get_event_loop()
        loop.run_until_complete(dialog.dismiss())

    def _init_page(self, loop: loop_typing = None) -> None:
        loop = loop or asyncio.get_event_loop()
        self.page = loop.run_until_complete(self.browser.newPage())
        loop.run_until_complete(self.page.setViewport({"width": 1280, "height": 800}))
        loop.run_until_complete(
            self.page.setUserAgent(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0"
            )
        )

    def click(self, css_selector: str, loop: loop_typing = None):
        loop = loop or asyncio.get_event_loop()
        loop.run_until_complete(self.page.click(css_selector))

    def keyboard(self, key: str, loop: loop_typing = None):
        loop = loop or asyncio.get_event_loop()
        loop.run_until_complete(self.page.keyboard.press(key))

    def input(self, css_selector: str, s: str, loop: loop_typing = None):
        loop = loop or asyncio.get_event_loop()
        loop.run_until_complete(self.page.type(css_selector, s))

    def content(self, loop: loop_typing = None) -> str:
        loop = loop or asyncio.get_event_loop()
        content = loop.run_until_complete(
            self.page.evaluate("""document.body.innerText""", force_expr=True)
        )
        return content

    def wait(self, loop: loop_typing = None):
        loop = loop or asyncio.get_event_loop()
        loop.run_until_complete(
            self.page.waitForNavigation(
                {"waitUntil": ["networkidle2"], "timeout": 60 * 1000}
            )
        )

    def wait_for(self, css_selector: str, loop: loop_typing = None):
        loop = loop or asyncio.get_event_loop()
        loop.run_until_complete(self.page.waitFor(css_selector))

    def fetch(self, url: str, loop: loop_typing = None):
        loop = loop or asyncio.get_event_loop()

        loop.run_until_complete(
            self.page.goto(
                url=url,
                options={"waitUntil": ["networkidle2"], "timeout": 60 * 1000},
            )
        )

    def html(self, loop: loop_typing = None) -> str:
        loop = loop or asyncio.get_event_loop()
        s = loop.run_until_complete(
            self.page.evaluate(
                """document.documentElement.outerHTML""", force_expr=True
            )
        )
        return s

    def scroll(self, loop: loop_typing = None):
        loop = loop or asyncio.get_event_loop()

        loop.run_until_complete(
            self.page.evaluate(
                "{window.scrollBy(0, document.body.scrollHeight);}", force_expr=True
            )
        )

    def reload(self, loop: loop_typing = None):
        loop = loop or asyncio.get_event_loop()
        loop.run_until_complete(
            self.page.reload(
                options={"waitUntil": ["networkidle2"], "timeout": 60 * 1000}
            )
        )
