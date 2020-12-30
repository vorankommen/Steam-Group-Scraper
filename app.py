import requests
from bs4 import BeautifulSoup
import concurrent.futures
import threading
import time

gid = int(input("Enter the start gid: "))  # stard gid
gid2 = int(input("Enter the end gid: "))  # end gid
workers = int(input("Threads: "))  # threading
if(gid > gid2):  # error handling
    print("Error start gid is greater than end gid")
    exit()
gid2 += 1
of = gid  # needed for the time check at the end
f = open("groups.txt", "w+", encoding='utf-8')
start = time.time()

# creating list for the threading method
list = []
x = gid
while(x < gid2):
    list.append("https://steamcommunity.com/gid/" + str(x))
    x += 1


def check(url):
    global r
    global soupz
    global gid
    r = requests.get(str(url))
    soupz = BeautifulSoup(r.content, 'html.parser')
    if soupz.find("body", {"class": "flat_page responsive_page"}):
        scrape(url)
    print(gid)
    gid += 1


def scrape(url):
    name = soupz.find(class_='grouppage_header_name').get_text().strip()
    date = soupz.find(class_='data').get_text().strip()
    members = soupz.find(class_='count').get_text().strip()
    f.write(url + "\n")
    f.write("Name Tag: " + name + "\n")
    f.write("Date: " + date + "\n")
    f.write("Members: " + members + "\n")
    f.write('\n')


with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
    executor.map(check, list)

end = time.time()
print(
    f"Runtime of the program is {end - start} sec, scraped groups: {gid2 - of}")
