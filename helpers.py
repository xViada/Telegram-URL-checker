from constants import *
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from random import randint
from time import sleep
from os import stat


# Create a new instance of the Undetected Chrome driver as browser
def set_browser():
    chrome_options = uc.ChromeOptions()
    browser = uc.Chrome(options=chrome_options)

    return browser


# Get URLs to check
def get_urls(mode):
    urls = []
    with open('URLs.txt') as db:
        for url in db:
            if mode == 'mega' and url.startswith('https://mega.nz') or mode == 'panel' and \
                    url.startswith('http://technica') or mode == 'tiktok' and url.startswith('https://www.tiktok.c') \
                    or mode == 'raw' and url.startswith('https://pastebin.com/' or 'https://rentry.co/') or mode == \
                    'workers' and url.startswith('https://xmr.2miners.com/'):
                urls.append(url.rstrip())
    return urls


# Get the URLs status message for telegram
def urls_final_message():
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
                    print('{} {} NOT WORKING(not clickable): {}'.format(url_count, mode, url))
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


# Get the workers status message for telegram
def workers_final_message():
    urls = get_urls('workers')
    browser = set_browser()
    workers = '⚠️WORKERS WEB NOT AVAILABLE⚠️'
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
            workers = f'Total: {total}\n' \
                      f'Last 24h: {last_24}\n' \
                      f'Last share: {last_share} at {share_hour}\n' \
                      f'Current: {current[0]}\n' \
                      f'Average: {average[0]}'

        except Exception as e:
            print(e)

    return workers


def refresh_admin_ids():
    with open('config.txt') as config:
        for x in config:
            if x.startswith('admin-user-ids:'):
                a = x.strip('admin-user-ids:').split(', ')
                admin_ids = [eval(i) for i in a]

    return admin_ids


def refresh_snoopers_db():
    snoopers = []
    if stat('snoopers.txt').st_size == 0:
        snoopers.append('Not snoopers in database.')
    else:
        with open('snoopers.txt') as db:
            for snoop in db:
                snoopers.append(snoop)

    return snoopers
