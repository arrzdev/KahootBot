'''
    ANSWER KAHOOT SCRAPER
    DATE: 24/02/2020
    AUTHOR: ARRZ.DEV
'''

#NORMALIZER MODULE
import unidecode

#SELENIUM
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def get(array):
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


        for pergunta in globalContainers:
            pergunta.click()

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
                    unidecode.unidecode(pergunta.find_element_by_class_name("styles__Question-enothq-4").text.lower()).strip().replace('\'', '').replace('"', ''):unidecode.unidecode(resposta_certa.lower()).strip()
                })

            pergunta.click()

    driver.quit()
    return results
