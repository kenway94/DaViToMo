import re
import os
import wikipedia as wp
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# # Set up the MongoDB client and database
client = MongoClient(os.getenv('DB_URI'))

db = client["DaViToMo"]

main_page = sys.argv[1]

# This is the name of the Wikipedia page
# main_page = "Morty_Smith"  # from the TV show "Rick & Morty"
# main_page = "Turing_Award"
# main_page = "The_Matrix"

# main_page = input("Enter an article with a _ between each word: ")

# # Create a new collection to store the articles with the name of the main page
collection = db[main_page]

articles=[]

col = collection.find_one()
if col == None:
    # Fetch the webpage
    main = wp.page(main_page, auto_suggest=False)
    print("== Downloading %s: %d links" % (main_page, len(main.links)))

    # print("Downloading to MongoDB database")
    # print("Type Y and Enter to continue")
    # yes = input().lower()
    # if yes != "y": exit()

    # Add page, and all links on page to the list of pages to download
    links = [main_page] + main.links
    for link in links:
        # Skip pages that are "List of" or "Category" pages
        if link.startswith("List"): continue

        # Try to download the page
        # print(link)
        try:
            page = wp.page(link, auto_suggest=False, preload=False)
        except wp.exceptions.PageError:
            print("    page not found, skipping")
            continue
        except wp.exceptions.DisambiguationError:
            print("    ambiguous name, skipping")
            continue
        except:
            print("    unexpected error, skipping")
            continue

        # Check if we already downloaded the page, and skip if it exists
        pageid = page.pageid
        if collection.find_one({"_id": pageid}):
            print("    page previously saved, skipping")
            continue

        # Get the title and text from the page
        title = page.title
        text = page.content
        # Remove non-alphabetic characters from text
        clean_text = re.sub('[^A-Za-z]+', ' ', text)

        # Insert the article into the MongoDB collection
        article = ({"_id": pageid, "title": title,  "text": clean_text})
        collection.insert_one(article)
    

