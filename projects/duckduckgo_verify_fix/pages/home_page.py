from playwright.async_api import Page, expect

class HomePage:
    """
    This is the search result page for the query 'Universal Gravity' on DuckDuckGo. It displays a list of search results, related searches, and a brief explanation of the topic.
    URL Pattern: https://duckduckgo.com/?origin=funnel_home_website&t=h_&q=Universal+Gravity&ia=web
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_input(self):
        """The input field where the search query is entered."""
        return self.page.//input[@id='search_form_input'].or_(self.page.css=#search_form_input)

    @property
    def search_button(self):
        """The button to submit the search query."""
        return self.page.//button[@id='search_button_homepage'].or_(self.page.css=#search_button_homepage)

    @property
    def all_tab(self):
        """Link to filter search results to show all types of results."""
        return self.page.//a[text()='All'].or_(self.page.css=a[data-zci-link='all'])

    @property
    def images_tab(self):
        """Link to filter search results to show only images."""
        return self.page.//a[text()='Images'].or_(self.page.css=a[data-zci-link='images'])

    @property
    def videos_tab(self):
        """Link to filter search results to show only videos."""
        return self.page.//a[text()='Videos'].or_(self.page.css=a[data-zci-link='videos'])

    @property
    def news_tab(self):
        """Link to filter search results to show only news articles."""
        return self.page.//a[text()='News'].or_(self.page.css=a[data-zci-link='news'])

    @property
    def more_tab(self):
        """Link to show more search result filters."""
        return self.page.//a[text()='More'].or_(self.page.css=a[data-zci-link='more'])

    @property
    def first_result_title(self):
        """The title of the first search result."""
        return self.page.//a[contains(@href, 'wikipedia.org')].or_(self.page.css=.results_links_deep.links_main.links_deep.result__a)

    @property
    def more_button(self):
        """Button to load more search results."""
        return self.page.//a[text()='More'].or_(self.page.css=.module__toggle)

    @property
    def download_browser_button(self):
        """Button to download the DuckDuckGo browser."""
        return self.page.//a[text()='Download Browser'].or_(self.page.css=.js-badge-link)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Universal Gravity at DuckDuckGo'
        await Search results are displayed
        await Related searches are displayed
        await The 'All' tab is selected by default