"""
Selenium WebDriver test with Python
E-commerce application testing - contains flaky patterns and code issues
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


class TestSeleniumPythonEcommerce:
    """Selenium Python test suite for e-commerce."""
    
    def setUp(self):
        """Setup method - creates driver instance."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        # ISSUE: No corresponding tearDown method
    
    def test_user_login_and_verify_dashboard_with_multiple_validations(self):
        """Test user login - ISSUE: Long function name."""
        driver = self.driver
        driver.get("https://demo-shop.example.com/login")
        
        # FLAKY: Hard-coded sleep
        time.sleep(5)
        
        # Find elements
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        
        username.send_keys("testuser@example.com")
        password.send_keys("Test@1234")
        
        # Click login
        driver.find_element(By.ID, "login-button").click()
        
        # FLAKY: Another hard-coded sleep
        time.sleep(3)
        
        # Verify dashboard
        assert "Dashboard" in driver.title
    
    def test_search_and_filter_products(self):
        """Search for products and apply filters."""
        driver = self.driver
        driver.get("https://demo-shop.example.com")
        
        time.sleep(3)
        
        # Search for product
        search_box = driver.find_element(By.NAME, "search")
        
        # FLAKY: Random search term
        search_terms = ["laptop", "phone", "tablet", "headphones"]
        search_term = random.choice(search_terms)
        
        search_box.send_keys(search_term)
        search_box.submit()
        
        time.sleep(2)
        
        # Apply price filter
        min_price = driver.find_element(By.ID, "min-price")
        max_price = driver.find_element(By.ID, "max-price")
        
        # FLAKY: Random price values
        min_price.send_keys(str(random.randint(100, 500)))
        max_price.send_keys(str(random.randint(1000, 2000)))
        
        driver.find_element(By.ID, "apply-filter").click()
        
        time.sleep(3)
        
        # Verify results
        results = driver.find_elements(By.CLASS_NAME, "product-item")
        assert len(results) > 0
    
    def test_add_to_cart_and_checkout(self):
        """Test adding product to cart and checkout process."""
        driver = self.driver
        
        # DUPLICATE CODE - START (similar pattern in test_add_multiple_items)
        driver.get("https://demo-shop.example.com/products")
        
        time.sleep(3)
        
        # Click first product
        products = driver.find_elements(By.CLASS_NAME, "product-card")
        products[0].click()
        
        time.sleep(2)
        
        # Add to cart
        driver.find_element(By.ID, "add-to-cart").click()
        
        time.sleep(2)
        # DUPLICATE CODE - END
        
        # Go to cart
        driver.find_element(By.ID, "cart-icon").click()
        
        time.sleep(2)
        
        # Proceed to checkout
        driver.find_element(By.ID, "checkout-button").click()
        
        time.sleep(3)
        
        # Fill checkout form
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "email").send_keys("john@example.com")
        driver.find_element(By.ID, "phone").send_keys("1234567890")
        driver.find_element(By.ID, "address").send_keys("123 Main St")
        driver.find_element(By.ID, "city").send_keys("New York")
        driver.find_element(By.ID, "zipcode").send_keys("10001")
        
        # Submit order
        driver.find_element(By.ID, "place-order").click()
        
        time.sleep(5)
        
        # Verify confirmation
        confirmation = driver.find_element(By.CLASS_NAME, "order-confirmation")
        assert confirmation.is_displayed()
    
    def test_add_multiple_items_to_cart(self):
        """Test adding multiple items to cart."""
        driver = self.driver
        
        # DUPLICATE CODE - START (similar to above)
        driver.get("https://demo-shop.example.com/products")
        
        time.sleep(3)
        
        # Add first 3 products
        products = driver.find_elements(By.CLASS_NAME, "product-card")
        for i in range(3):
            products[i].click()
            
            time.sleep(2)
            
            driver.find_element(By.ID, "add-to-cart").click()
            
            time.sleep(2)
            # DUPLICATE CODE - END
            
            driver.back()
            time.sleep(2)
        
        # Verify cart count
        cart_count = driver.find_element(By.ID, "cart-count")
        assert int(cart_count.text) == 3
    
    def test_product_availability_via_api(self):
        """Check product availability using API - FLAKY: External call."""
        # FLAKY: Unmocked external API call
        response = requests.get("https://api.demo-shop.example.com/products/12345")
        
        # ISSUE: Broad exception handling
        try:
            assert response.status_code == 200
            data = response.json()
            assert data["available"] == True
        except Exception as e:
            print(f"API test failed: {e}")
    
    def test_wait_for_element_with_polling_loop(self):
        """Test element waiting - FLAKY: Polling loop."""
        driver = self.driver
        driver.get("https://demo-shop.example.com/products")
        
        time.sleep(2)
        
        # Click on dynamic content button
        driver.find_element(By.ID, "load-reviews").click()
        
        # FLAKY: Polling loop instead of explicit wait
        timeout = 0
        element_found = False
        while not element_found and timeout < 10:
            try:
                reviews = driver.find_elements(By.CLASS_NAME, "review-item")
                if len(reviews) > 0:
                    element_found = True
            except:
                pass
            time.sleep(1)
            timeout += 1
        
        assert element_found
    
    def test_implicit_wait_usage(self):
        """Test with implicit wait - FLAKY: Implicit wait."""
        driver = self.driver
        
        # FLAKY: Implicit wait usage
        driver.implicitly_wait(10)
        
        driver.get("https://demo-shop.example.com")
        
        # Find element
        search_box = driver.find_element(By.ID, "search")
        search_box.send_keys("laptop")
        search_box.submit()
        
        # Verify results
        results = driver.find_elements(By.CLASS_NAME, "product-item")
        assert len(results) > 0
    
    def test_form_validation_with_complex_logic(self):
        """Test form validation - MAINTAINABILITY: High complexity."""
        driver = self.driver
        driver.get("https://demo-shop.example.com/contact")
        
        time.sleep(2)
        
        # MAINTAINABILITY: Too many nested conditionals
        test_cases = [
            {"name": "", "email": "test@example.com", "message": "Hello"},
            {"name": "John", "email": "", "message": "Hello"},
            {"name": "John", "email": "invalid-email", "message": "Hello"},
            {"name": "John", "email": "test@example.com", "message": ""},
            {"name": "A" * 200, "email": "test@example.com", "message": "Hello"},
        ]
        
        for test_case in test_cases:
            name = test_case["name"]
            email = test_case["email"]
            message = test_case["message"]
            
            driver.find_element(By.ID, "name").clear()
            driver.find_element(By.ID, "name").send_keys(name)
            
            driver.find_element(By.ID, "email").clear()
            driver.find_element(By.ID, "email").send_keys(email)
            
            driver.find_element(By.ID, "message").clear()
            driver.find_element(By.ID, "message").send_keys(message)
            
            driver.find_element(By.ID, "submit").click()
            
            time.sleep(1)
            
            # Complex validation logic
            if not name:
                error = driver.find_element(By.ID, "name-error")
                if error.is_displayed():
                    if "required" in error.text.lower():
                        print("Name validation works")
            elif len(name) > 100:
                error = driver.find_element(By.ID, "name-error")
                if error.is_displayed():
                    print("Name length validation works")
            
            if not email:
                error = driver.find_element(By.ID, "email-error")
                if error.is_displayed():
                    print("Email validation works")
            elif "@" not in email:
                error = driver.find_element(By.ID, "email-error")
                if error.is_displayed():
                    print("Email format validation works")
            
            if not message:
                error = driver.find_element(By.ID, "message-error")
                if error.is_displayed():
                    print("Message validation works")
    
    def test_no_assertion(self):
        """Test without assertion - ISSUE: Missing assertion."""
        driver = self.driver
        driver.get("https://demo-shop.example.com")
        
        time.sleep(3)
        
        # Click on products
        driver.find_element(By.LINK_TEXT, "Products").click()
        
        time.sleep(2)
        
        # ISSUE: No assertion to verify anything


# ISSUE: Test function outside class (poor organization)
def test_newsletter_subscription():
    """Test newsletter subscription - standalone function."""
    driver = webdriver.Chrome()
    driver.get("https://demo-shop.example.com")
    
    time.sleep(3)
    
    # Scroll to footer
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    
    time.sleep(2)
    
    email = driver.find_element(By.ID, "newsletter-email")
    email.send_keys("test@example.com")
    
    driver.find_element(By.ID, "subscribe-button").click()
    
    time.sleep(2)
    
    success = driver.find_element(By.CLASS_NAME, "success-message")
    assert success.is_displayed()
    
    driver.quit()
