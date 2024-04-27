import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


import requests
import socket

import time

SCORINGBOT_USERNAME = 'scoringbot'
SCORINGBOT_PASSWORD = 'Jingles.Flower!8461'

PINGO_DOMAIN = 'pingo.example.com'

PING_HOSTNAME = 'pingo.example.com'

class TestMisc(unittest.TestCase):
    def test_dns(self):
        try:
            socket.gethostbyname(PINGO_DOMAIN)
        except socket.gaierror:
            self.fail(f"DNS resolution failed for {PINGO_DOMAIN}")

    def test_ssl(self):
        try:
            requests.get(f'https://{PINGO_DOMAIN}')
        except requests.exceptions.SSLError:
            self.fail(f"SSL verification failed for {PINGO_DOMAIN}")

class TestSelenium(unittest.TestCase):
    def setUp(self):
        # headless
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        #chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration

        # Initialize WebDriver with headless mode
        self.driver = webdriver.Chrome(options=chrome_options)
    def tearDown(self):
        self.driver.quit()

    def _test_website(self, protocol='http://'):
        self.driver.get(f'{protocol}{PINGO_DOMAIN}')

        # wait for the page to load
        time.sleep(2)

        # Assert the title of the page
        self.assertEqual(self.driver.title, 'Login', 'Title of the page is not "Login"')

        # Assert the computed style of username field, height should be "37px"
        username_input = self.driver.find_element(By.NAME, 'username')
        self.assertEqual(username_input.value_of_css_property('height'), '37px', 'Height of the username field is not "37px"')

        # Wait for the username input field to be visible
        username_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'username'))
        )
        username_input.send_keys(SCORINGBOT_USERNAME)

        # Find and fill the password input field
        password_input = self.driver.find_element(By.NAME, 'password')
        password_input.send_keys(SCORINGBOT_PASSWORD)

        # Assert the submit button is colored #007bff;
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        self.assertEqual(submit_button.value_of_css_property('background-color'), 'rgba(0, 123, 255, 1)', 'Submit button is not colored #007bff')

        # Submit the form
        password_input.send_keys(Keys.RETURN)

        # Assert redirect to home page
        self.assertEqual(self.driver.current_url, f'{protocol}{PINGO_DOMAIN}/home')

        # Find the input field for entering hostname
        hostname_input = self.driver.find_element(By.NAME, 'hostname')
        hostname_input.send_keys(PING_HOSTNAME)

        # Assert the submit button is colored #007bff;
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        self.assertEqual(submit_button.value_of_css_property('background-color'), 'rgba(0, 123, 255, 1)', 'Submit button is not colored #007bff')

        # Submit the form to perform the ping
        submit_button.click()

        # Wait for the result to be displayed
        response = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'ping-response'))
        )

        # Assert the result contains "Loading..."
        self.assertIn("Loading...", response.text)

        # Wait for the result to be updated with the ping result
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_element(By.ID, 'ping-response').text != "Loading..."
        )

        # Assert that the result contains the ping response
        ping_response = response.text
        self.assertTrue(ping_response.startswith("PING "))

        # Click logout
        logout_button = self.driver.find_element(By.XPATH, "//form[@action='/logout']//button[@type='submit']")
        logout_button.click()

        # Assert redirect to login page
        self.assertEqual(self.driver.current_url, f'{protocol}{PINGO_DOMAIN}/')

    def test_http_website(self):
        self._test_website(protocol='http://')

    def test_https_website(self):
        self._test_website(protocol='https://')


if __name__ == '__main__':
    unittest.main()
