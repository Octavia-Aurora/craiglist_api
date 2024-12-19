from fastapi import FastAPI, Query
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

# Initialize FastAPI app
app = FastAPI()

# Function to scrape Craigslist listings
def scrape_craigslist(city: str, object: str) -> List[Dict]:
    # Construct the Craigslist URL
    url = f"https://{city}.craigslist.org/search/sss?free=1&query={object}#search=1~gallery~0~0"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    # Send an HTTP GET request
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return [{"Error": f"Failed to fetch the page. Status code: {response.status_code}"}]

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.find_all("li", class_="cl-static-search-result")

    # Extract data from each listing
    data = []
    for listing in listings[:50]:  # Limit to 50 listings
        title = listing.find("div", class_="title").text.strip() if listing.find("div", class_="title") else "No Title"
        price = listing.find("div", class_="price").text.strip() if listing.find("div", class_="price") else "No Price"
        location = listing.find("div", class_="location").text.strip() if listing.find("div", class_="location") else "No Location"
        link = listing.find("a")["href"] if listing.find("a") and "href" in listing.find("a").attrs else "No Link"

        data.append({
            "Title": title,
            "Price": price,
            "Location": location,
            "Link": link
        })

    return data

# API Endpoint to scrape Craigslist
@app.get("/scrape/")
def scrape(city: str = Query(..., description="City name for Craigslist search"), 
           object: str = Query(..., description="Object to search for")):
    """
    Scrape Craigslist listings for a specific city and search query.
    Example: /scrape/?city=houston&object=Couch
    """
    return scrape_craigslist(city, object)
