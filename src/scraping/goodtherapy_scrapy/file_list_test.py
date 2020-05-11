import scrapy
from os import listdir
from os.path import isfile, join
from .items import TherapistItem
from .good_therapy_scraper import GoodTherapySoupScraper

#mypath = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Denver/'
mypath = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/'
prefix = 'file://'
onlyfiles = [(prefix + mypath + f) for f in listdir(mypath) if isfile(join(mypath, f))]

#file_and_path = prefix + mypath + f
print(onlyfiles)

def get_search_results_paths(self)->list:
    #mypath = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/TherapistListings/Denver/'
    mypath = '/home/cgridley/Galvanize/repos/capstones/TherapistFitter/data/html/'
    prefix = 'file://'
    return [(prefix + mypath + f) for f in listdir(mypath) if isfile(join(mypath, f))]


for f in onlyfiles:
    good_tx_scraper = GoodTherapySoupScraper(f, True)
    soup = good_tx_scraper.get_soup()
    print(good_tx_scraper.get_all_data(soup))
