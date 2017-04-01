from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
import unittest
import logging

class ResultPage(object):
    def __init__(self,driver):
        self.driver = driver

    def first_link(self):        
        return self.driver.find_element_by_xpath("//a[@id='am-b2']/parent::div/preceding-sibling::cite[@class='_Rm']").text

    def first_image(self):
        element = self.driver.find_element(By.XPATH, '//div[@id="ires"]//div[@data-ri="0"]//span')
        return self.driver.execute_script("return arguments[0].textContent;", element)
        
    def title_return(self):
        return self.driver.title

class HomePage(object):
    def __init__(self,driver):
        self.driver = driver

    def search(self, param):
        self.driver.find_element_by_xpath("//input[@name='q']").clear()
        self.driver.find_element_by_xpath("//input[@name='q']").send_keys(param)
        return ResultPage(self.driver) 

    def go_to_images(self):
        self.driver.find_element_by_xpath("//a[@class='q qs'][text()='Image' or text()='Картинки']").click()
        return ResultPage(self.driver)
        
    def go_to_all(self):
        self.driver.find_element_by_xpath("//a[@class='q qs'][text()='All' or text()='Все']").click()
        return ResultPage(self.driver)
        
class BaseTestCase(unittest.TestCase):
    
    def setUp(self):
        logger.info(self.id() + '--START TEST--')
        logger.info('Заходим на google.com')
        self.driver = webdriver.Chrome()
        self.driver.get("http://google.com")
        self.driver.implicitly_wait(10)
        self.assertIn("Google", self.driver.title)

    def tearDown(self):
        logger.info(self.id() + '--Finish TEST--')
        self.driver.close()

class GoogleTesting(BaseTestCase):

    def testAutoTest(self):
        logger.info('Выполняем поиск по слову "selenium"')
        page = HomePage(self.driver)
        result = page.search("selenium\n")
        assert "www.seleniumhq.org/" in result.first_link()

        logger.info('Переходим на вкладку "Images" или "Картинки"')
        result = page.go_to_images()
        result2 = result.first_image()
        self.assertIn("seleniumhq.org", result2)
        
        logger.info("Вернуться на вкладку 'All' или 'Все'")
        result = page.go_to_all()
        assert "www.seleniumhq.org/" in result.first_link()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    filehandler = logging.FileHandler('Tect_logger.log')
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    logger.addHandler(console)
    logger.addHandler(filehandler)
    unittest.main()
