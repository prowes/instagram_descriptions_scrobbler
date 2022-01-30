from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
        self.check_if_wrong_credentials()
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_lz6s')))

    def check_if_wrong_credentials(self):
        try:
            notification_shown = self.wait_short.until(EC.visibility_of_element_located((By.ID, 'slfErrorAlert')))
            print("Your credentials are incorrect, please check and try again")
            quit()
        except TimeoutException:  # no error is shown
            pass

    def get_text(self):
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'C4VMK')))
        description = self.browser.find_element_by_class_name("C4VMK")
        ret = (f"link: {self.browser.current_url}, text:{description.text}\n\n")
        webdriver.ActionChains(self.browser).send_keys(Keys.RIGHT).perform()
        return ret

    def create_folder_and_file(self, file_location, amount_of_posts):
        if not os.path.exists(file_location):
            os.mkdir(file_location)
        f = open(rf"{file_location}\\content.txt", "w+", encoding="utf-8")
        for i in range (0, amount_of_posts):
            f.write(self.get_text())
            print (f"{i} out of {amount_of_posts}")
        f.close()

    def main(self):
        self.username = input("Please enter username:\n")
        self.password = getpass()
        account_name = input("Please enter the account name:\n")
        file_location = input("Please enter the desired location for the file name (ie C:\\folder) \n")
        if self.username == "" or self.password == "" or account_name == "" or file_location == "":
            print("Please check values and try again, something is empty")
            exit()
        if ":\\" not in file_location:
            print("Incorrect file location entered")
            exit()

        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.wait_short = WebDriverWait(self.browser, 5)

        link = "https://www.instagram.com/"
        self.browser.get(link)
        self.accept_cookies()
        self.login()
        self.browser.get(f"https://www.instagram.com/{account_name}/")

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'g47SY')))  # total posts counter
        amount_of_posts = int(self.browser.find_element_by_class_name("g47SY").text)
        all_posts = self.browser.find_elements_by_class_name("v1Nh3")
        all_posts[0].click()  # click the first photo

        self.create_folder_and_file(file_location, amount_of_posts)
        self.browser.quit()

if __name__ == '__main__':
    instag().main()
