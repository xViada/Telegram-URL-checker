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
            if mode == mega and line.startswith('https://mega.nz/file/'):
                urls.append(line.rstrip())
            if mode == panel and 'technical' in line:
                urls.append(line.rstrip())
            if mode == tiktok and line.startswith('https://www.tiktok.com/'):
                urls.append(line.rstrip())
            if mode == raw and line.startswith('https://pastebin.com/' or 'https://rentry.co/'):
                urls.append(line.rstrip())
    return urls


# Get Final Message
def final_message():
    system('cls')
    mega_data = mega()
    panel_data = panel()
    tiktok_data = tiktok()
    raw_data = raw()

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
def mega():
    urls = get_urls(mega)
    url_error_count = 0
    url_error = []
    browser = set_browser()
    url_count = 0

    for url in urls:
        browser.get(url)
        sleep(randint(15, 25))
        try:
            button = browser.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[2]/section/div[1]/div/div[4]/div['
                                                    '3]/div[2]/div[1]/button')
            if button.is_enabled():
                url_count += 1
                print('{} MEGA still working:{}'.format(url_count, url))
            else:
                url_count += 1
                url_error_count += 1
                print('{} MEGA NOT WORKING(not clickable): {}'.format(url_count, url))
                url_error.append(url)
        except NoSuchElementException:
            url_count += 1
            url_error_count += 1
            print('{} MEGA NOT WORKING(not available): {}'.format(url_count, url))
            url_error.append(url)

    print('Total errors in MEGA URLs: {}/{}'.format(url_error_count, url_count))

    browser.close()

    return [url_count, url_error_count, url_error]


def panel():
    urls = get_urls(panel)
    url_error = []
    url_error_count = 0
    browser = set_browser()
    url_count = 0

    for url in urls:
        browser.get(url)
        sleep(randint(5, 10))
        try:
            browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/form/button')
            url_count += 1
            print('{} still working...'.format(url, url_count))
        except NoSuchElementException:
            url_count += 1
            url_error_count += 1
            url_error.append(url)
            print('{} NOT WORKING (not available)'.format(url, url_count))

    print('Total errors in PANEL URLs: {}/{}'.format(url_error_count, url_count))
    browser.close()

    return [url_count, url_error_count, url_error]


def tiktok():
    urls = get_urls(tiktok)
    url_error = []
    url_error_count = 0
    browser = set_browser()
    url_count = 0

    for url in urls:
        browser.get(url)
        sleep(randint(1, 3))
        try:
            browser.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div/div/button')
            url_count += 1
            print('{} still working...'.format(url, url_count))
        except NoSuchElementException:
            url_count += 1
            url_error_count += 1
            url_error.append(url)
            print('{} NOT WORKING (not available)'.format(url, url_count))

    print('Total errors in TikTok URLs: {}/{}'.format(url_error_count, url_count))
    browser.close()

    return [url_count, url_error_count, url_error]


def raw():
    urls = get_urls(raw)
    url_error = []
    url_error_count = 0
    browser = set_browser()
    url_count = 0

    for url in urls:
        browser.get(url)
        sleep(randint(1, 3))
        try:
            browser.find_element(By.XPATH, '/html/body/pre')
            url_count += 1
            print('{} still working...'.format(url, url_count))
        except NoSuchElementException:
            url_count += 1
            url_error_count += 1
            url_error.append(url)
            print('{} NOT WORKING (not available)'.format(url, url_count))

    print('Total errors in RAW URLs: {}/{}'.format(url_error_count, url_count))
    browser.close()

    return [url_count, url_error_count, url_error]