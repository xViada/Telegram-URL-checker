import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from random import randint
from time import sleep
from os import system


# Create a new instance of the Chrome driver as browser
def set_browser():
    chrome_options = uc.ChromeOptions()
    browser = uc.Chrome(options=chrome_options)
    return browser


# Def URLs to check
def get_urls(mode):
    urls = []
    with open('URLs.txt') as db:
        for line in db:
            if mode == 'mega' and line.startswith('https://mega.nz/file/'):
                urls.append(line.rstrip())
            if mode == 'panel' and line.startswith('http://technical'):
                urls.append(line.rstrip())
            if mode == 'tiktok' and line.startswith('https://www.tiktok.com/'):
                urls.append(line.rstrip())
            if mode == 'raw' and line.startswith('https://pastebin.com/' or 'https://rentry.co/'):
                urls.append(line.rstrip())
    return urls


# Get Final Message
def final_message():
    system('cls')
    mega_data = check('mega', '/html/body/div[6]/div[2]/div[2]/section/div[1]/div/div[4]/div[3]/div[2]/div[1]/button')
    panel_data = check('panel', '/html/body/div[1]/div/div[2]/form/button')
    tiktok_data = check('tiktok', '//*[@id="app"]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/div/button')
    raw_data = check('raw', '/html/body/pre')

    return ('MEGA: {}/{} working.\n'
            'Url errors: {}\n'
            'PANEL: {}/{} working.\n'
            'Url errors: {}\n'
            'TIKTOK: {}/{} working.\n'
            'Url errors: {}\n'
            'RAW: {}/{} working.\n'
            'Url errors: {}\n'.format((mega_data[0] - mega_data[1]), mega_data[0], mega_data[2],
                                      (panel_data[0] - panel_data[1]), panel_data[0], panel_data[2],
                                      (tiktok_data[0] - tiktok_data[1]), tiktok_data[0], tiktok_data[2],
                                      (raw_data[0] - raw_data[1]), raw_data[0], raw_data[2]))


# URLs checks
def check(mode, xpath):
    urls = get_urls(mode)
    url_error = []
    url_error_count = 0
    browser = set_browser()
    url_count = 0

    for url in urls:
        browser.get(url)
        if mode == 'mega':
            sleep(randint(20, 25))
        else:
            sleep(randint(4, 7))

        try:
            b = browser.find_element(By.XPATH, xpath)
            if mode == 'mega':
                if b.is_enabled():
                    url_count += 1
                    print('{} {} still working:{}'.format(url_count, mode, url))
                else:
                    url_count += 1
                    url_error_count += 1
                    print('{} MEGA NOT WORKING(not clickable): {}'.format(url_count, url))
                    url_error.append(url)
            else:
                url_count += 1
                print('{} still working...'.format(url, url_count))
        except NoSuchElementException:
            url_count += 1
            url_error_count += 1
            url_error.append(url)
            print('{} NOT WORKING (not available)'.format(url, url_count))

    print('Total errors in {} URLs: {}/{}'.format(mode, url_error_count, url_count))
    browser.close()

    return [url_count, url_error_count, url_error]
