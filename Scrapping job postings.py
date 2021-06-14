from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def remove_chars(sentence):
    chars = ['  ', '\n', '\r']
    sentence = sentence.strip()
    for character in chars:
        sentence = sentence.replace(character, '')
    return sentence
	
def find_jobs():
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
    desc = {'Job Title': [],
            'Company': [],
           'Skills': [],
           'Link': []}

    for job in jobs:
        publish_Date = job.find('span', class_ = 'sim-posted').span.text
        if 'few' in publish_Date:
            company_name = job.find('h3', class_ = 'joblist-comp-name').text
            company_name = remove_chars(company_name)
            job_title = job.find('h2').text
            job_title = remove_chars(job_title)
            skills = job.find('span', class_ = 'srp-skills').text
            skills = remove_chars(skills)
            link = job.h2.a['href']
            desc["Company"].append(company_name)
            desc["Job Title"].append(job_title)
            desc["Skills"].append(skills)
            desc["Link"].append(link)
            if unfamiliar_skills not in skills:
                print(f'''Job Title: {job_title}
                Company: {company_name}
                Skills: {skills}
                Link: {link}
                ''')
            pd.DataFrame(desc).to_csv('First scrapped.csv', index = None)

if __name__ == '__main__':
    unfamiliar_skills = input('Enter Unfamiliar Skills >')
    while True:
        find_jobs()
        wait = 0.5
        print(f'Updating in {wait} minute(s)...')
        time.sleep(wait*60)