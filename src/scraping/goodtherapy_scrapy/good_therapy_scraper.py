from bs4 import BeautifulSoup
import requests

def dec_check_none(func):
        def func_wrapper(*args, **kwargs):
            try:
                val = func(*args, **kwargs)
                return val
            except Exception as e:
                if isinstance(e, AttributeError):
                    return None
        return func_wrapper

class GoodTherapySoupScraper(object):
    

    def __init__(self, starting_url:str, is_local_file:bool):
        self.starting_url = starting_url
        self.is_local_file = is_local_file
        self.escape_chars = ['/','\n','/n','\r', '\t']

    def get_soup(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML,\
         like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
        if self.is_local_file:
            soup = BeautifulSoup(open(self.starting_url), "html.parser")
        else:
            page = requests.get(self.starting_url, headers=headers)
            soup = BeautifulSoup(page.content, 'html.parser')

        soup.prettify()
        return soup

    def clean_string(self, string: str) -> str:
        string = self.clean_escapes(string)
        #string = clean_punctuation(string)
        
        return string.strip()

    def clean_escapes(self, string: str):
        for esc in self.escape_chars:
            string = string.replace(esc,'')
            #string = string.replace('/n','')
            #string = string.replace('\n','')
            #string = string.replace('\r','')

        return string

    def clean_punctuation(self, string: str, keep_emo_punc=False) -> str:
        string = string.replace('&amp;', '&')

    def convert_html_list(self, li: list):
        clean_li = []
        for elem in li:
            if elem not in self.escape_chars:
                try:
                    string = ''
                    if isinstance(elem, str):
                        string = elem.strip()
                    else:
                        string = elem.text.strip()
                    
                    #check if empty
                    if string:
                        clean_li.append(string)
                except Exception as e:
                    print(f'Error caught: {e}')
                    continue
                
        return clean_li
        #return [tag.text for tag in li if type(tag) == 'li']
        
    def get_all_data(self, soup: BeautifulSoup) -> dict:
        all_data = {}
        full_name_ls = self.get_name(soup).split()
        first_name = full_name_ls[0]
        last_name = full_name_ls[-1]
        all_data['full_name'] = self.get_name(soup)
        all_data['first_name'] = first_name
        all_data['last_name'] = last_name
        all_data['street'] = self.sub_get_street(soup)
        all_data['city'] = self.sub_get_city(soup)
        all_data['state'] = self.sub_get_state(soup)
        all_data['zip_code'] = self.sub_get_zip(soup)
        all_data['phone'] = self.get_phone(soup)
        all_data['primary_credential'] = self.get_primary_credential(soup)
        all_data['license_status'] = self.get_license_status(soup)
        all_data['website'] = self.get_website(soup)
        all_data['info_source'] = 'goodtherapy'
        all_data['verified'] = self.get_verification(soup)
        all_data['age_group_list'] = self.get_client_ages(soup)
        all_data['issues_list'] = self.get_tx_issues(soup)
        all_data['orientations_list'] = self.get_orientations(soup)
        all_data['professions_list'] = self.get_professions(soup)
        all_data['services_list'] = self.get_services(soup)
        all_data['writing_sample'] = self.get_writing_sample(soup)
        
        return all_data

    @dec_check_none
    def get_name(self, soup: BeautifulSoup) -> str:
        name = soup.find('h1', id='profileTitle_id').contents[1].get_text()
        return self.clean_escapes(name)

    @dec_check_none
    def get_writing_sample(self, soup: BeautifulSoup) -> str:
        desc = soup.find_all('div', class_='profileBottomLeft')
        all_text = desc[0].find_all('div', class_='text')
        good_stuff = []
        for txt in all_text:
            for child in txt.children:
                if(child.name == 'p'):
                    good_stuff.append(child.get_text())

        good_stuff_st = ''.join(good_stuff)
        return good_stuff_st

    @dec_check_none
    def get_tx_issues(self, soup: BeautifulSoup)-> list:
        issues_html = soup.find_all('ul', id='issuesData')
        issues_list = list(issues_html[0].children)
        
        ##if want to return string instead
        # issues_str = issues_html[0].get_text()
        # clean_str = clean_string(issues_str)
        list_text = self.convert_html_list(issues_list)
        return list_text

    @dec_check_none
    def get_orientations(self, soup: BeautifulSoup)-> list:
        orientations_html = soup.find_all('ul', id='modelsData')
        orientations_list = list(orientations_html[0].children)
        
        ##if want to return string instead
        # issues_str = issues_html[0].get_text()
        # clean_str = clean_string(issues_str)
        list_text = self.convert_html_list(orientations_list)
        return list_text

    @dec_check_none
    def get_services(self, soup: BeautifulSoup)-> list:
        services_html = soup.find_all('ul', id='servicesprovidedData')
        services_list = list(services_html[0].children)
        
        list_text = self.convert_html_list(services_list)
        return list_text

    @dec_check_none
    def get_client_ages(self, soup: BeautifulSoup) -> list:
        ages_html = soup.find_all('ul', id='agesData')
        ages_list = list(ages_html[0].children)
        
        list_text = self.convert_html_list(ages_list)
        return list_text

    @dec_check_none
    def get_professions(self, soup: BeautifulSoup) -> list:
        profs_str = soup.find('span', id='professionsDefined').get_text()
        profs_list = profs_str.split(',')
        
        return [prof.strip() for prof in profs_list]

    @dec_check_none
    def get_primary_credential(self, soup: BeautifulSoup) -> str:
        credential = soup.find('span', id='licenceinfo1').get_text()
        
        return self.clean_escapes(credential)

    @dec_check_none
    def get_license_status(self, soup: BeautifulSoup) -> str:
        license_status = soup.find('span', id='license_status_id').get_text()
        
        return self.clean_escapes(license_status)

    @dec_check_none
    def get_website(self, soup: BeautifulSoup) -> str:
        try:
            website = soup.find('a', id='edit_website')['href']
        except:
            website = 'None'
        return website

    def get_address(self, soup: BeautifulSoup) -> dict:
        #office = soup.find('div', id='editOffice1')
        address = {}
        
        address['street'] = self.sub_get_street(soup)
        address['city'] = self.sub_get_city(soup)
        address['state'] = self.sub_get_state(soup)
        address['zip'] = self.sub_get_zip(soup)
        
        return address

    @dec_check_none
    def sub_get_street(self, soup: BeautifulSoup) -> str:
            return soup.find('span', itemprop='streetAddress').get_text()

    @dec_check_none      
    def sub_get_city(self, soup: BeautifulSoup) -> str:
        return soup.find('span', itemprop='addressLocality').get_text()

    @dec_check_none
    def sub_get_state(self, soup: BeautifulSoup) -> str:
        return soup.find('span', itemprop='addressRegion').get_text()

    @dec_check_none            
    def sub_get_zip(self, soup: BeautifulSoup) -> str:
        return soup.find('span', itemprop='postalCode').get_text()

    @dec_check_none
    def get_phone(self, soup: BeautifulSoup) -> str:
        phone  =soup.find('span', {'class':'profilePhone'}).text

        return self.clean_string(phone)

    @dec_check_none
    def get_verification(self, soup: BeautifulSoup) -> bool:
        verified  = soup.find('div', {'class':'profileVer'}).text

        return self.clean_string(verified) == 'Verified'

if __name__ == '__main__':
    import psycopg2

    conn = psycopg2.connect(dbname='therapist_predictor', user='postgres', host='localhost', password='password')
    cur = conn.cursor()

    #start_url = 'https://www.goodtherapy.org/therapists/profile/jessica-fern-cooley-20170717'
    start_url = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Jennifer.html'
    good_scraper = GoodTherapySoupScraper(starting_url=start_url, is_local_file=True)
    soup = good_scraper.get_soup()

    all_data = good_scraper.get_all_data(soup)

    #therapist_id = cur.execute("""DROP TABLE IF EXISTS quotes""")
    services = good_scraper.get_services(soup)
    print(all_data['full_name'])
    print(all_data['first_name'])
    print(all_data['last_name'])
    print(all_data['phone'])

    conn.close()
