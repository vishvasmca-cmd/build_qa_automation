from playwright.async_api import Page, expect

class HomePage:
    """
    This is the homepage for Yahoo Finance, providing access to news, stock quotes, and financial data.
    URL Pattern: https://finance.yahoo.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def news(self):
        """Link to the News section."""
        return self.page.text=News.or_(self.page.css=a[href*='/news/'])

    @property
    def today_s_news(self):
        """Link to the Today's News section."""
        return self.page.text=Today's news.or_(self.page.css=a[href*='/news/today'])

    @property
    def us(self):
        """Link to the US news section."""
        return self.page.text=US.or_(self.page.css=a[href*='/us'])

    @property
    def politics(self):
        """Link to the Politics news section."""
        return self.page.text=Politics.or_(self.page.css=a[href*='/politics'])

    @property
    def health(self):
        """Link to the Health section."""
        return self.page.text=Health.or_(self.page.css=a[href*='/health'])

    @property
    def wellness(self):
        """Link to the Wellness section."""
        return self.page.text=Wellness.or_(self.page.css=a[href*='/wellness'])

    @property
    def mental_health(self):
        """Link to the Mental health section."""
        return self.page.text=Mental health.or_(self.page.css=a[href*='/mental-health'])

    @property
    def nutrition(self):
        """Link to the Nutrition section."""
        return self.page.text=Nutrition.or_(self.page.css=a[href*='/nutrition'])

    @property
    def fitness(self):
        """Link to the Fitness section."""
        return self.page.text=Fitness.or_(self.page.css=a[href*='/fitness'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Yahoo Finance'
        await Page contains 'News'
        await Page contains 'Health'