from playwright.async_api import Page, expect

class YahooFinanceStockMarketLiveQuotesBusinessFinanceNewsPage:
    """
    This page provides a comprehensive overview of news, finance, and market data. It allows users to track stock quotes, business news, and financial information.
    URL Pattern: https://finance.yahoo.com/markets/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def news(self):
        """Link to the News section."""
        return self.page.text=News.or_(self.page.css=a[href*='/news/'])

    @property
    def today_s_news(self):
        """Link to the Today's news section."""
        return self.page.text=Today's news.or_(self.page.css=a[href*='/news/today'])

    @property
    def us(self):
        """Link to the US section."""
        return self.page.text=US.or_(self.page.css=a[href*='/us'])

    @property
    def politics(self):
        """Link to the Politics section."""
        return self.page.text=Politics.or_(self.page.css=a[href*='/politics'])

    @property
    def _2025_election(self):
        """Link to the 2025 Election section."""
        return self.page.text=2025 Election.or_(self.page.css=a[href*='/2025-election'])

    @property
    def world(self):
        """Link to the World section."""
        return self.page.text=World.or_(self.page.css=a[href*='/world'])

    @property
    def weather(self):
        """Link to the Weather section."""
        return self.page.text=Weather.or_(self.page.css=a[href*='/weather'])

    @property
    def climate_change(self):
        """Link to the Climate change section."""
        return self.page.text=Climate change.or_(self.page.css=a[href*='/climate-change'])

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
    def sexual_health(self):
        """Link to the Sexual health section."""
        return self.page.text=Sexual health.or_(self.page.css=a[href*='/sexual-health'])

    @property
    def dermatology(self):
        """Link to the Dermatology section."""
        return self.page.text=Dermatology.or_(self.page.css=a[href*='/dermatology'])

    @property
    def oral_health(self):
        """Link to the Oral health section."""
        return self.page.text=Oral health.or_(self.page.css=a[href*='/oral-health'])

    @property
    def hair_loss(self):
        """Link to the Hair loss section."""
        return self.page.text=Hair loss.or_(self.page.css=a[href*='/hair-loss'])

    @property
    def foot_health(self):
        """Link to the Foot health section."""
        return self.page.text=Foot health.or_(self.page.css=a[href*='/foot-health'])

    @property
    def nutrition(self):
        """Link to the Nutrition section."""
        return self.page.text=Nutrition.or_(self.page.css=a[href*='/nutrition'])

    @property
    def healthy_eating(self):
        """Link to the Healthy eating section."""
        return self.page.text=Healthy eating.or_(self.page.css=a[href*='/healthy-eating'])

    @property
    def meal_delivery(self):
        """Link to the Meal delivery section."""
        return self.page.text=Meal delivery.or_(self.page.css=a[href*='/meal-delivery'])

    @property
    def weight_loss(self):
        """Link to the Weight loss section."""
        return self.page.text=Weight loss.or_(self.page.css=a[href*='/weight-loss'])

    @property
    def vitamins_and_supplements(self):
        """Link to the Vitamins and supplements section."""
        return self.page.text=Vitamins and supplements.or_(self.page.css=a[href*='/vitamins-and-supplements'])

    @property
    def fitness(self):
        """Link to the Fitness section."""
        return self.page.text=Fitness.or_(self.page.css=a[href*='/fitness'])

    @property
    def equipment(self):
        """Link to the Equipment section."""
        return self.page.text=Equipment.or_(self.page.css=a[href*='/equipment'])

    @property
    def exercise(self):
        """Link to the Exercise section."""
        return self.page.text=Exercise.or_(self.page.css=a[href*='/exercise'])

    @property
    def women_s_health(self):
        """Link to the Women's health section."""
        return self.page.text=Women's health.or_(self.page.css=a[href*='/womens-health'])

    @property
    def sleep(self):
        """Link to the Sleep section."""
        return self.page.text=Sleep.or_(self.page.css=a[href*='/sleep'])

    @property
    def healthy_aging(self):
        """Link to the Healthy aging section."""
        return self.page.text=Healthy aging.or_(self.page.css=a[href*='/healthy-aging'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Title contains 'Yahoo Finance - Stock Market Live, Quotes, Business & Finance News'
        await Page contains the 'News' link
        await Page contains the 'Today's news' link