from playwright.async_api import Page, expect

class WikipediaMainPagePage:
    """
    This is the main page of Wikipedia, providing access to a vast collection of articles in multiple languages.
    URL Pattern: https://en.wikipedia.org/wiki/Anti-gravity
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_wikipedia_input(self):
        """Input field to enter search queries."""
        return self.page.role=searchbox.or_(self.page.css=input[name='search'])

    @property
    def search_button(self):
        """Button to initiate the search."""
        return self.page.role=button[name='Search'].or_(self.page.css=input[value='Search'])

    @property
    def language_dropdown(self):
        """Dropdown to select the language for searching Wikipedia."""
        return self.page.role=combobox[name='language'].or_(self.page.css=select[name='language'])

    @property
    def english_link(self):
        """Link to the English version of Wikipedia with the number of articles."""
        return self.page.role=link[name='English'].or_(self.page.text=English 7,121,000+ articles)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Wikipedia'
        await Header text contains 'Wikipedia The Free Encyclopedia'
        await Search input field is present
        await Search button is present