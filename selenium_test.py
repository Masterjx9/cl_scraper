import time
# start_time = time.time()
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import fulllist


# Path to the chromedriver executable
# chromedriver_path = './chromedriver'  # Update with the actual path if needed

# Configure Chrome options for headless browsing
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/chromium-browser"
chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.add_argument('--incognito')  # Run Chrome in incognito mode
chrome_options.add_argument('--disable-cache')  # Disable browser caching
chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
chrome_options.add_argument('--log-level=3')  # Set log level to suppress DevTools log
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver_path = "/usr/bin/chromedriver"
# Create a new instance of the Chrome driver with the configured options
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver = webdriver.Chrome(options=chrome_options, service=Service(driver_path))
driver.get("https://www.google.com")

def get_post_info(url, fulldatalist):
    linkcheck =[]
    for loccheck in fulldatalist:
        linkcheck.append(loccheck["Link"])
    # Load the page
    driver.get(url)
    time.sleep(3)

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Define the current date
    current_date = datetime.now()

    # Define the timedelta for 3 days
    three_days = timedelta(days=3)

    # Find all listing items
    listings = soup.find_all("li")

    # print(listings)
    postinfolist = []

    # Iterate over each listing and extract title, link, and date
    for listing in listings:
        temp_postinfo = {}

        # Extract date
        date_span = listing.find("span", title=lambda value: value and "Pacific Daylight Time" in value)
        if date_span:
            date_str = date_span["title"].split(" GMT")[0]
            date = datetime.strptime(date_str, "%a %b %d %Y %H:%M:%S")
            # Check if the date is within 3 days
            if current_date - date <= three_days:
                

                # Extract title and href
                if listing.find("a", class_="titlestring"):
                    if listing.find("a", class_="titlestring")["href"] not in linkcheck:
                        temp_postinfo["date"] = date_str
                        title = listing.find("a", class_="titlestring").text
                        href = listing.find("a", class_="titlestring")["href"]
                        temp_postinfo["Title"] = title
                        temp_postinfo["Link"] = href
                    
                    # print(temp_postinfo["date"])
                    # print(temp_postinfo["Title"])
                    # print(temp_postinfo["Link"])
                    # print(listing)
                    


                if temp_postinfo:
                    postinfolist.append(temp_postinfo)

    return postinfolist

def save_post_info_to_json(post_info, location):
    filename = f"locationdata/{location.replace('/', '')}.json"
    postinfodict = {location: post_info}
    with open(filename, "w") as json_file:
        json.dump(postinfodict, json_file, indent=4)

def save_all_post_to_list(location, datalist, fulldatalist):
    for da in datalist:
        da["location"] = location
    fulldatalist.extend(datalist)  # use extend instead of append
    return fulldatalist


def all_posts_to_json_from_list(fulldatalist):
    filename = "alllocdata.json"
    postinfodict = {"data": fulldatalist}
    with open(filename, "w") as json_file:
        json.dump(postinfodict, json_file, indent=4)

# Example usage
# print(fulllist.cl_list)

fulldatalist = [] #initialize the list here
# for i in range(4): ## For testing
#     item = fulllist.cl_list[i] ## For testing
while True:
    for item in fulllist.cl_list:
        print("Now processing: "+item["state_name"])
        for locs in item["state_list"]:
            print(locs["location"])
            print(locs["link"]+"/search/cpg?bundleDuplicates=1")
            post_info = get_post_info(locs["link"]+"/search/cpg?bundleDuplicates=1", fulldatalist)
            fulldatalist = save_all_post_to_list(locs["location"], post_info, fulldatalist)
            if post_info: 
                save_post_info_to_json(post_info, locs["location"])
    all_posts_to_json_from_list(fulldatalist)
# Quit the browser
driver.quit()

end_time = time.time()
elapsed_time = end_time - start_time
print(f"The script took {elapsed_time} seconds to complete.")
print(f"The script took {elapsed_time / 60} minutes to complete.")
