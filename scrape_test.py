'''
PsychToday
- Treatment Approaches


- Important HTML tags
profile-address
    -class="address address-rank-1"

test page
https://www.psychologytoday.com/us/therapists/80205/484085?sid=5ea74d42a072a&ref=8&tr=ResultsName
'''
from bs4 import BeautifulSoup
import requests

def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup.prettify()
    return soup

def clean_string(string):
    cleaned = string
    cleaned = cleaned.replace('/','')
    cleaned = cleaned.replace('/n','')
    cleaned = cleaned.replace('\r','')
    
    return cleaned

def get_good_tx_text(soup):
    desc = soup.find_all('div', class_='profileBottomLeft')
    all_text = desc[0].find_all('div', class_='text')
    good_stuff = []
    for txt in all_text:
        for child in txt.children:
            if(child.name == 'p'):
                good_stuff.append(child.get_text())

    good_stuff_st = ''.join(good_stuff)
    return good_stuff_st

def get_good_tx_issues(soup)-> list:
    issues_html = soup.find_all('ul', id='issuesData')
    issues_list = list(issues_html[0].children)
    
    ##if want to return string instead
    # issues_str = issues_html[0].get_text()
    # clean_str = clean_string(issues_str)
    
    return issues_list

if __name__ == '__main__':
    therapists = ['https://www.goodtherapy.org/therapists/profile/andrea-risi-20130730']
    soup = get_soup(url = 'https://www.goodtherapy.org/therapists/profile/andrea-risi-20130730')
    issues = get_good_tx_issues(soup)
    description = get_good_tx_text(soup)

    print(issues)
    print(description)