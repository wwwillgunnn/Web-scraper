"""
This is an eBay web scraper with the purpose of finding ebay listings that have things on the EEPL list
Then that data is stored in a spreadsheet

Made by William Gunn
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_page(name):
    # Create list for data frame
    data = []
    page_number = 1
    while True:
        # Get page information
        page_url = f"https://www.ebay.com.au/sch/i.html?_from=R40&_nkw={name}&_sacat=190&rt=nc&_pgn={page_number}"
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, "html.parser")
        # get total results for looping
        total_results = soup.find(id="mainContent")
        count = total_results.find(class_="srp-controls__count-heading")
        count_number = count.find("span", class_="BOLD")
        # Loop through all pages on site
        if page_url is not None and int(count_number.text.strip().replace(',', '')) > 0:
            # Get page data
            results = soup.find(id="srp-river-main")
            product_listings = results.find_all("li", class_="s-item s-item__pl-on-bottom")
            # Loop through each listing on the page (skip 1st listing, its bugged)
            for item in product_listings[1:]:
                title = item.find("span", role="heading")
                price = item.find("span", class_="s-item__price")
                seller_name = item.find("span", class_="s-item__seller-info")
                # Store data in a dictionary
                items = {"Title": title.text.strip(),
                         "Price": price.text.strip(),
                         "Seller Name": seller_name.text.strip(),
                         }
                try:
                    seller_location = item.find("span", class_="s-item__location s-item__itemLocation")
                    items["Seller Location"] = seller_location.text.strip()
                except AttributeError:
                    seller_location = "Australia"  # Maybe have 'None' I'm just assuming it's in Australia
                    items["Seller Location"] = seller_location
                # Append to list
                data.append(items)
            # Increment page number
            int(page_number)
            page_number += 1
            print(page_url)
        else:
            break
    # Export data to a spreadsheet
    print(data)
    export_data(data)


def export_data(full_data):
    df = pd.DataFrame(full_data)
    df.to_excel("searchResults.xlsx")


def main():
    # Input URL of choice
    listing_name = input("Enter an Ebay listing (EEPL species): ")
    print()
    # Call scrape page function
    scrape_page(listing_name)


if __name__ == "__main__":
    main()
    
