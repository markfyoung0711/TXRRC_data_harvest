import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# this program gets the URLs for the dataset section
# next it will make a list of URLs for each of the files section by section

driver = webdriver.Chrome()
driver.get("https://www.rrc.texas.gov/resource-center/research/data-sets-available-for-download/")

# Find the Data Sets H2 element.
h2 = driver.find_element(By.XPATH, "//article/h2[text()='Data Sets']")

td_download_elements = h2.find_elements(By.XPATH, "following-sibling::table/tbody/tr/td[@data-label='Download']")
th_description = h2.find_elements(By.XPATH, "following-sibling::table/tbody/tr/th")
a_elements = [td.find_element(By.XPATH, "span/a") for td in td_download_elements]

data_set_names = [x.text for x in th_description]

download_types = []
for file_type in a_elements:
    file_type_words = file_type.text.split(' ')
    try:
        file_type_words.remove('File')
        file_type_words.remove('Format')
    except Exception as e:
        pass
    download_type = ' '.join(file_type_words)
    download_types.append(download_type)

href_list = [x.get_attribute('href') for x in a_elements]
df = pd.DataFrame(zip(download_types, href_list, data_set_names),
                  columns=['filetype', 'uri', 'dataset_description'])

time_start = time.time()
for uri in list(df['uri']):
    driver.get(uri)
time_end = time.time()
elapsed_sec = str((time_end - time_start) / 60.0)
print(f'time for all pages: in minutes {elapsed_sec}')
