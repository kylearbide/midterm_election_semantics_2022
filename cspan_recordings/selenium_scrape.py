from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json
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

def pull_transcripts(name:str):
    url = "https://www.c-span.org/search/?searchtype=People&sort=Most+Recent+Airing&text=0"
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_argument('headless')
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

    show_100 = driver.find_element(By.XPATH, '//a[@id="search-results-limit-100"]')
    show_100.click()

    recent_videos = driver.find_elements(By.XPATH, '//a[@class="title"]')
    dates = driver.find_elements(By.XPATH, '//span[@class="time"]//time')
    dates = [date.get_attribute("datetime") for date in dates] 
    output_list = []
    for ix in range(len(recent_videos)):
        if datetime.strptime(dates[ix*2], "%Y-%m-%d") >= datetime.strptime("2021-02-01", "%Y-%m-%d"):
            speech_text = []

            clickable_video = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@class="title"]'))
            )
            recent_videos = driver.find_elements(By.XPATH, '//a[@class="title"]')
            video = recent_videos[ix]

            video.click()

            try:
                speaker_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="dropdown scrollable"]'))
                )
                dropdown_len =  len(driver.find_elements(By.XPATH,'//div[@class="dropdown scrollable"]//li'))
            except:
                speaker_dropdown = driver.find_elements(By.XPATH, ' //div[@class="dropdown"]')[1]
                dropdown_len = len(driver.find_elements(By.XPATH,'//div[@class="dropdown"]//li')) - 3

            speaker_dropdown.click()

            print(dropdown_len)
            if dropdown_len > 2:
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
                        speech_chunk = [line.text.replace("Show Less Text", "") for line in transcript.find_elements(By.TAG_NAME, "a")]
                        speech_text.append(" ".join(speech_chunk))
                        output = videoTranscipt(speech_text, dates[ix*1], dates[ix*2 + 1], driver.current_url)
                
            else:
                show_fulls = driver.find_elements(By.XPATH, '//span[@class="link-show-full-text"]')
                for expand in show_fulls:
                        expand.click()

                transcripts = driver.find_elements(By.XPATH, '//p[@class="short_transcript"]')
                if len(transcripts) > 0:
                    speech_exists = True
                    for transcript in transcripts:
                        speech_chunk = [line.text.replace("Show Less Text", "") for line in transcript.find_elements(By.TAG_NAME, "a")]
                        speech_text.append(" ".join(speech_chunk))
                        output = videoTranscipt(speech_text, dates[ix*1], dates[ix*2 + 1], driver.current_url)
                else:
                    speech_exists = False
            if not speech_exists:
                type_dropdown = driver.find_elements(By.XPATH, ' //div[@class="dropdown"]')[0]
                type_dropdown.click()

                graph_line = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,  f'//li[text()="Graphical Timeline"]')))
                graph_line.click()

                time.sleep(5)
                graph_transcripts = driver.find_elements(By.XPATH, '//area[@class  = "app transcript-time-seek"]')
                # [print((" " + block.get_attribute("title").split(r'<br>',1)[0]).rsplit(' ',1)[1]) for block in graph_transcripts]
                speaker_times = [block.get_attribute("title").split("<font size=2>",1)[1].split(" (Length",1)[0] for block in graph_transcripts if (" " + block.get_attribute("title").split(r'<br>',1)[0]).rsplit(' ',1)[1].upper() == name.rsplit(" ",1)[1].upper()]
                print(speaker_times)

                if speaker_times:
                    speech_exists = True
                    move_mouse = driver.find_element(By.XPATH, '//label[text()="Search this text"]')
                    move_mouse.click()

                    type_dropdown.click()
                    text_line = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,  f'//li[text()="Text"]')))
                    text_line.click()

                    speaker_dropdown.click()

                    speaker = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,  f'//li[text()="All Speakers"]')))
                    speaker.click()

                    show_fulls = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//span[@class="link-show-full-text"]'))
                    )
                    show_fulls = driver.find_elements(By.XPATH, '//span[@class="link-show-full-text"]')
                    for expand in show_fulls:
                        expand.click()

                    for speaker_time in speaker_times:
                        table_row = driver.find_element(By.XPATH, f"//tr[th//text()[contains(., '{speaker_time}')]]")
                        speech_chunk = [line.text.replace("Show Less Text", "") for line in table_row.find_elements(By.TAG_NAME, "a") if line.text]
                        speech_text.append(" ".join(speech_chunk))
                        output = videoTranscipt(speech_text, dates[ix*1], dates[ix*2 + 1], driver.current_url)

            if speech_exists:
                output_list.append({"text":output.text,"date":output.date,"last_aired":output.last_aired,"link":output.link})

            
            driver.back()

        else:
            break

    output_dict = ({"name":name, "output":output_list})

    driver.quit()

    print(output_dict)
    return(output_dict)

with open("../candidates_dict.json","r") as f:
    candidates_dict = json.load(f)

all_transcripts = []
errors_output = []
ix = 0

for candidate in candidates_dict:
    try:
        candidate_output = pull_transcripts(candidate['Name'])
        all_transcripts.append(candidate_output)
    except:
        print(f"unknown error for {candidate['Name']}")
        ix += 1
        errors_output.append({candidate['Name']: ix})

with open("../cspan_output.json","w") as f:
    json.dump(all_transcripts,f)

with open("../error.json","w") as f:
    json.dump(errors_output,f)