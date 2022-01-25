from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import os, os.path


class instag():
    def accept_cookies(self):
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'aOOlW')))
        accept_button = self.browser.find_element_by_class_name("aOOlW")
        accept_button.click()

    def login(self):
        self.wait.until(EC.visibility_of_element_located((By.NAME, 'username'))) 
        self.browser.find_element_by_name("username").send_keys(self.username)
        self.browser.find_element_by_name("password").send_keys(self.password)
        self.browser.find_element_by_class_name("Igw0E").click()  # login button
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_lz6s')))

    def get_text(self):
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'C4VMK')))
        description = self.browser.find_element_by_class_name("C4VMK")
        ret = (f"link: {self.browser.current_url}, text:{description.text}\n\n")
        webdriver.ActionChains(self.browser).send_keys(Keys.RIGHT).perform()
        return ret

    def main(self):  # todo: refactor this to small methods
        self.username = input("Please enter username:\n")
        self.password = getpass()  # todo: check if incorrect
        account_name = input("Please enter the account name:\n")
        file_location = input("Please enter the desired location for the file name (ie C:\\folder) \n")  # todo: consider different input cases

        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)

        link = "https://www.instagram.com/"
        self.browser.get(link)
        self.accept_cookies()
        self.login()
        self.browser.get(f"https://www.instagram.com/{account_name}/")

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'g47SY')))  # total posts counter
        amount_of_posts = int(self.browser.find_element_by_class_name("g47SY").get_attribute('text'))
        all_posts = self.browser.find_elements_by_class_name("v1Nh3")
        all_posts[0].click()  # click the first photo

        if not os.path.exists(file_location):
            os.mkdir(file_location)
        f = open(rf"{file_location}\\content.txt", "w+", encoding="utf-8")
        for i in range (0, amount_of_posts):
            f.write(self.get_text())
            print (f"{i} out of {amount_of_posts}")
        f.close()
        self.browser.quit()


if __name__ == '__main__':
    instag().main()
