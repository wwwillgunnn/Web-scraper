"""
This is an eBay web scraper with the purpose of finding ebay listings that have things on the EEPL list
Then that data is stored in a spreadsheet

Made by William Gunn
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

# EEPL
EEPL = [
    # Fresh water invertebrates
    "Asian clam", "Assassin snail", "Bloody-red mysid shrimp", "Chinese mitten crab", "Chinese mystery snail",
    "Japanese mystery snail", "Danube crayfish", "Turkish crayfish", "Freshwater mussel", "Golden apple snail",
    "Island apple snail", "Golden mussel", "Horn snail", "Louisiana red crayfish", "Mud snail", "Northen crayfish",
    "Virile crayfish", "Quagga mussel", "Zebra mussel", "Quilted melania", "Rusty crayfish", "Serrate crownsnail",
    "Signal crayfish", "Spinycheek crayfish", "Freshwater snails",
    # Marine pests
    "Asian brackish-water clam", "Overbite clam",
    "Asian green mussel", "Atlantic oyster drill", "Black-striped false mussel", "Brown mussel",
    "Brush-clawed shore crab", "Carpet sea squirt", "Centric diatom", "Mitten crab", "Comb jelly", "Harris' mud crab",
    "Japanese shore crab", "Japanese skeleton shrimp", "Japanese wireweed", "Lady crab", "Asian paddle crab",
    "New Zealand green-lipped mussel", "Red whelk", "Red-gilled mudworm", "Soft shelled clam", "Toxic dinoflagellate"
    # Terrestrial invertebrates
                                                                                               "Africanised honeybee",
    "Annona mealybug", "Asian hornet", "Yellow-legged hornet", "Asian beetle mite", "Asian gypsy moth",
    "Brown marmorated stink bug", "Cape honeybee", "Common eastern bumblebee", "Cycad aulacaspis scale", "Delta wasp",
    "Dichroplus grasshopper",
    "Electric ant", "Formosan subterranean termite", "Giant african snail", "Gold dust weevil", "Harlequin lady beetle",
    "Multicolored Asian lady beetle",
    "Honey bee tracheal mite", "Oriental powderpost beetle", "Picnic beetle", "Red imported fire ant",
    "Rosy predator snail", "Shot hole borer",
    "Western drywood termite",
    # Vertebrate pests
    "African pygmy hedgehog", "Asian black-spined toad", "Asian painted frog", "Boa constrictor", "Burmese python",
    "Chinese carp", "Climbing perch",
    "Common snapping turtle", "Corn snake", "Fire bellied newt", "Flat-tailed house gecko", "Green iguana",
    "Grey squirrel", "House crow",
    "Nile tilapia", "Oriental garden lizard", "Pacific rat", "Red-eared slider turtle", "Silver carp", "Snakeheads",
    "Stoat",
    "Veiled chameleon", "Walking catfish"
    # Weeds and freshwater alge
                        "Asiatic sans sedge", "Black sage", "Black swallow-wort", "Brittle naiad", "Cane tibouchina",
    "Didymo", "Halogeton", "Karoo thorn",
    "Lagariosiphon", "Leafy spurge", "Limnocharis flava", "Manchurian wildrice", "Mikania", "Mouse-ear hawkweed",
    "Nepalese browntop", "Portuguese broom",
    "Slangbos", "South african ragwort", "Spiked pepper", "Water primrose", "Wiregrass"
]
# Create list for data frame
data = []


def scrape_page():
    for eepl_species in EEPL:
        eepl_species_listing = eepl_species.replace(" ", "+")
        page_number = 1
        while True:
            # Use session for HTTP requests
            with requests.Session() as session:
                # Get page HTML information
                page_url = f"https://www.ebay.com.au/sch/i.html?_from=R40&_nkw={eepl_species_listing}&_sacat=190&rt=nc&_pgn={page_number}"
                response = session.get(page_url)
                soup = BeautifulSoup(response.text, "lxml")
            # Get total results for looping
            count = soup.find(class_="srp-controls__count-heading")
            count_number = count.find("span", class_="BOLD").get_text().strip()
            # Loop through all pages on site
            if page_url is not None and int(count_number.replace(',', '')) > 0:
                # Get page data
                results = soup.find(id="srp-river-main")
                product_listings = results.find_all("li", class_="s-item__pl-on-bottom")
                # Use list comprehension for creating the data set
                data.extend([
                    {"Title": item.find("span", role="heading").get_text().strip(),
                     "Price": item.find("span", class_="s-item__price").get_text().strip(),
                     "Seller Name": item.find("span", class_="s-item__seller-info").get_text().strip()
                     if item.find("span", class_="s-item__seller-info") else "None",
                     "Seller Location": item.find("span", class_="s-item__itemLocation").get_text().strip()
                     if item.find("span", class_="s-item__itemLocation") else "Australia"}
                    for item in product_listings[1:]
                ])
                # Check to see if theres next page
                navigation = results.find("nav", class_="pagination")
                next_page = soup.find("a", class_="pagination__next")
                if navigation is not None and next_page is not None:
                    # Increment page number
                    page_number += 1
                    print(page_url)
                else:
                    break
            else:
                break
    # Export data to a spreadsheet
    print(data)
    export_data(data)


def export_data(full_data):
    df = pd.DataFrame(full_data)
    df.to_excel("Results.xlsx")


def main():
    # Call scrape page function
    print("Scraping page ...")
    scrape_page()


if __name__ == "__main__":
    main()
