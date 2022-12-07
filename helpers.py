from constants import *
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from random import randint
from time import sleep
from os import system


# Create a new instance of the Undetected Chrome driver as browser
def set_browser():
    chrome_options = uc.ChromeOptions()
    browser = uc.Chrome(options=chrome_options)
    return browser


# Get URLs to check
def get_urls(mode):
    urls = []
    with open('URLs.txt') as db:
        for line in db:
            if mode == 'mega' and line.startswith('https://mega.nz') or mode == 'panel' and \
                    line.startswith('http://technical') or mode == 'tiktok' and line.startswith('https://www.tiktok.c')\
                    or mode == 'raw' and line.startswith('https://pastebin.com/' or 'https://rentry.co/') or mode == \
                    'workers' and line.startswith('https://xmr.2miners.com/'):
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


# URLs check
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


def workers():
    urls = get_urls('workers')
    browser = set_browser()
    total = 'ERROR'
    last_24 = 'ERROR'
    last_share = 'ERROR'
    share_hour = 'ERROR'
    current = 'ERROR'
    average = 'ERROR'
    for url in urls:
        try:
            browser.get(url)
            total = browser.find_element(By.XPATH, TOTAL).text
            last_24 = browser.find_element(By.XPATH, LAST_24).text
            last_share = browser.find_element(By.XPATH, LAST_SHARE).text
            share_hour = browser.find_element(By.XPATH, SHARE_HOUR).text
            current = [browser.find_element(By.XPATH, CURRENT[0]).text.replace('\n', ' '),
                       browser.find_element(By.XPATH, CURRENT[1]).text]
            average = [browser.find_element(By.XPATH, CURRENT[0]).text.replace('\n', ' '),
                       browser.find_element(By.XPATH, AVERAGE[1]).text]

            browser.close()
            break

        except TimeoutException or NoSuchElementException:
            pass

    return total, last_share, share_hour, last_24, current, average
