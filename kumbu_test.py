from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC


def test_l001():
    driver = webdriver.Chrome()

    driver.get('https://staging.getkumbu.com')
    driver.find_element_by_name('inputEmail').send_keys('kumbutest@mailinator.com')
    driver.find_element_by_name('inputPassword').send_keys('$PASSWORD')
    driver.find_element_by_id('login-submit').click()

    # Assertion part to be done.


def test_l002():
    driver = webdriver.Chrome()

    driver.get('https://staging.getkumbu.com')
    driver.find_element_by_name('inputEmail').send_keys('kumbutest@mailinator.com')
    driver.find_element_by_name('inputPassword').send_keys('kumbu ​is ​not ​cool')
    driver.find_element_by_id('login-submit').click()
    flashes = driver.find_elements_by_id('flash-messages')

    assert len(flashes) != 0 and flashes[0].text.strip() == 'Invalid email or password'
    flashes[0].find_element_by_class_name('close-button').click()
