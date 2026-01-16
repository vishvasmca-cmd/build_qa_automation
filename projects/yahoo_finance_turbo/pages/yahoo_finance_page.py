from playwright.async_api import Page, expect

class YahooFinancePage:
    """
    This page provides financial information and news related to a specific stock (AAPL in this case).
    URL Pattern: https://finance.yahoo.com/quote/AAPL/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def news_link(self):
        """Link to the news section."""
        return self.page.//a[text()='News'].or_(self.page.css=a[href*='/news/'])

    @property
    def today_s_news_link(self):
        """Link to today's news section."""
        return self.page.//a[text()="Today's news"].or_(self.page.css=a[href*='/news/today'])

    @property
    def us_news_link(self):
        """Link to US news section."""
        return self.page.//a[text()='US'].or_(self.page.css=a[href*='/us'])

    @property
    def politics_news_link(self):
        """Link to Politics news section."""
        return self.page.//a[text()='Politics'].or_(self.page.css=a[href*='/politics'])

    @property
    def world_news_link(self):
        """Link to World news section."""
        return self.page.//a[text()='World'].or_(self.page.css=a[href*='/world'])

    @property
    def weather_news_link(self):
        """Link to Weather news section."""
        return self.page.//a[text()='Weather'].or_(self.page.css=a[href*='/weather'])

    @property
    def health_link(self):
        """Link to Health news section."""
        return self.page.//a[text()='Health '].or_(self.page.css=a[href*='/health'])

    @property
    def wellness_link(self):
        """Link to Wellness news section."""
        return self.page.//a[text()='Wellness '].or_(self.page.css=a[href*='/wellness'])

    @property
    def nutrition_link(self):
        """Link to Nutrition news section."""
        return self.page.//a[text()='Nutrition '].or_(self.page.css=a[href*='/nutrition'])

    @property
    def fitness_link(self):
        """Link to Fitness news section."""
        return self.page.//a[text()='Fitness '].or_(self.page.css=a[href*='/fitness'])

    @property
    def originals_link(self):
        """Link to Originals news section."""
        return self.page.//a[text()='Originals '].or_(self.page.css=a[href*='/originals'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'AAPL'
        await Page contains the text 'News'
        await Page contains the text 'Health'