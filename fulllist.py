import requests
from bs4 import BeautifulSoup
import json
cl_usa_list = requests.get("https://www.craigslist.org/about/sites#US")
soup = BeautifulSoup(cl_usa_list.text, "html.parser")

# Find the <h4> elements containing state names
state_elements = soup.find_all("h4")

cl_list = []
# Iterate over each state element and extract the links
for state_element in state_elements:
    cl_dict = {}
    state_name = state_element.get_text()
    state_links = state_element.find_next("ul").find_all("a")

    # print(state_name)
    cl_dict["state_name"] = state_name
    cl_dict["state_list"] = []
    for link in state_links:
        loc_dict = {}
        location_name = link.get_text()
        location_url = link["href"]
        # print(location_name, location_url)
        loc_dict["location"] = location_name
        loc_dict["link"] = location_url
        # print()
        cl_dict["state_list"].append(loc_dict)
    cl_list.append(cl_dict)

# print(cl_list)

with open("test.json", "w") as json_file:
    json.dump({"data":cl_list}, json_file, indent=4)
