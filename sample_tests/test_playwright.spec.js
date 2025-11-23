/**
 * Playwright E2E Tests for E-commerce Application (JavaScript)
 * Contains flaky patterns and code quality issues
 */

const { test, expect } = require('@playwright/test');

test.describe('E-commerce Application Tests', () => {
  
  // ISSUE: No proper beforeEach/afterEach setup
  
  test('should login with valid credentials', async ({ page }) => {
    await page.goto('https://demo-shop.example.com/login');
    
    // FLAKY: Hard-coded wait
    await page.waitForTimeout(5000);
    
    await page.fill('#username', 'testuser@example.com');
    await page.fill('#password', 'Test@1234');
    
    await page.click('#login-button');
    
    // FLAKY: Another hard-coded wait
    await page.waitForTimeout(3000);
    
    await expect(page).toHaveTitle(/Dashboard/);
  });
  
  test('should search for products and apply filters', async ({ page }) => {
    await page.goto('https://demo-shop.example.com');
    
    // FLAKY: Hard-coded wait
    await page.waitForTimeout(3000);
    
    // FLAKY: Random search term
    const searchTerms = ['laptop', 'phone', 'tablet', 'camera'];
    const randomTerm = searchTerms[Math.floor(Math.random() * searchTerms.length)];
    
    await page.fill('[name="search"]', randomTerm);
    await page.press('[name="search"]', 'Enter');
    
    await page.waitForTimeout(2000);
    
    // Apply filters
    await page.click('#price-filter');
    await page.waitForTimeout(1000);
    
    // FLAKY: Random selection
    const priceOptions = ['#price-0-500', '#price-500-1000', '#price-1000-2000'];
    const randomPrice = priceOptions[Math.floor(Math.random() * priceOptions.length)];
    await page.click(randomPrice);
    
    await page.waitForTimeout(2000);
    
    const products = await page.locator('.product-card').count();
    expect(products).toBeGreaterThan(0);
  });
  
  test('should add product to cart and checkout', async ({ page }) => {
    await page.goto('https://demo-shop.example.com/products');
    
    // FLAKY: Hard-coded wait
    await page.waitForTimeout(3000);
    
    // Click first product
    await page.locator('.product-card').first().click();
    
    await page.waitForTimeout(2000);
    
    // Add to cart
    await page.click('#add-to-cart');
    
    await page.waitForTimeout(2000);
    
    // Go to cart
    await page.click('#cart-icon');
    
    await page.waitForTimeout(2000);
    
    // Checkout
    await page.click('#checkout-button');
    
    await page.waitForTimeout(3000);
    
    // DUPLICATE CODE - START (similar pattern in multiple tests)
    await page.fill('#first-name', 'John');
    await page.fill('#last-name', 'Doe');
    await page.fill('#email', 'john@example.com');
    await page.fill('#phone', '1234567890');
    await page.fill('#address', '123 Main St');
    await page.fill('#city', 'New York');
    await page.fill('#zipcode', '10001');
    // DUPLICATE CODE - END
    
    await page.click('#place-order');
    
    await page.waitForTimeout(5000);
    
    await expect(page.locator('.order-confirmation')).toBeVisible();
  });
  
  test('should add multiple items to cart', async ({ page }) => {
    await page.goto('https://demo-shop.example.com/products');
    
    await page.waitForTimeout(3000);
    
    // Add first 3 products
    const products = page.locator('.product-card');
    const count = await products.count();
    
    for (let i = 0; i < Math.min(3, count); i++) {
      await products.nth(i).click();
      await page.waitForTimeout(2000);
      
      await page.click('#add-to-cart');
      await page.waitForTimeout(2000);
      
      await page.goBack();
      await page.waitForTimeout(2000);
    }
    
    // Verify cart count
    const cartCount = await page.locator('#cart-count').textContent();
    expect(parseInt(cartCount)).toBe(3);
  });
  
  test('should check product availability via API', async ({ request }) => {
    // FLAKY: External API call without mocking
    const response = await request.get('https://api.demo-shop.example.com/products/12345');
    
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    expect(data.available).toBe(true);
  });
  
  test('should wait for dynamic content with polling loop', async ({ page }) => {
    await page.goto('https://demo-shop.example.com/products');
    
    await page.waitForTimeout(2000);
    
    await page.click('#load-reviews');
    
    // FLAKY: Custom polling loop instead of proper wait
    let attempts = 0;
    let reviewsFound = false;
    
    while (!reviewsFound && attempts < 10) {
      const reviews = await page.locator('.review-item').count();
      if (reviews > 0) {
        reviewsFound = true;
      } else {
        await page.waitForTimeout(1000);
        attempts++;
      }
    }
    
    expect(reviewsFound).toBeTruthy();
  });
  
  test('should validate form with complex nested conditions and multiple validation scenarios', async ({ page }) => {
    // MAINTAINABILITY: Long test name and complex logic
    await page.goto('https://demo-shop.example.com/contact');
    
    await page.waitForTimeout(2000);
    
    // MAINTAINABILITY: Too many nested conditions and branches
    const testCases = [
      { name: '', email: 'test@example.com', message: 'Hello' },
      { name: 'John', email: '', message: 'Hello' },
      { name: 'John', email: 'invalid-email', message: 'Hello' },
      { name: 'John', email: 'test@example.com', message: '' },
      { name: 'A'.repeat(200), email: 'test@example.com', message: 'Hello' }
    ];
    
    for (const testCase of testCases) {
      await page.fill('#name', testCase.name);
      await page.fill('#email', testCase.email);
      await page.fill('#message', testCase.message);
      
      await page.click('#submit');
      
      await page.waitForTimeout(1000);
      
      // Complex validation - too many nested ifs
      if (!testCase.name) {
        const nameError = page.locator('#name-error');
        await expect(nameError).toBeVisible();
        const errorText = await nameError.textContent();
        if (errorText.includes('required')) {
          console.log('Name validation works');
        }
      } else if (testCase.name.length > 100) {
        const nameError = page.locator('#name-error');
        if (await nameError.isVisible()) {
          console.log('Name length validation works');
        }
      }
      
      if (!testCase.email) {
        await expect(page.locator('#email-error')).toBeVisible();
      } else if (!testCase.email.includes('@')) {
        const emailError = page.locator('#email-error');
        if (await emailError.isVisible()) {
          const errorText = await emailError.textContent();
          if (errorText.includes('invalid')) {
            console.log('Email format validation works');
          }
        }
      }
      
      if (!testCase.message) {
        await expect(page.locator('#message-error')).toBeVisible();
      }
    }
  });
  
  test('should test without proper assertions', async ({ page }) => {
    // ISSUE: No assertions
    await page.goto('https://demo-shop.example.com');
    
    await page.waitForTimeout(3000);
    
    await page.click('[href="/products"]');
    
    await page.waitForTimeout(2000);
    
    // Test ends without verifying anything
  });
  
  test('should handle multiple tabs', async ({ context, page }) => {
    await page.goto('https://demo-shop.example.com');
    
    await page.waitForTimeout(2000);
    
    // Click link that opens new tab
    const [newPage] = await Promise.all([
      context.waitForEvent('page'),
      page.click('#help-link')
    ]);
    
    await page.waitForTimeout(3000);
    
    await expect(newPage).toHaveURL(/.*help/);
    
    await newPage.close();
  });
  
  test('should perform complete e2e flow with registration and checkout', async ({ page }) => {
    // MAINTAINABILITY: Single test doing too much (God test)
    
    await page.goto('https://demo-shop.example.com/register');
    
    await page.waitForTimeout(2000);
    
    // FLAKY: Random email
    const randomEmail = `user${Math.random().toString(36).substring(7)}@example.com`;
    
    await page.fill('#reg-email', randomEmail);
    await page.fill('#reg-password', 'Test@1234');
    await page.fill('#reg-confirm', 'Test@1234');
    await page.click('#register-submit');
    
    await page.waitForTimeout(3000);
    
    // Login
    await page.fill('#username', randomEmail);
    await page.fill('#password', 'Test@1234');
    await page.click('#login-button');
    
    await page.waitForTimeout(3000);
    
    // Search
    await page.fill('[name="search"]', 'laptop');
    await page.press('[name="search"]', 'Enter');
    
    await page.waitForTimeout(2000);
    
    // Add to cart
    await page.locator('.product-card').first().click();
    await page.waitForTimeout(2000);
    await page.click('#add-to-cart');
    await page.waitForTimeout(2000);
    
    // Checkout
    await page.click('#cart-icon');
    await page.waitForTimeout(2000);
    await page.click('#checkout-button');
    await page.waitForTimeout(3000);
    
    // Fill checkout form - DUPLICATE CODE
    await page.fill('#first-name', 'John');
    await page.fill('#last-name', 'Doe');
    await page.fill('#address', '123 Main St');
    await page.fill('#city', 'New York');
    await page.fill('#zipcode', '10001');
    
    await page.click('#place-order');
    await page.waitForTimeout(5000);
    
    await expect(page.locator('.order-confirmation')).toBeVisible();
  });
});

// ISSUE: Test outside describe block (poor organization)
test('standalone test without test suite', async ({ page }) => {
  await page.goto('https://demo-shop.example.com');
  await page.waitForTimeout(2000);
  // No assertions
});

