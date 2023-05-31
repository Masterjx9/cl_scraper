from bs4 import BeautifulSoup
import requests

craigslistpage = requests.get("https://newyork.craigslist.org/search/brk/cpg")
soup = BeautifulSoup(craigslistpage.text, "html.parser")

results_div = soup.find("div", class_="results cl-results-page cl-search-view-mode-thumb cl-two-column")
if results_div:
    listing_ol = results_div.find("ol")
    if listing_ol:
        listings = listing_ol.find_all("li")

        for listing in listings:
            title = listing.find("a", class_="result-title").text
            link = listing.find("a", class_="result-title")["href"]
            print("Title:", title)
            print("Link:", link)
            print()
    else:
        print("No listings found.")
else:
    print("No results div found.")
