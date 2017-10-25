from selenium import webdriver
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestKumbuFunctional:
    @pytest.fixture(scope='class')
    def webdriver(self):
        driver = webdriver.Firefox()
        yield driver
        driver.quit()

    @pytest.fixture(scope='function')
    def driver(self, webdriver):
        yield webdriver
        webdriver.delete_all_cookies()
        webdriver.get('https://www.google.com')

    @staticmethod
    def verify_flash_message(driver, message):
        flashes = driver.find_elements_by_id('flash-messages')
        assert len(flashes) != 0 and message in flashes[0].text
        flashes[0].find_element_by_class_name('close-button').click()

    def test_l001(self, driver):
        driver.get('https://staging.getkumbu.com')
        driver.find_element_by_name('inputEmail').send_keys('kumbutest@mailinator.com')
        driver.find_element_by_name('inputPassword').send_keys('$PASSWORD')
        driver.find_element_by_id('login-submit').click()

        links = driver.find_elements_by_class_name('profile-link')
        assert len(links) != 0 and 'Kumbu Test M2' in links[0].text
        links[0].click()

        assert len(driver.find_elements_by_class_name('profile-modal')) != 0
        driver.find_element_by_class_name('profile-tab-signout').click()
        assert 'https://staging.getkumbu.com/login' in driver.current_url

    def test_l002(self, driver):
        driver.get('https://staging.getkumbu.com')
        driver.find_element_by_name('inputEmail').send_keys('kumbutest@mailinator.com')
        driver.find_element_by_name('inputPassword').send_keys('kumbu ​is ​not ​cool')
        driver.find_element_by_id('login-submit').click()
        self.verify_flash_message(driver, 'Invalid email or password')

    def test_l003(self, driver):
        driver.get('https://staging.getkumbu.com')
        driver.find_element_by_class_name('password-link').click()
        assert 'https://staging.getkumbu.com/reset' in driver.current_url

        driver.find_element_by_name('inputEmail').send_keys('kumbutest@mailinator.com')
        driver.find_element_by_id('login-submit').click()
        self.verify_flash_message(driver, 'An email to reset your password has been sent')
        time.sleep(5)

        driver.get('https://www.mailinator.com/v2/inbox.jsp?zone=public&query=kumbutest#')
        driver.find_element_by_xpath('//div[contains(text(), "Reset your Kumbu password")]').click()

        frame = driver.find_element_by_id('msg-body')
        driver.switch_to.frame(frame)
        driver.find_element_by_class_name('mcnButton').click()

        driver.switch_to.window(driver.window_handles[1])
        driver.find_element_by_id('inputPassword').send_keys('$PASSWORD')
        driver.find_element_by_id('confirmPassword').send_keys('$PASSWORD')
        driver.find_element_by_id('login-submit').click()

        self.verify_flash_message(driver, 'Your password has been successfully changed')
        self.test_l001(driver)

    def test_m001(self, driver):
        self.test_l001(driver)

        driver.find_element_by_class_name('souvenirs-menu-link').click()

        prior = 0
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            current = len(WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.item.columns'))))

            if current != prior:
                prior = current
            else:
                break

        count = current

    def test_m002(self, driver):
        self.test_l001(driver)

        driver.find_element_by_class_name('souvenirs-menu-link').click()
        driver.find_element_by_css_selector('ul.dropdown.menu > li').click()
        driver.find_element_by_class_name('sort-by-title').click()

        '''Not completed'''
