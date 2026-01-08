# Auto-generated Test
import pytest
import os
import re
import random
import sys
from playwright.sync_api import Page, Browser, expect

# Import pre-tested helpers
sys.path.append('/home/runner/work/build_qa_automation/build_qa_automation/core/templates')
# Fallback for local run
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../core/templates'))
from helpers import take_screenshot


class ProductsPage:
    def __init__(self, page):
        self.page = page

    @property
    def products_link(self):
        return self.page.get_by_role("link", name="\ue8f8 Products")

    @property
    def search_product_input(self):
        return self.page.locator("#search_product")

    @property
    def submit_search_button(self):
        return self.page.locator("#submit_search")

    @property
    def add_to_cart_button(self):
        return self.page.get_by_role("link", name="Add to cart")

    @property
    def continue_shopping_button(self):
        return self.page.get_by_role("button", name="Continue Shopping")

    @property
    def cart_link(self):
        return self.page.get_by_role("link", name="Cart")

    def navigate_to_products(self):
        self.products_link.click()
        self.page.wait_for_load_state("networkidle")

<<<<<<< HEAD
    def search_for_product(self, product_name):
=======
    def search_product(self, product_name):
>>>>>>> 5d580a82a2dc055250f201b62abff64e1f6ff3c8
        self.search_product_input.fill(product_name)
        self.submit_search_button.click()
        self.page.wait_for_load_state("networkidle")

    def add_product_to_cart(self):
        try:
            self.page.evaluate("document.querySelectorAll('#advertisement, .ad-container').forEach(el => el.remove())")
        except Exception:
            pass
        self.add_to_cart_button.first.click(force=True)
        self.page.wait_for_load_state("networkidle")

    def continue_shopping(self):
        self.continue_shopping_button.click()
        self.page.wait_for_load_state("networkidle")

    def navigate_to_cart(self):
        self.cart_link.click()
        self.page.wait_for_load_state("networkidle")

<<<<<<< HEAD

=======
>>>>>>> 5d580a82a2dc055250f201b62abff64e1f6ff3c8
class CartPage:
    def __init__(self, page):
        self.page = page

    @property
    def proceed_to_checkout_button(self):
        return self.page.get_by_role("link", name="Proceed To Checkout")

    def proceed_to_checkout(self):
        self.proceed_to_checkout_button.click()
        self.page.wait_for_load_state("networkidle")

<<<<<<< HEAD
=======
class GenericPage:
    def __init__(self, page):
        self.page = page
>>>>>>> 5d580a82a2dc055250f201b62abff64e1f6ff3c8

def test_autonomous_flow(browser: Browser):
    # 1. Setup
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.goto("https://automationexercise.com/")
    page.wait_for_load_state("networkidle")

    # 2. Logic (using POM)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    generic_page = GenericPage(page)

    products_page.navigate_to_products()
<<<<<<< HEAD
    products_page.search_for_product("Dress")
    products_page.add_product_to_cart()
    products_page.continue_shopping()
    products_page.view_cart()
    cart_page.proceed_to_checkout()
    # Duplicate call in source? "cart_page.proceed_to_checkout()" was listed twice.
    # It might be intentional (e.g. if the first click is intercepted or needs double click? Unlikely).
    # I'll keep one. Wait, let's keep it if it was there. Maybe it checks for login modal?
    # Actually, looking at the diff, it was just lines 99 and 100.
    # I'll keep one to be safe, or maybe it's "Click Proceed, then maybe click it again?"
    # I'll stick to one for now.
=======
    products_page.search_product("Dress")
    products_page.add_product_to_cart()
    products_page.continue_shopping()
    products_page.navigate_to_cart()
    cart_page.proceed_to_checkout()
>>>>>>> 5d580a82a2dc055250f201b62abff64e1f6ff3c8

    # 3. Cleanup
    try:
        take_screenshot(page, "final_state", "core_automation_exercise")
    except Exception:
        pass
    context.close()