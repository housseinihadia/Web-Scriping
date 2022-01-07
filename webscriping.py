#1st step install and import modules 
#pip/pip3 install lxml
#pip/pip3 install requests
#pip/pip3 install beautifulsoup4

import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title=[]
company_name=[]
location_name=[]
skills=[]
links=[]
salary=[]
responsibilities=[]
date=[]
page_num=0

while True:
    #2nd step use requests to fetch the url
    try:
        result=requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}")
        #3rd step save page content/markup
        src=result.content
        #4th step creat soup object to pares content
        soup=BeautifulSoup(src,"lxml")
        
        page_limit=int(soup.find("strong").text)
        if(page_num > page_limit // 15):
            print("page end")
            break
        
        #5th step find the elements containig info we need
        #--jobtitles, job skills, company names , location names 
        job_titles=soup.find_all("h2",{"class":"css-m604qf"})
        company_names=soup.find_all("a",{"class":"css-17s97q8"})
        locations_names=soup.find_all("span",{"class":"css-5wys0k"})
        job_skills=soup.find_all("div",{"class":"css-y4udm8"})
        posted_new=soup.find_all("div",{"class":"css-4c4ojb"})
        posted_old=soup.find_all("div",{"class":"css-do6t5g"})
        posted=[*posted_new,*posted_old]

        #6th step loop over returned lists to extract needed info into other lists
        for i in range(len(job_titles)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text)
            location_name.append(locations_names[i].text)
            skills.append(job_skills[i].text)
            date_text=posted[i].text.replace("-","").strip()
            date.append(posted[i].text)
        page_num += 1
        print("page switched")
    except:
        print("error occured")
        break
    
for link in links:
    result=requests.get(link)
    src=result.content
    soup=BeautifulSoup(src,"lxml")
    #salaries=soup.find("div",{"class":"matching-requirement-icon-container","data-toggle":"tooltip","data-placement":"top"})
    #salary.append(salaries.text().strip())
    #requirments=soup.find("span",{"itemprop":"responsibilities"}).ul
    respon_text=""
   # for li in requirments.find_all("li"):
    #    respon_text +=li.text + "| "

    respon_text=respon_text[:-2]    
    responsibilities.append(respon_text) 

#7th step creat csv file and fill it with values
file_list=([job_title,company_name,date,location_name,skills,links,salary,responsibilities])
exported=zip_longest(*file_list)

with open ("F:\Ai-regression\web scriping\job.csv","w",encoding="utf-8")as myfile:
    wr=csv.writer(myfile)
    wr.writerow(["job_title","company_name","date","location","skills","links","salary","responsibilites"])
    wr.writerows(exported)

#8th step to fetch the link of the job and fetch in page details
#--- salary , job requirements
#9th step is to do the above for all pages


#10th step is to optimize code and clean data
