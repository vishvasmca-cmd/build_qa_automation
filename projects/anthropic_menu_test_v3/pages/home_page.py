from playwright.async_api import Page, expect

class HomePage:
    """
    The home page of Anthropic, introducing the company and its AI research and products, particularly Claude Opus 4.5.
    URL Pattern: https://www.anthropic.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def try_claude_button(self):
        """Button to try Claude."""
        return self.page.role=button[name="Try Claude"].or_(self.page.text=Try Claude)

    @property
    def research_link(self):
        """Link to the research page."""
        return self.page.text=Research.or_(self.page.a[href='/research'])

    @property
    def economic_futures_link(self):
        """Link to the Economic Futures page."""
        return self.page.text=Economic Futures.or_(self.page.a[href='/economic-futures'])

    @property
    def commitments_dropdown(self):
        """Dropdown menu for Commitments."""
        return self.page.text=Commitments.or_(self.page.button[aria-haspopup='true'][aria-expanded='false']:has-text('Commitments'))

    @property
    def learn_dropdown(self):
        """Dropdown menu for Learn."""
        return self.page.text=Learn.or_(self.page.button[aria-haspopup='true'][aria-expanded='false']:has-text('Learn'))

    @property
    def news_link(self):
        """Link to the News page."""
        return self.page.text=News.or_(self.page.a[href='/news'])

    @property
    def introducing_claude_opus_4_5_link(self):
        """Link to learn more about Claude Opus 4.5."""
        return self.page.text=Introducing Claude Opus 4.5.or_(self.page.a:has-text('Introducing Claude Opus 4.5'))

    @property
    def advanced_tool_use_on_the_claude_link(self):
        """Link to learn more about Advanced tool use on the Claude."""
        return self.page.text=Advanced tool use on the Claude.or_(self.page.a:has-text('Advanced tool use on the Claude'))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Anthropic'
        await Header text contains 'AI research and products that put safety at the frontier'
        await The 'Try Claude' button is visible