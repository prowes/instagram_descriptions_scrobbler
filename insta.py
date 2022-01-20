from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from getpass import getpass

class instag():
    def wait_until_element_visible(self, element):
        i = 0
        while i < 30:
            return self.wait_until_element_visible(element, i)
        print ("The element is not visible in 30secs, check locator or your Internet connection")
        exit()

    def check_if_element_is_shown(self, element, i)
        try:
            if element.is_displayed():
                return True
        except:
            print(f"{element} is not visible, attempt #{i}, wait a second and check again...")
            sleep(1)
            i =+ 1
            self.check_if_element_is_shown(element)

    def accept_cookies(self):
        accept_button = self.browser.find_element_by_class_name("aOOlW")
        self.wait_until_element_visible(accept_button)
        accept_button.click()

    def login(self):
        self.browser.find_element_by_name("username").send_keys(self.username)
        self.browser.find_element_by_name("password").send_keys(self.password)
        self.browser.find_element_by_class_name("Igw0E").click()  # login button
        profile_photo = self.browser.find_element_by_class_name("_2dbep qNELH")
        self.wait_until_element_visible(profile_photo)

    def get_text(self):
        description = self.browser.find_element_by_class_name("C4VMK")
        self.wait_until_element_visible(description)
        ret = (f"link: {self.browser.current_url}, text:{description.text}\n\n")
        webdriver.ActionChains(self.browser).send_keys(Keys.RIGHT).perform()
        return ret

    def main(self):  # todo: refactor this to small methods
        self.username = input("Please enter username:\n")
        self.password = getpass()

        self.browser = webdriver.Chrome()
        link = "https://www.instagram.com/"
        self.browser.get(link)
        self.accept_cookies()
        self.login()
        account_name = input("Please enter the account link:\n")
        self.browser.get(f"https://www.instagram.com/{account_name}/")
        file_location = input("Please enter the desired location for the file name (ie C:\texts) \n")  # todo: consider different cases

        # #amount_of_posts = int(self.browser.find_element_by_class_name("g47SY").get_attribute('text'))
        amount_of_posts = 10
        all_posts = self.browser.find_elements_by_class_name("v1Nh3")
        all_posts[0].click()  # click the first photo
        f = open(rf"{file_location}\\street.txt", "a+")
        for i in range (0, amount_of_posts):
            f.write(self.get_text())
            print (f"{i} out of {amount_of_posts}")
        f.close()
        self.browser.quit()

if __name__ == '__main__':
    instag().main()
