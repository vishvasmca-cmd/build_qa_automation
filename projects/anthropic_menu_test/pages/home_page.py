from playwright.async_api import Page, expect

class HomePage:
    """
    The Anthropic homepage showcases the company's AI research and products, emphasizing safety and its commitment to public benefit. It highlights Claude Opus 4.5 and provides links to learn more.
    URL Pattern: https://www.anthropic.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def anthropic_logo(self):
        """Anthropic logo in the top left corner."""
        return self.page.role=link[name='Anthropic'].or_(self.page.css=a[aria-label='Anthropic'])

    @property
    def research_link(self):
        """Link to the Research page."""
        return self.page.role=link[name='Research'].or_(self.page.text=Research)

    @property
    def economic_futures_link(self):
        """Link to the Economic Futures page."""
        return self.page.role=link[name='Economic Futures'].or_(self.page.text=Economic Futures)

    @property
    def commitments_dropdown(self):
        """Dropdown button for Commitments."""
        return self.page.role=button[name='Commitments'].or_(self.page.text=Commitments)

    @property
    def learn_dropdown(self):
        """Dropdown button for Learn."""
        return self.page.role=button[name='Learn'].or_(self.page.text=Learn)

    @property
    def news_link(self):
        """Link to the News page."""
        return self.page.role=link[name='News'].or_(self.page.text=News)

    @property
    def try_claude_button(self):
        """Button to try Claude."""
        return self.page.role=button[name='Try Claude'].or_(self.page.text='Try Claude')

    @property
    def introducing_claude_opus_4_5_link(self):
        """Link to learn more about Claude Opus 4.5."""
        return self.page.role=link[name='Introducing Claude Opus 4.5'].or_(self.page.text='Introducing Claude Opus 4.5')

    @property
    def advanced_tool_use_on_the_claude_link(self):
        """Link to learn more about Advanced tool use on the Claude."""
        return self.page.role=link[name='Advanced tool use on the Claude'].or_(self.page.text='Advanced tool use on the Claude')

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'Anthropic'
        await Header text contains 'AI research and products that put safety at the frontier'
        await Element with text 'Try Claude' is visible