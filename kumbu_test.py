from selenium import webdriver
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures('driver')
class TestKumbuFunctional:
    @pytest.fixture(scope='class')
    def driver(self):
        driver = webdriver.Chrome()
        yield driver
        driver.quit()

    def test_l001(self, driver):
        driver.get('https://staging.getkumbu.com')
        driver.find_element_by_name('inputEmail').send_keys('kumbutest@mailinator.com')
        driver.find_element_by_name('inputPassword').send_keys('$PASSWORD')
        driver.find_element_by_id('login-submit').click()

        links = driver.find_elements_by_class_name('profile-link')
        assert len(links) != 0 and 'Kumbu Test M2' in links[0].text
        links[0].click()

        '''Profile Panel is not implemented yet!'''

    def test_l002(self, driver):
        driver.get('https://staging.getkumbu.com')
        driver.find_element_by_name('inputEmail').send_keys('kumbutest@mailinator.com')
        driver.find_element_by_name('inputPassword').send_keys('kumbu ​is ​not ​cool')
        driver.find_element_by_id('login-submit').click()

        flashes = driver.find_elements_by_id('flash-messages')
        assert len(flashes) != 0 and 'Invalid email or password' in flashes[0].text
        flashes[0].find_element_by_class_name('close-button').click()

    def test_l003(self, driver):
        driver.get('https://staging.getkumbu.com')
        driver.find_element_by_class_name('password-link').click()
        assert 'https://staging.getkumbu.com/reset' in driver.current_url

        driver.find_element_by_name('inputEmail').send_keys('kumbutest@mailinator.com')
        driver.find_element_by_id('login-submit').click()

        flashes = driver.find_elements_by_id('flash-messages')
        assert len(flashes) != 0 and 'An email to reset your password has been sent' in flashes[0].text
        flashes[0].find_element_by_class_name('close-button').click()
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

        flashes = driver.find_elements_by_id('flash-messages')
        assert len(flashes) != 0 and 'Your password has been successfully changed' in flashes[0].text
        flashes[0].find_element_by_class_name('close-button').click()

        self.test_l001()

    def test_m001(self):
        self.test_l001()

        driver = webdriver.Chrome()
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

    def test_m002(self):
        self.test_l001()

        driver = webdriver.Chrome()
        driver.find_element_by_class_name('souvenirs-menu-link').click()
        driver.find_element_by_css_selector('ul.dropdown.menu > li').click()
        driver.find_element_by_class_name('sort-by-title').click()

        '''Not completed'''
