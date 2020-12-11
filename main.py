from sut import plugins
from sut.chrome import Browser, Page
import importlib
import json


def loading_config():
    import os

    path = os.path.abspath(".config.json")
    with open(path, "r") as f:
        return json.load(f)


def test():
    config = loading_config()
    executable_path = config.get("chrome").get("executable_path")
    browser = Browser(executable_path)._init_browser()
    page = Page(browser=browser)
    for item in plugins.__all__:
        page._init_page()
        plugin = importlib.import_module("sut.plugins.{}".format(item)).Plugin()
        login = config.get("login").get(plugin.platform)
        result = plugin.start(page=page, login=login)
        page._close_page()
        print(plugin.platform, result)


if __name__ == "__main__":
    test()