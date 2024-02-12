"""
This is an eBay web scraper with the purpose of finding and storing ebay listings that have
pests on the Exotic Environmental Pest List (EEPL)

This module will only print out results to the terminal

Made by William Gunn
"""
import requests
from bs4 import BeautifulSoup

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
    "Africanised honeybee", "Annona mealybug", "Asian hornet", "Yellow-legged hornet", "Asian beetle mite", "Asian gypsy moth",
    "Brown marmorated stink bug", "Cape honeybee", "Common eastern bumblebee", "Cycad aulacaspis scale", "Delta wasp", "Dichroplus grasshopper",
    "Electric ant", "Formosan subterranean termite", "Giant african snail", "Gold dust weevil", "Harlequin lady beetle", "Multicolored Asian lady beetle",
    "Honey bee tracheal mite", "Oriental powderpost beetle", "Picnic beetle", "Red imported fire ant", "Rosy predator snail", "Shot hole borer",
    "Western drywood termite",
    # Vertebrate pests
    "African pygmy hedgehog", "Asian black-spined toad", "Asian painted frog", "Boa constrictor", "Burmese python", "Chinese carp", "Climbing perch",
    "Common snapping turtle", "Corn snake", "Fire bellied newt", "Flat-tailed house gecko", "Green iguana", "Grey squirrel", "House crow",
    "Nile tilapia", "Oriental garden lizard", "Pacific rat", "Red-eared slider turtle", "Silver carp", "Snakeheads", "Stoat",
    "Veiled chameleon", "Walking catfish"
    # Weeds and freshwater alge
    "Asiatic sans sedge", "Black sage", "Black swallow-wort", "Brittle naiad", "Cane tibouchina", "Didymo", "Halogeton", "Karoo thorn",
    "Lagariosiphon", "Leafy spurge", "Limnocharis flava", "Manchurian wildrice", "Mikania", "Mouse-ear hawkweed", "Nepalese browntop", "Portuguese broom",
    "Slangbos", "South african ragwort", "Spiked pepper", "Water primrose", "Wiregrass"
    ]


def scrape_page():
    # Loop through all pages on site
    page_number = 1
    for EEPL_species in EEPL:
        EEPL_species_listing = EEPL_species.replace(" ", "+")
        # Get page information
        page_url = f"https://www.ebay.com.au/sch/i.html?_from=R40&_nkw={EEPL_species_listing}&_sacat=190&rt=nc&_pgn={page_number}"
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, "html.parser")
        # Get page result number
        results = soup.find(id="mainContent")
        navigation = results.find("nav", class_="pagination")
        count = results.find(class_="srp-controls__count-heading")
        count_number = count.find("span", class_="BOLD")
        # Check page exists
        if page_url is not None and int(count_number.text.strip().replace(',', '')) > 0:
            # Get page data
            get_data(soup)
            # For when a page doesn't only have 1 page
            if navigation is not None:
                # Increment page number
                int(page_number)
                page_number += 1
                print(page_url)
            else:
                continue
        else:
            continue


def get_data(content):
    # Get HTML data from listings
    results = content.find(id="srp-river-main")
    product_listings = results.find_all("li", class_="s-item__pl-on-bottom")
    # Loop through each listing on the page (skip 1st listing)
    for item in product_listings[1:]:
        title = item.find("span", role="heading")
        price = item.find("span", class_="s-item__price")
        print(title.text.strip())
        print(price.text.strip())
        # if the format is different on the site
        try:
            seller_name = item.find("span", class_="s-item__seller-info")
            print(seller_name.text.strip())
        except AttributeError:
            seller_name = item.find("span", class_="s-item__seller-info-text__field-0")
            seller_name2 = item.find("span", class_="s-item__seller-info-text__field-1")
            if (seller_name and seller_name2) is not None:
                print(seller_name.text.strip())
                print(seller_name.text.strip())
            else:
                seller_name = "None"
                print(seller_name)
        try:
            seller_location = item.find("span", class_="s-item__location s-item__itemLocation")
            print(seller_location.text.strip())
        except AttributeError:
            seller_location = "Australia"  # Maybe have 'None' I'm just assuming it's in Australia
            print(seller_location)
        try:
            watching = item.find("span", class_="s-item__dynamic s-item__watchCountTotal")
            print(watching.text.strip())
        except AttributeError:
            watching = "None watching"
            print(watching)
        print()


def main():
    # Call scrape page function
    print("Scraping page ...")
    scrape_page()


if __name__ == "__main__":
    main()
