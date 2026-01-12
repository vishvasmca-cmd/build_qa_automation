from playwright.async_api import Page, expect

class HomePage:
    """
    The home page of Katalon, designed to introduce the Katalon Studio and its capabilities for automated testing.
    URL Pattern: https://katalon.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def katalon_logo(self):
        """The Katalon logo in the top left corner."""
        return self.page.locator("//a[@class='logo']").or_(self.page.locator("img[alt='Katalon']"))

    @property
    def products_dropdown(self):
        """Dropdown menu for Katalon products."""
        return self.page.locator("//div[@class='top_nav_menu_item'][1]/button").or_(self.page.get_by_text("Products"))

    @property
    def solutions_dropdown(self):
        """Dropdown menu for Katalon solutions."""
        return self.page.locator("//div[@class='top_nav_menu_item'][2]/button").or_(self.page.get_by_text("Solutions"))

    @property
    def katalon_pricing_link(self):
        """Link to the Katalon pricing page."""
        return self.page.locator("//a[text()='Katalon Pricing']").or_(self.page.get_by_text("Katalon Pricing"))

    @property
    def resources_dropdown(self):
        """Dropdown menu for Katalon resources."""
        return self.page.locator("//div[@class='top_nav_menu_item'][3]/button").or_(self.page.get_by_text("Resources"))

    @property
    def view_demo_button(self):
        """Button to view a Katalon demo."""
        return self.page.locator("//a[text()='View Demo']").or_(self.page.get_by_text("View Demo"))

    @property
    def download_studio_button(self):
        """Button to download Katalon Studio."""
        return self.page.locator("//a[text()='Download Studio']").or_(self.page.get_by_text("Download Studio"))

    @property
    def learn_more_button(self):
        """Button to learn more about Katalon Studio."""
        return self.page.locator("//a[text()='Learn more']").or_(self.page.get_by_text("Learn more"))

    @property
    def integrations_button(self):
        """Button to explore Katalon integrations."""
        return self.page.locator("//a[text()='Integrations']").or_(self.page.get_by_text("Integrations"))

    @property
    def accept_all_cookies_button(self):
        """Button to accept all cookies."""
        return self.page.locator("//button[text()='Accept All Cookies']").or_(self.page.get_by_text("Accept All Cookies"))

    @property
    def reject_all_cookies_button(self):
        """Button to reject all cookies."""
        return self.page.locator("//button[text()='Reject All']").or_(self.page.get_by_text("Reject All"))

    @property
    def cookies_settings_button(self):
        """Button to customize cookie settings."""
        return self.page.locator("//button[text()='Cookies Settings']").or_(self.page.get_by_text("Cookies Settings"))

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await expect(self.page).to_have_title(re.compile(r'.*Katalon.*', re.I))
        # Verify the main header text is 'Katalon Studio'
        # Verify the 'Learn more' button is present
        # Verify the 'Download Studio' button is present