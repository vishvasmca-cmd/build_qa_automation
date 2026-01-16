from playwright.async_api import Page, expect

class DuckduckgoSearchResultsPage:
    """
    DuckDuckGo search results page for 'Universal Gravity', focusing on identifying key elements and assertions for automated testing.
    URL Pattern: https://duckduckgo.com/?q=Universal+Gravity
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """The main search input field on the DuckDuckGo homepage."""
        return self.page.id=search_form_input_homepage.or_(self.page.css=input[type='text'])

    @property
    def search_button(self):
        """The button to submit the search query."""
        return self.page.id=search_button_homepage.or_(self.page.css=button[aria-label='Search'])

    @property
    def all_tab(self):
        """The 'All' tab for displaying all search results."""
        return self.page.text=All.or_(self.page.css=.module--about__link.module--about__link--active)

    @property
    def images_tab(self):
        """The 'Images' tab for displaying image search results."""
        return self.page.text=Images.or_(self.page.css=.module--about__link[data-zci-tab='images'])

    @property
    def videos_tab(self):
        """The 'Videos' tab for displaying video search results."""
        return self.page.text=Videos.or_(self.page.css=.module--about__link[data-zci-tab='videos'])

    @property
    def news_tab(self):
        """The 'News' tab for displaying news search results."""
        return self.page.text=News.or_(self.page.css=.module--about__link[data-zci-tab='news'])

    @property
    def wikipedia_result_link(self):
        """Link to the Wikipedia article about Newton's law of universal gravitation."""
        return self.page.text=Newton's law of universal gravitation - Wikipedia.or_(self.page.css=a[href*='wikipedia.org'][class='result__a'])

    @property
    def download_browser_button(self):
        """Button to download the DuckDuckGo browser."""
        return self.page.text=Download Browser.or_(self.page.css=a[class='js-advert-link'])

    @property
    def search_suggestion_universal_gravity_constant(self):
        """Suggested search term: universal gravity constant"""
        return self.page.text=universal gravity constant.or_(self.page.css=a[href*='q=universal+gravity+constant'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await title contains 'Universal Gravity at DuckDuckGo'
        await page contains text 'Newton's law of universal gravitation'
        await page contains link to 'https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation'