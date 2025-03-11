import os
from typing import Tuple, Dict, List, Union, Optional
from playwright.sync_api import Browser, Page
from .base_playwright import BasePlaywrightComputer
from browserbase import Browserbase
from dotenv import load_dotenv

load_dotenv()


class BrowserbaseBrowser(BasePlaywrightComputer):
    """
    Browserbase is a headless browser platform that offers a remote browser API. You can use it to control thousands of browsers from anywhere.
    You can find more information about Browserbase at https://docs.browserbase.com/ or view our OpenAI CUA Quickstart at https://docs.browserbase.com/integrations/openai-cua/introduction.
    """

    def __init__(
        self,
        width: int = 1024,
        height: int = 768,
        region: str = "us-west-2",
        proxy: bool = False,
    ):
        """
        Initialize the Browserbase instance. Additional configuration options for features such as persistent cookies, ad blockers, file downloads and more can be found in the Browserbase API documentation: https://docs.browserbase.com/reference/api/create-a-session

        Args:
            width (int): The width of the browser viewport. Default is 1024.
            height (int): The height of the browser viewport. Default is 768.
            region (str): The region for the Browserbase session. Default is "us-west-2". Pick a region close to you for better performance. https://docs.browserbase.com/guides/multi-region
            proxy (bool): Whether to use a proxy for the session. Default is False. Turn on proxies if you're browsing is frequently interrupted. https://docs.browserbase.com/features/proxies
        """
        super().__init__()
        self.bb = Browserbase(api_key=os.getenv("BROWSERBASE_API_KEY"))
        self.project_id = os.getenv("BROWSERBASE_PROJECT_ID")
        self.session = None
        self.dimensions = (width, height)
        self.region = region
        self.proxy = proxy

    def _get_browser_and_page(self) -> Tuple[Browser, Page]:
        """
        Create a Browserbase session and connect to it.

        Returns:
            Tuple[Browser, Page]: A tuple containing the connected browser and page objects.
        """
        # Create a session on Browserbase with specified parameters
        width, height = self.dimensions
        session_params = {
            "project_id": self.project_id,
            "browser_settings": {"viewport": {"width": width, "height": height}},
            "region": self.region,
            "proxies": self.proxy,
        }
        self.session = self.bb.sessions.create(**session_params)

        # Print the live session URL
        print(
            f"Watch and control this browser live at https://www.browserbase.com/sessions/{self.session.id}"
        )

        # Connect to the remote session
        browser = self._playwright.chromium.connect_over_cdp(self.session.connect_url)
        context = browser.contexts[0]
        page = context.pages[0]
        page.goto("https://bing.com")

        return browser, page

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Clean up resources when exiting the context manager.

        Args:
            exc_type: The type of the exception that caused the context to be exited.
            exc_val: The exception instance that caused the context to be exited.
            exc_tb: A traceback object encapsulating the call stack at the point where the exception occurred.
        """
        if self._page:
            self._page.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

        if self.session:
            print(
                f"Session completed. View replay at https://browserbase.com/sessions/{self.session.id}"
            )

    def screenshot(self) -> str:
        """
        Capture a screenshot of the current viewport.

        Returns:
            str: A base64 encoded string of the screenshot.
        """
        return super().screenshot()
