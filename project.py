import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class TestGitHubLogin(unittest.TestCase):

    def setUp(self):
        """Setup before each test"""
        self.driver = webdriver.Chrome() # Ensure ChromeDriver is in your PATH
        self.driver.maximize_window()

    def tearDown(self):
        """Teardown after each test"""
        self.driver.quit()

    def test_valid_login(self):
        """Test valid login on GitHub"""
        driver = self.driver
        driver.get("https://github.com/login")

        username_field = driver.find_element(By.ID, "login_field")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.NAME, "commit")

        username_field.send_keys("senthilloganathan30@gmail.com") # your GitHub username
        password_field.send_keys("senthil30@") # your GitHub password
        login_button.click()

        # Wait until the dashboard page loads
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='user-profile-nav']"))
        )

        # Assert that we are logged in (checking the presence of the user profile menu)
        user_profile = driver.find_element(By.XPATH, "//div[@class='user-profile-nav']")
        self.assertTrue(user_profile.is_displayed())

        print("✅ GitHub login test PASSED!")

        # Take a screenshot
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        driver.save_screenshot("screenshots/github_login_success.png")

    def test_invalid_login(self):
        """Test invalid login on GitHub"""
        driver = self.driver
        driver.get("https://github.com/login")

        username_field = driver.find_element(By.ID, "login_field")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.NAME, "commit")

        username_field.send_keys("wrongusername") # Invalid username
        password_field.send_keys("wrongpassword") # Invalid password
        login_button.click()

        # Wait for error message
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='flash flash-error']"))
        )

        error_message = driver.find_element(By.XPATH, "//div[@class='flash flash-error']")
        self.assertIn("Incorrect username or password.", error_message.text)

        print("❌ GitHub login test FAILED as expected with invalid credentials.")

        # Take a screenshot
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        driver.save_screenshot("screenshots/github_login_failed.png")

if __name__ == "__main__":
    try:
        unittest.main(exit=False) # Prevent SystemExit in interactive mode
    except SystemExit as e:
        print(f"Test run failed with exit code: {e.code}")