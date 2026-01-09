from playwright.async_api import Page, expect

class UiTestAutomationPlaygroundPage:
    """
    The UI Test Automation Playground is a website designed to provide a platform for sharpening UI test automation skills. The home page presents various common automation challenges as individual scenarios.
    URL Pattern: http://uitestingplayground.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Page Header(self):
        """The main heading of the page."""
        return self.page.role=heading[name="UI Test Automation Playground"].or_(self.page.css=h1)

    @property
    def Dynamic ID Link(self):
        """Link to the Dynamic ID challenge page."""
        return self.page.role=link[name="Dynamic ID"].or_(self.page.text=Dynamic ID)

    @property
    def Class Attribute Link(self):
        """Link to the Class Attribute challenge page."""
        return self.page.role=link[name="Class Attribute"].or_(self.page.text=Class Attribute)

    @property
    def Hidden Layers Link(self):
        """Link to the Hidden Layers challenge page."""
        return self.page.role=link[name="Hidden Layers"].or_(self.page.text=Hidden Layers)

    @property
    def Load Delay Link(self):
        """Link to the Load Delay challenge page."""
        return self.page.role=link[name="Load Delay"].or_(self.page.text=Load Delay)

    @property
    def AJAX Data Link(self):
        """Link to the AJAX Data challenge page."""
        return self.page.role=link[name="AJAX Data"].or_(self.page.text=AJAX Data)

    @property
    def Client Side Delay Link(self):
        """Link to the Client Side Delay challenge page."""
        return self.page.role=link[name="Client Side Delay"].or_(self.page.text=Client Side Delay)

    @property
    def Click Link(self):
        """Link to the Click challenge page."""
        return self.page.role=link[name="Click"].or_(self.page.text=Click)

    @property
    def Text Input Link(self):
        """Link to the Text Input challenge page."""
        return self.page.role=link[name="Text Input"].or_(self.page.text=Text Input)

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title is 'UI Test Automation Playground'
        await Page header 'UI Test Automation Playground' is displayed
        await The Dynamic ID link is present
        await The Class Attribute link is present
        await The Hidden Layers link is present
        await The Load Delay link is present
        await The AJAX Data link is present
        await The Client Side Delay link is present
        await The Click link is present
        await The Text Input link is present