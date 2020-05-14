import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup    

class WebCrawler(object):
    def __init__(self, starting_url: str):
        self.starting_url =  starting_url
        self.visited = set()

    def get_html(self, url: str):
        try:
            html = requests.get(url)
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('latin-1')

    def get_links(self, url:str):
        html = self.get_html(url)
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base = base + link
                links[i] = link_with_base

        return set(filter(lambda x: 'mailto' not in x, links))

    def extract_info(self, url: str) -> BeautifulSoup:
        # #html = self.get_html(url)
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
        # breakpoint()
        # page = requests.get(url, headers=headers)
        # soup = BeautifulSoup(page.content, 'html.parser')
        # soup.prettify()
        # return soup                  
        html = self.get_html(url)
        meta = re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>", html)
        return dict(meta)

    def crawl(self, url: str):
        for link in self.get_links(url):
            # we only want to crawl therapist profile pages associated with the starting link
            is_next_page_link = link.find('www.goodtherapy.org/search2') != -1
            is_therapist_profile_link = link.find('www.goodtherapy.org/therapists/profile/') != -1

            if link in self.visited:
                continue
            print(link)

            self.visited.add(link)
            if(is_next_page_link or is_therapist_profile_link):
                soup = self.extract_info(link)
                #self.temp(soup)
                self.crawl(link)
            else:
                pass

    def start(self):
        self.crawl(self.starting_url)

    def temp(self, soup: BeautifulSoup):
        h2_ls = soup.find_all('h2')
        for h2 in list(h2_ls):
            try:
                print(f'H2: {h2.get_text()}')
            except Exception as e:
                print(e)
                continue
                

if __name__ == '__main__':
    denver_therapists = 'https://www.goodtherapy.org/search2.html?search%5Btherapist_search%5D=Find+a+Therapist&search%5' \
        'Bstate%5D=&search%5Bzipcode%5D=denver%2C+colorado&search%5Blat%5D=39.7392358&search%5Blon%5D=-104.990251&search%5' \
            'Bmiles%5D=25&search%5Bcity_log%5D=Denver&search%5Bcity_log_short%5D=Denver&search%5Bstate_log%5D=Colorado&search%5' \
                'Bstate_log_short%5D=CO&search%5Bcountry_log%5D=United+States&search%5Bcountry_log_short%5D=US&TOS_agreement=P&fromheader=1'
    inbtwn = 'http://www.inbetweentherapy.com'
    brickset = "https://brickset.com/"

    crawler = WebCrawler(inbtwn)        
    crawler.start()
