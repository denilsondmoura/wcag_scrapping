from utils.get_page import use_requests, use_selenium
import re
import time
from bs4 import BeautifulSoup

wcag_url = 'https://www.w3.org/TR/WCAG22/'

def get_page(url):
    return use_requests(url)
    # return use_selenium(url)
        
def get_conformance_level(guideline):
    conformance_level = guideline.find('p', {'class': 'conformance-level'})
    if conformance_level:
        return re.sub(r'\(Level\s*|\)', '', conformance_level.text)
    else:
        return ""
    
def get_secno(guideline):
    secno = guideline.find('bdi', {'class': 'secno'})
    if secno:
        return re.sub(r'\(Guideline\s*|\)', '', secno.text)
    else:
        return ""
    
def get_principle_title(guideline):
    secno = guideline.find('h2')
    if secno:
        return  secno.text
    else:
        return ""

def get_guideline_title(guideline):
    title_h3 = guideline.find('h3')
    if title_h3:
        return  title_h3.text
    else:
        title_h4 = guideline.find('h4')
        
        if title_h4:
            return  title_h4.text
        else:
            return f'{get_secno(guideline)}{guideline.get("id")}' 
    
def is_guideline_relevant(guideline):
    doclinks = guideline.find('div', {'class': 'doclinks'})
    links = doclinks.find_all('a')
    
    for link in links:
        if 'Understanding' in link.text:
            understanding_page = get_page(link.get('href'))
            
            benefits = understanding_page.find('section', {'id': 'benefits'})
            if benefits:
                benefits_li = benefits.find_all('li')
                
                for li in benefits_li:
                    if 'low vision' in li.text or 'blind' in li.text:
                        return True
                    
            else:
                return False
        else:
            return False
 
def is_success_criterion(title):
    if 'Success Criteri' in title:
        return True
    else:
        return False

 
success_criterion_count = 1
wcag_page = get_page(wcag_url)   

if wcag_page:
    principles = wcag_page.find_all('section', {'class': 'principle'})

    for principle in principles:
        principle_title = get_principle_title(principle)
        print(f'{principle_title}')
        
        guidelines = principle.find_all('section', {'class': 'guideline'})
        for guideline in guidelines:
                    
            conformance_level = get_conformance_level(guideline)
            guideline_title = get_guideline_title(guideline)
            is_relevant = is_guideline_relevant(guideline)
            
            if not is_success_criterion(guideline_title) or is_relevant:
                print(f'{guideline_title} ({conformance_level})')
                
            if is_relevant:
                success_criterion_count+=1
                
            time.sleep(2)

    print(f'Total Success Criterion', success_criterion_count)

