import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import xlsxwriter
import pandas as pd

# Provide the URL of the channel whose data you want to fetch
urls = [
    'https://www.youtube.com/c/GeeksforGeeksVideos/videos'
]

# Define Chrome options
options = webdriver.ChromeOptions()

# Create a new instance of the browser driver
driver = webdriver.Chrome(options=options)

for url in urls:
    times = 0  # Reset times for each URL
    driver.get(f'{url}/videos?view=0&sort=p&flow=grid')
    
    while times < 5:
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        times += 1
        
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'lxml')

    # Title
    titles = soup.findAll('a', id='video-title')
    t = []
    for i in titles:
        t.append(i.text.strip())  # Strip leading/trailing whitespace

    # Debug: Print the titles to check if they are being captured
    print("Titles:", t)

    # Views
    views = soup.findAll('span', class_='style-scope ytd-grid-video-renderer')
    v = []
    for i in range(len(views)):
        if i % 2 == 0:
            v.append(views[i].text.strip())  # Strip leading/trailing whitespace
        else:
            continue

    # Debug: Print the views to check if they are being captured
    print("Views:", v)

    # Duration
    duration = soup.findAll('span', class_='style-scope ytd-thumbnail-overlay-time-status-renderer')
    d = []
    for i in duration:
        d.append(i.text.strip())  # Strip leading/trailing whitespace

    # Debug: Print the durations to check if they are being captured
    print("Durations:", d)

    # Write to Excel file
    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write(0, 0, "Title")
    worksheet.write(0, 1, "Views")
    worksheet.write(0, 2, "Duration")

    row = 1
    for title, view, dura in zip(t, v, d):
        worksheet.write(row, 0, title)
        worksheet.write(row, 1, view)
        worksheet.write(row, 2, dura)
        row += 1

    workbook.close()

driver.quit()

# Read and display data from Excel file
data = pd.read_excel('output.xlsx')
print(data.head())
