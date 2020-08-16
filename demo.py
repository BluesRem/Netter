from selenium import webdriver


class Demo:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


with Demo() as driver:
    driver.get('https://www.baidu.com')
    driver.quit()
