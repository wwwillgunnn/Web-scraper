"""
This is an eBay web scraper with the purpose of finding ebay listings that have things on the EEPL list
Then that data is stored in a spreadsheet

IMPORTANT NOTE: eBay has a limit on how many items you can search for in 1 session,
It's reccomended to use 1 pest classification at a time, else you will run into this issue :^).

Made by William Gunn
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Exotic Environmental Pests List
EEPL = [
    # Fresh water invertebrates
    "Asian clam", "Assassin snail", "Bloody-red mysid shrimp", "Chinese mitten crab", "Chinese mystery snail",
    "Japanese mystery snail", "Danube crayfish", "Turkish crayfish", "Freshwater mussel", "Golden apple snail",
    "Island apple snail", "Golden mussel", "Horn snail", "Louisiana red crayfish", "Mud snail", "Northen crayfish",
    "Virile crayfish", "Quagga mussel", "Zebra mussel", "Quilted melania", "Rusty crayfish", "Serrate crownsnail",
    "Signal crayfish", "Spinycheek crayfish", "Freshwater snails",
    # Marine pests
    "Asian brackish-water clam", "Overbite clam", "Asian green mussel", "Atlantic oyster drill",
    "Black-striped false mussel", "Brown mussel", "Brush-clawed shore crab", "Carpet sea squirt", "Centric diatom",
    "Mitten crab", "Comb jelly", "Harris' mud crab", "Japanese shore crab", "Japanese skeleton shrimp",
    "Japanese wireweed", "Lady crab", "Asian paddle crab", "New Zealand green-lipped mussel", "Red whelk",
    "Red-gilled mudworm", "Soft shelled clam", "Toxic dinoflagellate",
    # Terrestrial invertebrates
    "Africanised honeybee", "Annona mealybug", "Asian hornet", "Yellow-legged hornet", "Asian beetle mite",
    "Asian gypsy moth", "Brown marmorated stink bug", "Cape honeybee", "Common eastern bumblebee",
    "Cycad aulacaspis scale", "Delta wasp", "Dichroplus grasshopper", "Electric ant", "Formosan subterranean termite",
    "Giant african snail", "Gold dust weevil", "Harlequin lady beetle", "Multicolored Asian lady beetle",
    "Honey bee tracheal mite", "Oriental powderpost beetle", "Picnic beetle", "Red imported fire ant",
    "Rosy predator snail", "Shot hole borer", "Western drywood termite",
    # Vertebrate pests
    "African pygmy hedgehog", "Asian black-spined toad", "Asian painted frog", "Boa constrictor", "Burmese python",
    "Chinese carp", "Climbing perch", "Common snapping turtle", "Corn snake", "Fire bellied newt",
    "Flat-tailed house gecko", "Green iguana", "Grey squirrel", "House crow", "Nile tilapia", "Oriental garden lizard",
    "Pacific rat", "Red-eared slider turtle", "Silver carp", "Snakeheads", "Stoat", "Veiled chameleon", "Walking catfish"
    # Weeds and freshwater alge
    "Asiatic sans sedge", "Black sage", "Black swallow-wort", "Brittle naiad", "Cane tibouchina", "Didymo", "Halogeton",
    "Karoo thorn", "Lagariosiphon", "Leafy spurge", "Limnocharis flava", "Manchurian wildrice", "Mikania",
    "Mouse-ear hawkweed", "Nepalese browntop", "Portuguese broom", "Slangbos", "South african ragwort", "Spiked pepper",
    "Water primrose", "Wiregrass"
    ]
# Create list for data frame
data = []


def scrape_pages():
    # Create persistent session
    session = requests.Session()
    for eepl_species in EEPL:
        get_data(session, eepl_species)
    export_data(data)


def get_data(session, eepl_species):
    page_number = 1
    while True:
        page_url = f"https://www.ebay.com.au/sch/i.html?_from=R40&_nkw={eepl_species.replace(' ', '+')}&_sacat=190&rt=nc&_pgn={page_number}"
        response = session.get(page_url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"})
        soup = BeautifulSoup(response.text, "lxml")
        # Get total item count of page
        try:
            count = soup.find(class_="srp-controls__count-heading")
            count_number = count.find("span", class_="BOLD").text.strip()
        except AttributeError:
            print("Too many items were seen on eBay, try to refine search options")
            export_data(data)
            break
        # Check if page is legitimate for collecting data from
        if page_url is not None and int(count_number.replace(',', '')) > 0 and count_number is not None:
            results = soup.find(id="srp-river-main")
            product_listings = results.find_all("li", class_="s-item__pl-on-bottom")
            # Use list comprehension for creating the data frame
            data.extend([
                {"Title": item.find("span", role="heading").get_text().strip(),
                 "Price": item.find("span", class_="s-item__price").get_text().strip(),
                 "Seller Name": item.find("span", class_="s-item__seller-info-text").get_text().strip()
                 if item.find("span", class_="s-item__seller-info") else "None",
                 "Seller Location": item.find("span", class_="s-item__itemLocation").get_text().strip()
                 if item.find("span", class_="s-item__itemLocation") else "Australia",
                 "Species": eepl_species}
                # Loop through each listing
                for item in product_listings[1:]
            ])
            # Loop to the next page
            navigation = results.find("nav", class_="pagination")
            next_page = soup.find("a", class_="pagination__next")
            if navigation is not None and next_page is not None:
                page_number += 1
                # Introduce a delay between requests
                time.sleep(1)
            else:
                break
        else:
            break


def export_data(data_frame):
    df = pd.DataFrame(data_frame)
    df.to_excel("Results.xlsx", index=False)


def main():
    print("Scraping pages...")
    scrape_pages()


if __name__ == "__main__":
    main()
