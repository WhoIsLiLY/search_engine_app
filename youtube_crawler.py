import requests as rq #library to make requests to a website
from selenium import webdriver

wd = webdriver.Chrome() #Initializes the Chrome webdriver with the configured options

from selenium.webdriver.common.by import By #By class is used to locate elements within a document.

page = rq.get('https://www.youtube.com/results?search_query=blackpink') 
#print(page.status_code)

wd.get("https://www.youtube.com/results?search_query=blackpink") #get html structure from kompas.com page

i=0
for news in wd.find_elements(By.CSS_SELECTOR,'ytd-video-renderer.style-scope'):
  if(i>10): break
  else:
    print(i, "<br>")
    title = news.find_element(By.CSS_SELECTOR,'yt-formatted-string.style-scope').text
    # cat = news.find_element(By.CSS_SELECTOR,'a.articles--iridescent-list--text-item__category').text
    # link = news.find_element(By.CSS_SELECTOR,'a.articles--iridescent-list--text-item__title-link').get_attribute("href")
    # img = news.find_element(By.CSS_SELECTOR,'img.articles--iridescent-list--text-item__figure-image-lazyload').get_attribute("data-src")
    
    # print("<tr>")
    # print("<td><img src='",img,"' width='150' height='100'></td>")
    # print("<td>",cat,"</td>")
    # print("<td><a href='",link,"'>",title,"</a></td>")
    # print("</tr>")
    print(title, "<br>")
  i+=1