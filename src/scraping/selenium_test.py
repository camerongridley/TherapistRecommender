from selenium import webdriver
import time
from random import randint
import pickle

def build_url(base_url, page_num):
    return base_url + suffix + str(page_num)

driver = webdriver.Firefox()

base_url = 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=new%20york,%20new%20york&search[lat]=40.7127753&search[lon]=-74.0059728'
sf = 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=san%20francisco,%20california&search[lat]=37.7749295&search[lon]=-122.4194155'
page_num = 1
suffix = '&search[p]='

full_url = build_url(base_url, page_num)
driver.get(full_url)

time.sleep(2)

last_page_num = 110#driver.find_element_by_xpath("//ul[@class='pagination hide-on-med-and-down']/li[last()]").text

links = []

def get_links_from_current_page(links:list)->list:
    elements = driver.find_elements_by_xpath("//ul[@class='therapist-list']/li/div/a")
    for element in elements:
        links.append(element.get_attribute('href'))

    return links

get_links_from_current_page(links)

for pg in range(2, int(last_page_num) + 1):
    new_url = build_url(base_url, pg)
    driver.get(new_url)
    t = randint(3,5)
    print(f'Sleep for {t} sec')
    time.sleep(t)
    get_links_from_current_page(links)

    pickle.dump(links, open( "nyc_links.pkl", "wb" ) )
    print(f'Saving Page: {pg}')
#print(links)

print(f'Last Page Num: {last_page_num}')

driver.close()

