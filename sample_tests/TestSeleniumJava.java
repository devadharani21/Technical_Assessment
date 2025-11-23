/**
 * Selenium WebDriver test with Java
 * E-commerce application testing - contains flaky patterns and code issues
 */

package com.example.tests;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.testng.Assert;
import org.testng.annotations.*;
import java.util.List;
import java.util.Random;

public class TestSeleniumJava {
    
    private WebDriver driver;
    private Random random = new Random();
    
    @BeforeMethod
    public void setUp() {
        System.setProperty("webdriver.chrome.driver", "/path/to/chromedriver");
        driver = new ChromeDriver();
        driver.manage().window().maximize();
    }
    
    @AfterMethod
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
    
    @Test
    public void testUserLoginWithValidCredentials() {
        driver.get("https://demo-shop.example.com/login");
        
        // FLAKY: Hard-coded sleep
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        WebElement username = driver.findElement(By.id("username"));
        WebElement password = driver.findElement(By.id("password"));
        
        username.sendKeys("testuser@example.com");
        password.sendKeys("Test@1234");
        
        driver.findElement(By.id("login-button")).click();
        
        // FLAKY: Another hard-coded sleep
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        Assert.assertTrue(driver.getTitle().contains("Dashboard"));
    }
    
    @Test
    public void testSearchProductsAndApplyFilters() {
        driver.get("https://demo-shop.example.com");
        
        // FLAKY: Hard-coded sleep
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        WebElement searchBox = driver.findElement(By.name("search"));
        
        // FLAKY: Random search term
        String[] searchTerms = {"laptop", "phone", "tablet", "camera"};
        String searchTerm = searchTerms[random.nextInt(searchTerms.length)];
        
        searchBox.sendKeys(searchTerm);
        searchBox.submit();
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // Apply filters
        WebElement priceFilter = driver.findElement(By.id("price-filter"));
        priceFilter.click();
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // FLAKY: Random price selection
        driver.findElement(By.id("price-500-1000")).click();
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        List<WebElement> products = driver.findElements(By.className("product-card"));
        Assert.assertTrue(products.size() > 0);
    }
    
    @Test
    public void testAddToCartAndCheckout() {
        driver.get("https://demo-shop.example.com/products");
        
        // FLAKY: Hard-coded sleep
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // Click first product
        List<WebElement> products = driver.findElements(By.className("product-card"));
        products.get(0).click();
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // Add to cart
        driver.findElement(By.id("add-to-cart")).click();
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // Go to cart
        driver.findElement(By.id("cart-icon")).click();
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // Checkout
        driver.findElement(By.id("checkout-button")).click();
        
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // Fill form - DUPLICATE CODE (similar pattern in multiple tests)
        driver.findElement(By.id("first-name")).sendKeys("John");
        driver.findElement(By.id("last-name")).sendKeys("Doe");
        driver.findElement(By.id("email")).sendKeys("john@example.com");
        driver.findElement(By.id("address")).sendKeys("123 Main St");
        driver.findElement(By.id("city")).sendKeys("New York");
        driver.findElement(By.id("zipcode")).sendKeys("10001");
        
        driver.findElement(By.id("place-order")).click();
        
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        WebElement confirmation = driver.findElement(By.className("order-confirmation"));
        Assert.assertTrue(confirmation.isDisplayed());
    }
    
    @Test
    public void testPollingForDynamicContent() {
        driver.get("https://demo-shop.example.com/products");
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        driver.findElement(By.id("load-more")).click();
        
        // FLAKY: Polling loop instead of explicit wait
        boolean elementFound = false;
        int timeout = 0;
        while (!elementFound && timeout < 10) {
            try {
                List<WebElement> products = driver.findElements(By.className("product-card"));
                if (products.size() > 10) {
                    elementFound = true;
                }
            } catch (Exception e) {
                // Ignore
            }
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            timeout++;
        }
        
        Assert.assertTrue(elementFound);
    }
    
    @Test
    public void testComplexFormValidationWithMultipleNestedConditions() {
        // MAINTAINABILITY: Function name too long and complex logic
        driver.get("https://demo-shop.example.com/register");
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // MAINTAINABILITY: Too many nested conditions
        String[] testEmails = {"", "invalid", "test@example", "valid@example.com"};
        String[] testPasswords = {"", "123", "weak", "StrongP@ss123"};
        
        for (String email : testEmails) {
            for (String password : testPasswords) {
                driver.findElement(By.id("email")).clear();
                driver.findElement(By.id("email")).sendKeys(email);
                
                driver.findElement(By.id("password")).clear();
                driver.findElement(By.id("password")).sendKeys(password);
                
                driver.findElement(By.id("register-button")).click();
                
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                
                if (email.isEmpty()) {
                    try {
                        WebElement error = driver.findElement(By.id("email-error"));
                        if (error.isDisplayed()) {
                            if (error.getText().contains("required")) {
                                System.out.println("Email required validation works");
                            }
                        }
                    } catch (Exception e) {
                        // Element not found
                    }
                } else if (!email.contains("@")) {
                    try {
                        WebElement error = driver.findElement(By.id("email-error"));
                        if (error.isDisplayed()) {
                            System.out.println("Email format validation works");
                        }
                    } catch (Exception e) {
                        // Element not found
                    }
                }
                
                if (password.isEmpty()) {
                    try {
                        WebElement error = driver.findElement(By.id("password-error"));
                        if (error.isDisplayed()) {
                            System.out.println("Password required validation works");
                        }
                    } catch (Exception e) {
                        // Element not found
                    }
                } else if (password.length() < 8) {
                    try {
                        WebElement error = driver.findElement(By.id("password-error"));
                        if (error.isDisplayed()) {
                            System.out.println("Password length validation works");
                        }
                    } catch (Exception e) {
                        // Element not found
                    }
                }
            }
        }
    }
    
    @Test
    public void testWithoutAssertion() {
        // ISSUE: No assertion in test
        driver.get("https://demo-shop.example.com");
        
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        driver.findElement(By.linkText("Products")).click();
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        // ISSUE: Test ends without any verification
    }
    
    @Test
    public void testImplicitWaitUsage() {
        // FLAKY: Using implicit wait
        driver.manage().timeouts().implicitlyWait(10, java.util.concurrent.TimeUnit.SECONDS);
        
        driver.get("https://demo-shop.example.com");
        
        WebElement searchBox = driver.findElement(By.id("search"));
        searchBox.sendKeys("laptop");
        searchBox.submit();
        
        List<WebElement> results = driver.findElements(By.className("product-item"));
        Assert.assertTrue(results.size() > 0);
    }
}

