DaftScraper
===========

Data miner for Daft.ie

This project contains two modules

#The Daft Scraper
  This module has an optional scraper to iterate through the pages of daft.ie's rental listings and store the scraped info for mining
  This module also has a GET request that takes advantage of a hole in the ajax requests daft.ie's map views rely upon.
    This request allows us to specify the top left of ireland, and the bottom right as the search params along with price, rental or buy, etc.
    
  As each item is put through the pipeline there is an option to persist the item, and then an option to email the item.
  
#The Data Miner
  This module is served by a CherryPy python web server, within you will find a web site and a data miner
  The data miner performs some trivial operations upon the data base to allow a user to predict the price of a home given an area and set of facilities.
