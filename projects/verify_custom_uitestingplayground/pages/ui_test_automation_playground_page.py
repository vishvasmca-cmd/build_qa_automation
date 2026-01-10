from playwright.async_api import Page, expect

class UiTestAutomationPlaygroundPage:
    """
    The UI Test Automation Playground is a website designed to provide a platform for sharpening UI test automation skills. The home page presents various scenarios that are common pitfalls in modern web applications.
    URL Pattern: http://uitestingplayground.com/
    """
    def __init__(self, page: Page):
        self.page = page

    @property
    def Dynamic ID Link(self):
        """Link to the Dynamic ID page."""
        return self.page.text=Dynamic ID.or_(self.page.css=a[href='/dynamicid'])

    @property
    def Class Attribute Link(self):
        """Link to the Class Attribute page."""
        return self.page.text=Class Attribute.or_(self.page.css=a[href='/classattr'])

    @property
    def Hidden Layers Link(self):
        """Link to the Hidden Layers page."""
        return self.page.text=Hidden Layers.or_(self.page.css=a[href='/hiddenlayers'])

    @property
    def Load Delay Link(self):
        """Link to the Load Delay page."""
        return self.page.text=Load Delay.or_(self.page.css=a[href='/loaddelay'])

    @property
    def AJAX Data Link(self):
        """Link to the AJAX Data page."""
        return self.page.text=AJAX Data.or_(self.page.css=a[href='/ajax'])

    @property
    def Client Side Delay Link(self):
        """Link to the Client Side Delay page."""
        return self.page.text=Client Side Delay.or_(self.page.css=a[href='/clientdelay'])

    @property
    def Click Link(self):
        """Link to the Click page."""
        return self.page.text=Click.or_(self.page.css=a[href='/click'])

    @property
    def Text Input Link(self):
        """Link to the Text Input page."""
        return self.page.text=Text Input.or_(self.page.css=a[href='/textinput'])

    async def verify_loaded(self):
        """Executes critical checks to ensure page is ready."""
        await Page title contains 'UI Test Automation Playground'
        await Page heading contains 'UI Test Automation Playground'
        await The purpose of this website is to provide a platform for sharpening UI test automation skills.