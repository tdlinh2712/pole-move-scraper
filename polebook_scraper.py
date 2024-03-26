import csv
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

from dataclasses import PoleMove

web_url = 'https://polemovebook.com/'
response = requests.get(web_url)

driver = webdriver.Chrome('/Users/linh.eiii/Downloads/chromedriver-mac-arm64/chromedriver')
driver.get(web_url)


try:
    while True:
        clickable = driver.find_element_by_id("morebutton")
        clickable.click()
        #wait to load
        time.sleep(10)
except Exception:
    print("QUITTING!")
    pass

img_elems = driver.find_elements_by_xpath('//img[@class="moveImgClass"]')
move_name_elems = driver.find_elements_by_xpath('//span[@class="moveNameClass"]')
level_elems = driver.find_elements_by_xpath('//span[@class="moveDiffClass"]')

print(len(img_elems), len(move_name_elems), len(level_elems))
moves_list = []
for i in range(len(img_elems)):
    img_src = img_elems[i].get_attribute("src")
    name = move_name_elems[i].text
    difficulty = level_elems[i].text
    moves_list.append(PoleMove(name, img_src, difficulty))


print("Fetched moves: ", len(moves_list))

def write2csv(listOfEntries: list, file_name: str):
    with open(file_name, "w") as fileObj:
        writer = csv.writer(fileObj)
        writer.writerow(listOfEntries[0].toHeader())
        for item in listOfEntries:
            writer.writerow(item.toIterable())

file_name = "pole_moves.csv"
write2csv(moves_list, file_name)
print(f"Pole db wrote to {file_name}")
# for move in moves_list:
#     print(move.name)

#print(response.text)