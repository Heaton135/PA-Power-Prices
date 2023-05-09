import os
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import date
import time
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

chrome_options = webdriver.ChromeOptions()

# Getting current working directory for file download navigation
global cwd
cwd = os.getcwd()

# Setting chrome options 
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--disable-dev-shm-usage')
prefs = {'download.default_directory' : cwd}
chrome_options.add_experimental_option('prefs', prefs)

# Pass in our custom options to chrome
driver = webdriver.Chrome(chrome_options=chrome_options)
failed_zips = []

# This dataframe will serve as our repository for all data until we are ready to export all results at the end
global fullData
fullData = pd.DataFrame(columns = ['Price', 'Supplier', 'Type', 'Cancellation Fee', 'Discounts available?',
       'Introductory price?', 'More info', 'Service Type', 'Rate type',
       'Term Length', 'PA wind', 'Renewable Energy', 'Term End Date',
       'Enrollment Fee', 'Monthly service fee amount', 'date', 'zipcode'])


def main():
    print("---------------------------------")
    print("\nWelcome to PA rates scraper!..")
    print("Gathering Zip Codes...\n")

    zips = {"Duquesne Light":15106, "Met-Ed":17325, "PECO":19109, "Penelec":16619, "PennPower":15086, "PPL":18015,"Pike-County-LP":18324, "UGI":18622, "WestPenn":15020}
    # Referring to global variable to hold all of our data.
    global fullData
    print("\n-------- Begin Scraping ---------\n")

    # first flag to handle tutorial iteration
    first = True
    fullTime = 0    # tracks the full time elapsed (s)
    count = 0       # tracks the number of zip codes processed
    total = len(zips)   # total # of zips to be processed


    for x in zips:
  
        print("Getting data for zip: "+ str(zips[x]))
        tic = time.perf_counter()
        getRates(zips[x],first)
        first = False
        fullData = importResults(zips[x],fullData, x)
        count += 1
        toc = time.perf_counter()
        fullTime += toc-tic
        print("Processed zip: "+str(zips[x])+f" data in {toc - tic:0.4f} seconds   (",count,"/",total,")")

    print("\n--------- Done Scraping ---------\n")
    print(f"Full time elapsed: {fullTime:0.4f} s")
    print(f"Avg. time per zipcode: {fullTime/count:0.4f}s \n")
    # Close our chrome window
    driver.close()
    print("Closing Browser Window....")
    print("Exporting results to csv....")


    
    filepath = Path('Output-Files/'+date.today().strftime('%Y-%m-%d')+'-RS.csv')
    path = date.today().strftime('%Y-%m-%d')+'-RS.csv'
    fullData.to_csv(filepath)

    print("Exporting done. Process Finished.")
    print("---------------------------------")

    return


#This function takes the passed in Zipcode and Navigates to Papowerswitch.com and downloads the desired results
def getRates(zipcode, isFirst):

    # Navigate to website using zipcode
    url = 'https://www.papowerswitch.com/shop-for-electricity/shop-for-your-home?type=all&zip=' + str(zipcode)
    driver.get(url)

    try:
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-id='27499']"))).click()
            # driver.find_element(By.XPATH, "//a[@data-id='27513']").click()
    except:
        pass
     # Handles website tutorial case
    if(isFirst == True):
        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//a[@data-id='27488']"))).click()
            # driver.find_element(By.XPATH, "//a[@data-id='27513']").click()
        except:
            pass
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-skipbutton"))).click()
        except:
            pass

    time.sleep(1)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,"export-results"))).click()
        # driver.find_element(By.ID,"export-results").click()
    except:
        print("Error downloading results for: " + str(zipcode))
        return


# This function opens the downloaded csv results file, processes the data,
# adds Date and Zip code, and then appends the new data to our full Dataframe
def importResults(zipcode, fullData, provider):

    global failed_zips
    # This while loop is supposed to wait for the downloaded file to be found until 5 seconds has passed, we assume the file was never downloaded
    timer_count = 0
    myfile = cwd+'/rates.csv'
    while not os.path.exists(myfile):
        time.sleep(1)
        timer_count+=1
        if(timer_count == 5):
            print("No results found for " + str(zipcode) + ". Program will continue...")
            failed_zips.append(zipcode) # add zip code to list of failed zips...
            return fullData

    # Read downloaded file and checks if it exists
    if os.path.isfile(myfile):
       data = pd.read_csv(myfile)
    else:
        return

    # Adding the date, zipcode, and provider column
    data['date'] = date.today().strftime('%Y-%m-%d')
    data['zipcode'] = zipcode
    data['provider'] = provider

    # Append zip code data to full Dataframe
    fullData = fullData.append(data, ignore_index=True)
    # print(fullData)


    # File operations:
    # If file exists, delete it.
    if os.path.isfile(myfile):
        os.remove(myfile)
    else:
        pass

    # Return our full dataFrame
    return fullData

main()