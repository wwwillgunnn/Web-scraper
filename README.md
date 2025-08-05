# 🕷️ Exotic Pest Web Scraper
This project is a web scraper designed to identify and log listings of exotic environmental pests on online marketplaces (currently tailored for eBay Australia). Its primary goal is to assist in the early detection and reporting of exotic pest trading activities, which can have serious environmental impacts in Australia.

## 🚀 Features
- Scrapes data from eBay listings related to known exotic pests.
- Extracts listing title, price, seller info, and location.
- Supports proxy rotation to help bypass request limits.
- Saves results to an Excel file for easy analysis.
- Easy to adapt for other e-commerce sites with minimal changes.

## 📜 Supported Species
The scraper checks listings against an extensive Exotic Environmental Pests List (EEPL), including:
- Freshwater invertebrates (e.g. Zebra mussel, Golden apple snail)
- Marine pests (e.g. Mitten crab, Comb jelly)
- Terrestrial invertebrates (e.g. Red imported fire ant, Asian hornet)
- Vertebrate pests (e.g. Burmese python, Green iguana)
- Weeds and algae (e.g. Water primrose, Black sage)
See the EEPL list in the source code for the complete reference.

## 🧠 Notes
- This script is configured specifically for eBay. To adapt it to another website, you'll need to:
- Change the base URL in the get_data() function.
- Update the HTML tag selectors (soup.find(), etc.) based on the site's structure.
  
⚠️ eBay enforces a 10,000-item search limit per query. To handle this, the script rotates through proxies and paginates results.

## 👤 Author - William Gunn
Created as part of an initiative to monitor the illegal trade of exotic pests in Australia.
