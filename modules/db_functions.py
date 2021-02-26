'''
    ANSWER KAHOOT SCRAPER
    DATE: 24/02/2020
    AUTHOR: ARRZ.DEV
'''

#NORMALIZER MODULE
import unidecode
from time import sleep

#SELENIUM
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

usern = 'kahoot.bot.resolver@gmail.com'
passw = 'kahootbotpost'

def get_answers(array):
    results = {}
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    for url in array:
        #GET PAGE
        driver.get(url)
        #WAIT PAGE LOAD
        wait = WebDriverWait(driver, 1)
        while True:
            try:
                t = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'kahoot-logo-svg__KahootLogoSVG-r8i26f-0')))
                break
            except:
                pass


        globalContainers = driver.find_elements_by_class_name('styles__Group-enothq-1')


        for question in globalContainers:
            question.click()

            respostas_container = driver.find_elements_by_class_name('styles__Choices-enothq-12')

            for i in range(len(respostas_container)):
                icon_containers = respostas_container[i].find_elements_by_class_name('styles__IconWrapper-enothq-17')
                for i in range(1,len(icon_containers),2):
                    try: 
                        icon_containers[i].find_element_by_id('correct-icon')
                        resposta_certa = driver.find_elements_by_class_name('styles__Choice-enothq-13')[int((i+1)/2)-1].find_element_by_class_name('styles__Answer-enothq-16').text
                        break
                    except:
                        pass


                results.update({
                    unidecode.unidecode(question.find_element_by_class_name("styles__Question-enothq-4").text.lower()).strip().replace('\'', '').replace('"', ''):unidecode.unidecode(resposta_certa.lower()).strip().replace('\'', '').replace('"', '')
                })

            question.click()

    driver.quit()
    return results

def get_links(topic=False, language='pt', quantity=6):
    if not topic:
        return 'You need to specify a topic'

    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    if language == 'pt':
        url = f'https://create.kahoot.it/search?query={topic}&usage=teacher&language=Portugu%C3%AAs'
    else:
        url = f'https://create.kahoot.it/search?query={topic}&language=English'

    driver.get(url)

    #WAIT FOR PAGE TO LOAD
    wait = WebDriverWait(driver, 1)
    while True:
        try:
            t = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'card__WideCardTitle-sc-1rk0phi-3')))
            break
        except:
           pass
    
    #LOGIN
    driver.find_element_by_id('username').send_keys(usern)
    driver.find_element_by_id('password').send_keys(passw)
    driver.find_element_by_class_name('button__Button-c6mvr2-0').submit()

    #WAIT FOR NEW PAGE TO LOAD
    wait = WebDriverWait(driver, 1)
    while True:
        try:
            t = wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'styles__Label-sc-810hdv-5')))
            break
        except:
           pass
           
    sleep(3)
    containers = driver.find_elements_by_class_name('styles__Title-sc-19d0ynv-6')


    results = []
    for i in range(quantity):
        results.append(containers[i].get_attribute('href'))

    driver.quit()
    return results
        

