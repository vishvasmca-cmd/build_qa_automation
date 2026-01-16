from playwright.async_api import Page, expect

class WikipediaMainPagePage:
    """
    Wikipedia Main Page - serves as the entry point to the online encyclopedia, providing access to various language versions, search functionality, and information about Wikipedia's anniversary.
    URL Pattern: https://en.wikipedia.org/wiki/Anti-gravity
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def search_wikipedia_input(self):
        """Input field to enter search queries."""
        return self.page.[name='search'].or_(self.page.css=input[name='search'])

    @property
    def language_dropdown(self):
        """Dropdown to select the language for searching Wikipedia."""
        return self.page.id=searchLanguage.or_(self.page.css=select#searchLanguage)

    @property
    def search_button(self):
        """Button to initiate the Wikipedia search."""
        return self.page.css=button.searchButton.or_(self.page.text=Search)

    @property
    def english_link(self):
        """Link to the English version of Wikipedia."""
        return self.page.text='English 7,121,000+ articles'.or_(self.page.css=a[title='English'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Wikipedia'
        await Main heading contains 'Wikipedia The Free Encyclopedia'
        await Search input field is present
        await Language dropdown is present
        await Search button is present