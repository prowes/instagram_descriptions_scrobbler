from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from getpass import getpass
import os, os.path


class Instag():
    def accept_cookies(self):
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, self.locators['accept_cookies'])))
        accept_button = self.browser.find_element_by_class_name(self.locators['accept_cookies'])
        accept_button.click()

    def login(self):
        self.wait.until(EC.visibility_of_element_located((By.NAME, 'username'))) 
        self.browser.find_element_by_name('username').send_keys(self.username)
        self.browser.find_element_by_name('password').send_keys(self.password)

        webdriver.ActionChains(self.browser).send_keys(Keys.ENTER).perform()
        self.check_if_wrong_credentials()
        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, self.locators['header'])))

    def check_if_wrong_credentials(self):
        try:
            notification_shown = self.wait_short.until(EC.visibility_of_element_located((By.ID, self.locators['wrong_credentials_notification'])))
            print('Your credentials are incorrect, please check and try again')
            exit()
        except TimeoutException:  # no error is shown
            pass

    def get_text(self, i):
        try:
            self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, self.locators['post_description'])))
            description = self.browser.find_element_by_class_name(self.locators['post_description'])
            print(type(description.text))
            description_text = str.join(" ", description.text.splitlines())
            print(description_text)
        except:
            description_text = ''
            print('the description is empty')
        ret = (f'{i},{self.browser.current_url},{description_text}\n')
        return ret

    def go_to_the_next_post(self):
        webdriver.ActionChains(self.browser).send_keys(Keys.RIGHT).perform()

    def create_folder_and_file(self, amount_of_posts):
        if not os.path.exists(self.file_location):
            os.mkdir(self.file_location)
        f = open(rf'{self.file_location}\\content.csv', 'w+', encoding='utf-16')
        f.write('Number,URL,post description\n')
        for i in range (0, amount_of_posts):
            f.write(self.get_text(i))
            self.go_to_the_next_post()
            print (f'{i} out of {amount_of_posts}')
        f.close()

    def ask_arguments(self):
        self.username = input('Please enter username:\n')
        self.password = getpass()
        if len(self.password) < 6:
            print('Password seems to be incorrect, it should have at least 6 symbols, try again')
            exit()
        self.account_name = input('Please enter the account name:\n')
        self.file_location = input('Please enter the desired location for the file name (ie C:\\folder) \n')
        if self.username == '' or self.password == '' or self.account_name == '' or self.file_location == '':
            print('Please check values and try again, something is empty')
            exit()
        if ':\\' not in self.file_location:
            print('Incorrect file location entered')
            exit()

    def main(self):
        self.ask_arguments()

        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)
        self.wait_short = WebDriverWait(self.browser, 5)
        self.locators = {
                        'accept_cookies': 'aOOlW',
                        'header': '_lz6s',
                        'wrong_credentials_notification': 'slfErrorAlert',
                        'post_description': 'C4VMK',
                        'posts_counter': 'g47SY',
                        'all_posts': 'v1Nh3'
                        }
        link = 'https://www.instagram.com/'
        self.browser.get(link)
        self.accept_cookies()
        self.login()
        self.browser.get(f'https://www.instagram.com/{self.account_name}/')

        self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, self.locators['posts_counter'])))
        amount_of_posts = int(self.browser.find_element_by_class_name(self.locators['posts_counter']).text)
        all_posts = self.browser.find_elements_by_class_name(self.locators['all_posts'])
        all_posts[0].click()  # click the first photo

        self.create_folder_and_file(amount_of_posts)
        self.browser.quit()

if __name__ == '__main__':
    Instag().main()
