import datetime, random, time, os, csv 
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

#create empty file
data0 = [] 
data0.append({  "container_number": 1,
                "Type": 1,
                "port_of_loading_location": 1,
                "port_of_loading_date": 1,
                "port_of_transhipment_location": 1,
                "port_of_transhipment_date": 1,
                "port_of_discharge_location": 1,
                "port_of_discharge_location_date": 1, 
            })
df = pd.DataFrame(data0[:])
path = os.path.join(os.getcwd(),"scrapes","zim_cnt_detail_01.csv")
df.to_csv(path)

# headless browser
options = Options()
#options.add_argument('--headless')

# settings for time capturing capabilities.  
datetime.datetime.now()
datetime.datetime(2009, 1, 6, 15, 8, 24)
start_time = datetime.datetime.now()
print(f'\n  CargoFax Container Crawl')

# set how the range for my wait times between actions. 
wait_time = random.randrange(10, 15)
#print(f'\n     Saved wait: {wait_time}')

# website URL
base_url = "https://www.zim.com/tools/track-a-shipment"
print("\n     1.Directing to site")

# firefox session
# to improve this scraper, eventually we will need the ability to...
# disguising requests by rotating IPs or Proxy Services, randomize script patterns & wait times,...
# rotate user agents, webdrivers, maybe headless drivers, etc.   
driver = webdriver.Firefox(options=options)
driver.get(base_url) 
#driver.implicitly_wait(wait_time)

# wait for initial pop up and close it out
print("     2.Site Reached")
time.sleep(wait_time) #seconds, needed to load popup
pop_up_x = driver.find_element_by_xpath('.//*[@title="I Agree"]').click()


# LOOP HERE
data = []
# shipping line data to pull
shipping_line = "ZIM"
# file path to data
df = pd.read_csv(os.path.join(os.getcwd(),"output","01_cnt_num_all_scrape.csv"))
# select only relevant columns, clean data, search for relevant contianers, and make into a list 
df1 = df[['ctn_reference', 'filename']]
df2 = df1.dropna()
df3 = df2[df2['filename'].str.contains(shipping_line)]
df4 = df3['ctn_reference'].tolist()
containers = df4
#containers = ['SUDU6556254', 'MRKU9967192', 'SUDU6738264', 'MRKU9967192']

time.sleep(wait_time) #seconds, needed to load
print("     3.Scrape Initiated")
print("records to scrape = " + str(len(containers)))

for container in containers[:2]:
    driver.find_element_by_xpath('.//*[@name="consnumber"]').send_keys(container) #input container number
    driver.find_element_by_xpath('.//*[@value="Track Shipment"]').click() #click Search
    time.sleep(wait_time) #seconds, needed to load
 
    try :     
        container_type = driver.find_element_by_xpath('.//*[@class="dl-inline"]/dd')   
        if container_type.is_displayed():   
            container_type = driver.find_element_by_xpath('.//*[@class="dl-inline"]/dd').text
    except NoSuchElementException :
        container_type = "n/a" 



    try :     
        port_of_loading_location = driver.find_element_by_xpath('.//td[contains(text(),"Port of Loading")]/../td')  
        if port_of_loading_location.is_displayed():   
            port_of_loading_location = driver.find_elements_by_xpath('.//td[contains(text(),"Port of Loading")]/../td')[1].text
    except NoSuchElementException :
        port_of_loading_location = "n/a"

    try :     
        port_of_transhipment_location = driver.find_element_by_xpath('.//td[contains(text(),"Transshipment Port to Port of Discharge")]/../td')  
        if port_of_transhipment_location.is_displayed():   
            port_of_transhipment_location = driver.find_elements_by_xpath('.//td[contains(text(),"Transshipment Port to Port of Discharge")]/../td')[1].text
    except NoSuchElementException :
        port_of_transhipment_location = "n/a"        

    try :     
        port_of_discharge_location = driver.find_element_by_xpath('.//td[contains(text(),"arrival to Port of Discharge")]/../td') 
        if port_of_discharge_location.is_displayed():   
            port_of_discharge_location = driver.find_elements_by_xpath('.//td[contains(text(),"arrival to Port of Discharge")]/../td')[1].text
    except NoSuchElementException :
        port_of_discharge_location = "n/a"



    try :     
        port_of_loading_date = driver.find_element_by_xpath('.//td[contains(text(),"Port of Loading")]/../td')
        if port_of_loading_date.is_displayed():   
            port_of_loading_date = driver.find_elements_by_xpath('.//td[contains(text(),"Port of Loading")]/../td')[2].text
    except NoSuchElementException :
        port_of_loading_date = "n/a"

    try :     
        port_of_transhipment_date = driver.find_element_by_xpath('.//td[contains(text(),"Transshipment Port to Port of Discharge")]/../td')  
        if port_of_transhipment_date.is_displayed():   
            port_of_transhipment_date = driver.find_elements_by_xpath('.//td[contains(text(),"Transshipment Port to Port of Discharge")]/../td')[2].text
    except NoSuchElementException :
        port_of_transhipment_date = "n/a"    

    try :     
        port_of_discharge_location_date = driver.find_element_by_xpath('.//td[contains(text(),"arrival to Port of Discharge")]/../td')
        if port_of_discharge_location_date.is_displayed():   
            port_of_discharge_location_date = driver.find_elements_by_xpath('.//td[contains(text(),"arrival to Port of Discharge")]/../td')[2].text
    except NoSuchElementException :
        port_of_discharge_location_date = "n/a"        

    # append data 
    data.append({   "container_number": container,
                    "Type": container_type,

                    "port_of_loading_location": port_of_loading_location,
                    "port_of_loading_date": port_of_loading_date,
                    
                    "port_of_transhipment_location": port_of_transhipment_location,
                    "port_of_transhipment_date": port_of_transhipment_date,
                    
                    "port_of_discharge_location": port_of_discharge_location,
                    "port_of_discharge_location_date": port_of_discharge_location_date, 
                })
                
    print(f"       Completed:{container}")
    df = pd.DataFrame(data)
    df.to_csv(path, mode='a', header=False)               
    data =[]      
    #time.sleep(random.randrange(6, 8))
    #driver.back()
    #driver.find_element_by_xpath('.//*[@name="consnumber"]').clear() #clear search bar

    try :     
        error_check = driver.find_element_by_xpath('.//*[@name="consnumber"]')  
        if error_check.is_displayed():   
            driver.find_element_by_xpath('.//*[@name="consnumber"]').clear()
    except NoSuchElementException :
        driver.back()
        time.sleep(wait_time)
        driver.find_element_by_xpath('.//*[@name="consnumber"]').clear()
    
# save loop data to pandas dataframe
#       df = pd.DataFrame(data[:])

# save the df to the  folder path 
#       path = os.path.join(os.getcwd(),"scrapes","zim_cnt_detail.csv")
#       df.to_csv(path)

# close driver
print("     4.File saved to computer")
print("records scraped = " + str(len(containers)))
driver.quit()

# outro 
print(f'\n   Thank you for choosing CargoFax :)')
print(f'\n Project start time: {start_time}')
print(f' Project end time  : {datetime.datetime.now()}')
print(f' Time to Complete  : {datetime.datetime.now()-start_time}')          

