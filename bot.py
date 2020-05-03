import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import login_info


class TinderBot:
    def __init__(self, mode):
        self.driver = webdriver.Chrome()
        self.driver.get("https://tinder.com")
        self.driver.implicitly_wait(10)
        self.mode = mode

    def login(self):
        sleep(5)

        # Find only first css element with "Log in with Facebook"
        try:
            login_btn = self.driver.find_element_by_css_selector("[aria-label='Log in with Facebook']")
            login_method = "facebook"
        except selenium.common.exceptions.NoSuchElementException:
            login_btn = self.driver.find_element_by_css_selector("[aria-label='Log in with Google']")
            login_method = "google"
        login_btn.click()

        # Save base window layer
        base_window = self.driver.window_handles[0]

        # Switch to front popup window layer
        sleep(5)
        pop_up = self.driver.switch_to.window(self.driver.window_handles[1])

        if login_method == "facebook":
            fb_email = self.driver.find_element_by_id('email')
            fb_email.send_keys(login_info.fb_email)
            fb_password = self.driver.find_element_by_id('pass')
            fb_password.send_keys(login_info.fb_password)
            pop_up_login = self.driver.find_element_by_id('loginbutton')
            pop_up_login.click()

            # Switch back to base layer
            self.driver.switch_to.window(base_window)

        else:
            google_email = self.driver.find_element_by_css_selector("input[type='email']")
            google_email.send_keys(login_info.google_email)
            next_btn = self.driver.find_element_by_id('identifierNext')
            next_btn.click()
            sleep(2)
            google_password = self.driver.find_element_by_name("password")
            google_password.send_keys(login_info.google_password)
            next_btn2 = self.driver.find_element_by_id("passwordNext").click()
            next_btn2.click()

        # Handling Tinder main page popups
        allow_location = self.driver.find_element_by_css_selector("[aria-label='Allow']")
        allow_location.click()
        no_notifs = self.driver.find_element_by_css_selector("[aria-label='Not interested']")
        no_notifs.click()
        accept_cookies = self.driver.find_element(By.XPATH, "//button[.//span[contains(text(), 'I Accept')]]")
        accept_cookies.click()
        no_location = self.driver.find_element(By.XPATH, "//button[.//span[contains(text(),'No Thanks')]]")
        no_location.click()

    def like(self):
        like_btn = self.driver.find_element_by_css_selector("[aria-label='Like']")
        like_btn.click()

    def dislike(self):
        dislike_btn = self.driver.find_element_by_css_selector("[aria-label='Nope']")
        dislike_btn.click()

    # def message(self)

    def keep_swiping(self):
        continue_btn = self.driver.find_element(By.XPATH, "//a[contains(text(),'Keep Swiping')]")
        continue_btn.click()

    def close_popup(self):
        not_interested_btn = self.driver.find_element(By.XPATH, "//button[.//span[contains(text(),'Not interested')]]")
        not_interested_btn.click()

    def auto_swipe(self):
        # Eventually implement AI to detect facial features, preferences, and send auto-generated messages
        while True:
            sleep(1)
            try:
                self.like()
            except Exception:
                try:
                    if self.mode == "swipeOnly":
                        self.keep_swiping()
                except Exception:
                    self.close_popup()


if __name__ == "__main__":
    bot = TinderBot("swipeOnly")
    bot.login()
    bot.auto_swipe()
