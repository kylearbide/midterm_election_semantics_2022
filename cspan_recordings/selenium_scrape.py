from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime

class videoTranscipt():
    def __init__(self, video_text, date, last_aired, link):
        self.text = video_text
        self.date = date
        self.last_aired = last_aired
        self.location = link 

name = "Marco Rubio"
url = "https://www.c-span.org/search/?searchtype=People&sort=Most+Recent+Airing&text=0"
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path = "./chromedriver.exe")
driver.get(url)

search_bar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@class="add-search-keyword"]'))
    )

search_bar.send_keys(name)
search_bar.send_keys(Keys.RETURN)

profile_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[@class="name"]'))
    )

profile_button.click()

all_videos_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//section[@class="video stack tower"]//a[@class="all-videos"]'))
    )

all_videos_button.click()

recent_videos = driver.find_elements(By.XPATH, '//a[@class="title"]')
dates = driver.find_elements(By.XPATH, '//span[@class="time"]//time')
dates = [date.get_attribute("datetime") for date in dates] 
output_dict = {}

for ix in range(len(recent_videos)):
    output_list = []
    if datetime.strptime(dates[ix*2], "%Y-%m-%d") >= datetime.strptime("2022-02-01", "%Y-%m-%d"):
        speech_text = []

        clickable_video = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@class="title"]'))
        )
        recent_videos = driver.find_elements(By.XPATH, '//a[@class="title"]')
        video = recent_videos[ix]

        video.click()

        try:
            speaker_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, ' //div[@class="dropdown scrollable"]'))
            )
        except:
            speaker_dropdown = driver.find_elements(By.XPATH, ' //div[@class="dropdown"]')[1]

        speaker_dropdown.click()
        if len(speaker_dropdown.find_elements(By.XPATH, '//li')) > 1:
            speaker = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,  f'//li[text()="{name}"]')))
            speaker.click()

            try:
                show_fulls = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@class="link-show-full-text"]'))
                )
                speech_exists = True
            except:
                speech_exists = False
                print("No Identifiable Speech")
            
            if speech_exists:
                show_fulls = driver.find_elements(By.XPATH, '//span[@class="link-show-full-text"]')
                for expand in show_fulls:
                    expand.click()

                transcripts = driver.find_elements(By.XPATH, '//p[@class="short_transcript"]')
                for transcript in transcripts:
                    speech_chunk = [line.text for line in transcript.find_elements(By.TAG_NAME, "a")]
                    speech_text.append(" ".join(speech_chunk))
                    output = videoTranscipt(speech_text, dates[ix*1], dates[ix*2 + 1], driver.current_url)
            
        else:
            show_fulls = driver.find_elements(By.XPATH, '//span[@class="link-show-full-text"]')
            for expand in show_fulls:
                    expand.click()

            transcripts = driver.find_elements(By.XPATH, '//p[@class="short_transcript"]')
            if len(transcripts) > 0:
                for transcript in transcripts:
                    speech_chunk = [line.text for line in transcript.find_elements(By.TAG_NAME, "a")]
                    speech_text.append(" ".join(speech_chunk))
                    output = videoTranscipt(speech_text, dates[ix*1], dates[ix*2 + 1])

        if speech_exists:
            output_list.append(output)

        driver.back()

    else:
        break

output_dict.update({name:output_list})

driver.quit()

print(output_dict[name])
