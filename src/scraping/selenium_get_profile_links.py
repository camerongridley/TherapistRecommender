from selenium import webdriver
import time
from random import randint
import pickle

driver = webdriver.Firefox()

cities = {
    #'la' : ['74', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=los%20angeles,%20california&search[lat]=34.0522342&search[lon]=-118.2436849'],
    'chicago' : ['39', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=chicago,%20illinois&search[lat]=41.8781136&search[lon]=-87.6297982'],
    'houston' : ['11', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=houston,%20texas&search[lat]=29.7604267&search[lon]=-95.3698028'],
    'phoenix' : ['12', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=phoenix,%20arizona&search[lat]=33.4483771&search[lon]=-112.0740373'],
    'philadelphia' : ['98', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=philadelphia,%20pennsylvania&search[lat]=39.9525839&search[lon]=-75.1652215'],
    'san_antonio' : ['14', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=san%20antonio,%20texas&search[lat]=29.4241219&search[lon]=-98.49362819999999'],
    'san_diego' : ['32', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=san%20diego,%20california&search[lat]=32.715738&search[lon]=-117.1610838'],
    'dallas' : ['18', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=dallas,%20texas&search[lat]=32.7766642&search[lon]=-96.79698789999999'],
    'san_jose' : ['54', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=san%20jose,%20california&search[lat]=37.3382082&search[lon]=-121.8863286'],
    'austin' : ['14', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=austin,%20texas&search[lat]=30.267153&search[lon]=-97.7430608'],
    'jacksonville' : ['3', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=jacksonville,%20florida&search[lat]=30.3321838&search[lon]=-81.65565099999999'],
    'forth_worth' : ['18', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=fort%20worth,%20texas&search[lat]=32.7554883&search[lon]=-97.3307658'],
    'columbus' : ['7', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=columbus,%20ohio&search[lat]=39.9611755&search[lon]=-82.99879419999999'],
    'charlotte' : ['10', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=charlotte,%20north%20carolina&search[lat]=35.2270869&search[lon]=-80.8431267'],
    'indianapolis' : ['4', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=indianapolis,%20indiana&search[lat]=39.768403&search[lon]=-86.158068'],
    'seattle' : ['28', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=seattle,%20washington&search[lat]=47.6062095&search[lon]=-122.3320708'],
    'washington_dc' : ['37', 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=washington,%20district%20of%20columbia&search[lat]=38.9071923&search[lon]=-77.0368707'],
}

def build_url(base_url, page_num):
    return base_url + suffix + str(page_num)

def get_links_from_current_page(links:list)->list:
    elements = driver.find_elements_by_xpath("//ul[@class='therapist-list']/li/div/a")
    for element in elements:
        links.append(element.get_attribute('href'))

    return links

for city_name, search_result in cities.items():
    #last_page_num = 110#driver.find_element_by_xpath("//ul[@class='pagination hide-on-med-and-down']/li[last()]").text
    #base_url = 'https://www.goodtherapy.org/search2.html?search[miles]=100&search[zipcode]=new%20york,%20new%20york&search[lat]=40.7127753&search[lon]=-74.0059728'
    last_page_num = search_result[0]
    base_url = search_result[1]

    page_num = 1
    suffix = '&search[p]='

    full_url = build_url(base_url, page_num)
    driver.get(full_url)

    time.sleep(10)

    links = []
    # get links for first page
    get_links_from_current_page(links)

    # get links for pages 2 - last page
    for pg in range(2, int(last_page_num) + 1):
        new_url = build_url(base_url, pg)
        driver.get(new_url)
        t = randint(3,5)
        print(f'Sleep for {t} sec')
        time.sleep(t)
        get_links_from_current_page(links)

        pickle.dump(links, open( f'data/profile_links/{city_name}_in_progress.pkl', 'wb' ) )
        print(f'Saving Page: {pg}')

    pickle.dump(links, open( f'data/profile_links/cities_final/{city_name}_final.pkl', 'wb' ) )

    print(f'Last Page Num: {last_page_num}')

driver.close()




