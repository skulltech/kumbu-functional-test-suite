from selenium import webdriver
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

passing = pytest.mark.skip(reason="No need to run the cases that are known to be correct in development.")


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

    @staticmethod
    def sign_in(driver):
        driver.get('https://staging.getkumbu.com')
        driver.find_element_by_name('inputEmail').send_keys('kumbutest@mailinator.com')
        driver.find_element_by_name('inputPassword').send_keys('$PASSWORD')
        driver.find_element_by_id('login-submit').click()

    @passing
    def test_l001(self, driver):
        self.sign_in(driver)

        links = driver.find_elements_by_class_name('profile-link')
        assert len(links) != 0 and 'Kumbu Test M2' in links[0].text
        links[0].click()

        # Asserting that the element is found.
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-modal')))

        driver.find_element_by_class_name('profile-tab-signout').click()
        assert 'https://staging.getkumbu.com/login' in driver.current_url

    @passing
    def test_l002(self, driver):
        driver.get('https://staging.getkumbu.com')
        driver.find_element_by_name('inputEmail').send_keys('kumbutest@mailinator.com')
        driver.find_element_by_name('inputPassword').send_keys('kumbu ​is ​not ​cool')
        driver.find_element_by_id('login-submit').click()
        self.verify_flash_message(driver, 'Invalid email or password')

    @passing
    def test_l003(self, driver):
        driver.get('https://staging.getkumbu.com')
        driver.find_element_by_class_name('password-link').click()
        assert 'https://staging.getkumbu.com/reset' in driver.current_url

        driver.find_element_by_name('inputEmail').send_keys('kumbutest@mailinator.com')
        driver.find_element_by_id('login-submit').click()
        self.verify_flash_message(driver, 'An email to reset your password has been sent')
        time.sleep(5)

        driver.get('https://www.mailinator.com/v2/inbox.jsp?zone=public&query=kumbutest#')
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Reset your Kumbu password")]')))
        element.click()

        frame = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'msg_body')))
        driver.switch_to.frame(frame)
        button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'mcnButton')))
        button.click()

        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'inputPassword')))
        driver.find_element_by_name('inputPassword').send_keys('$PASSWORD')
        driver.find_element_by_name('confirmPassword').send_keys('$PASSWORD')
        driver.find_element_by_id('login-submit').click()

        self.verify_flash_message(driver, 'Your password has been successfully changed')
        self.test_l001(driver)

    @passing
    def test_c001(self, driver):
        self.sign_in(driver)

        driver.find_element_by_css_selector('div.secondary-navigation > div > div > ul > li > a').click()
        title = driver.find_element_by_id('collection-title')
        title.click()
        title.send_keys(Keys.CONTROL + 'a')
        title.send_keys('Collection ​for ​Test ​TEST_NUMBER')
        title.send_keys(Keys.ENTER)
        assert '0' in driver.find_element_by_class_name('collection-item-number').text
        driver.find_element_by_class_name('back-collections').click()
        assert 'Collection for Test TEST_NUMBER' in driver.find_element_by_css_selector('div.collection.columns').text

    @passing
    def test_m001(self, driver):
        self.sign_in(driver)

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
        self.sign_in(driver)

        driver.find_element_by_class_name('souvenirs-menu-link').click()
        items = [link.get_attribute('data-kumbu-item-id') for link in driver.find_elements_by_css_selector('div.item.columns > a')]
        elem = driver.find_element_by_css_selector('ul.dropdown.menu > li')
        hover = ActionChains(driver).move_to_element(elem)
        sort = driver.find_element_by_class_name('sort-by-title')
        hover.perform()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'sort-by-title')))
        sort.click()
        time.sleep(5)
        sorted_items = [link.get_attribute('data-kumbu-item-id') for link in driver.find_elements_by_css_selector('div.item.columns > a')]
        smaller = len(min(items, sorted_items))
        assert items[:smaller] != sorted_items[:smaller]
