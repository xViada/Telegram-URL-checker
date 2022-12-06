from constants import *
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
    mega_data = check('mega', MEGA_XPATH)
    panel_data = check('panel', PANEL_XPATH)
    tiktok_data = check('tiktok', TIKTOK_XPATH)
    raw_data = check('raw', RAW_XPATH)

    return (f'MEGA: {(mega_data[COUNT_POS] - mega_data[ERROR_COUNT_POS])}/{mega_data[COUNT_POS]} working.\n'
            f'Url errors: {mega_data[ERRORS_POS]}\n'
            f'PANEL: {(panel_data[COUNT_POS] - panel_data[ERROR_COUNT_POS])}/{panel_data[COUNT_POS]} working.\n' 
            f'Url errors: {panel_data[ERRORS_POS]}\n'
            f'TIKTOK: {(tiktok_data[COUNT_POS] - tiktok_data[ERROR_COUNT_POS])}/{tiktok_data[COUNT_POS]} working.\n' 
            f'Url errors: {tiktok_data[ERRORS_POS]}\n'
            f'RAW: {(raw_data[COUNT_POS] - raw_data[ERROR_COUNT_POS])}/{raw_data[COUNT_POS]} working.\n'
            f'Url errors: {raw_data[ERRORS_POS]}\n')


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
