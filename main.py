'''
    KAHOOT ANSWER GIVER FROM GOOGLEMEET SCREENSHARE
    DATE: 25/02/2020
    AUTHOR: ARRZ.DEV
'''

#DEFAULT
import os
from os import system
import sys
from time import sleep
import json
import datetime

#NORMALIZER MODULE
import unidecode

#COLORIZED
import colorama

#SELF-MADE MODULES
from modules.db_functions import *
from modules.algorithms import calc_prob

#IMAGING MODULES
import numpy as np
from PIL import ImageGrab, Image
import pytesseract


banner = '''\033[93m
       _  __   _   _  _  ___   ___ _____    ___  ___ _____ 
      | |/ /  /_\ | || |/ _ \ / _ \_   _|__| _ )/ _ \_   _|
      | ' <  / _ \| __ | (_) | (_) || ||___| _ \ (_) || |  
      |_|\_\/_/ \_\_||_|\___/ \___/ |_|    |___/\___/ |_|  
'''


def Display(status=False, question=False, answer=False, probability=False):
    if not question or not answer or not probability:
        question = last_question
        probability = last_probability
        answer = last_answer

    if not status:
        status = last_status

    #CHANGE TITLE
    SetTitle(title=status)

    #PROBABILITY ROUND
    probability = str(probability)[:4]

    #RE-STRUCT
    if len(question) == 0:
        question = ' '*48
    elif len(question) < 46:
        question = f'{question}..{(46-len(question))*" "}'
    else:
        question = f'{question[:46]}..'
    
    if len(answer) == 0:
        answer = ' '*48
    elif len(answer) < 46:
        answer = f'{answer}..{(46-len(answer))*" "}'
    else:
        answer = f'{answer[:46]}..'

    if len(status) < 46:
        status = f'{status}{(46-len(status))*" "}'

    #ROUND PROBABILITY
    if len(str(probability)) == 0:
        probability = ' '*47
    elif str(probability)[:3] == '100':
        probability = f'{str(probability)[:3]}%{" "*43}'
    else:
        probability = f'{str(probability)[:4]}%{" "*42}'


    #CHANGE COLOR CONSOANT STATUS
    if 'running' in status.lower():
        status = f'\033[92m{status}\033[94m'
    else:
        status = f'\033[91m{status}\033[94m'




    ClearWindow()
    print(banner)
    print(f'''\033[94m

      |--------------------------------------------------|
      | \033[93mSTATUS:\033[94m                                          |
      | {status}   |
      |--------------------------------------------------|
    ''')

    print(f'''\033[94m
      |--------------------------------------------------|
      | \033[93mPERGUNTA:\033[94m                                        |
      | \033[92m{question.capitalize()}\033[94m |
      |--------------------------------------------------|
      | \033[93mREPOSTA:\033[94m                                         |
      | \033[92m{answer.capitalize()}\033[94m | 
      |--------------------------------------------------|
      | \033[93mPROBABILIDADE DE ACERTO:\033[94m                         |
      | \033[92m{probability}\033[94m  |
      |--------------------------------------------------|
    ''')
    
def Imaging():
    while True:
        #REAL TIME LOAD COORDS CONFIG
        coords = json.loads(open(f'coords.json').read())

        fullscreen_coords = coords['ingame']
        full_img = np.array(ImageGrab.grab(bbox=(fullscreen_coords['x-off'],fullscreen_coords['y-off'],fullscreen_coords['width'],fullscreen_coords['height'])))

        ingame_coords = coords['ingame']
        question_game_image = np.array(ImageGrab.grab(bbox=(ingame_coords['x-off'],ingame_coords['y-off'],ingame_coords['width'],ingame_coords['height'])))

        loading_coords = coords['loading']
        question_loading_image = np.array(ImageGrab.grab(bbox=(loading_coords['x-off'],loading_coords['y-off'],loading_coords['width'],loading_coords['height'])))

        while Waiting(full_img):
            Imaging()
        
        if not Gaming(question_game_image):
            Gaming(question_loading_image)

def Waiting(image):
    global Flag
    global last_status

    waiting_texts = ['waiting for players', 'join', 'start', 'entre', 'iniciar', 'aguardando jogadores']

    try:
        page_text = (pytesseract.image_to_string(image, lang='eng')).lower()
    except:
        pass


    if any(x in page_text for x in waiting_texts):
        last_status = 'Waiting for game to start'
        Display(status='Waiting for game to start')
        Flag = False
        return True

    else:
        if Flag == False:
            last_status = 'Game Running'
            Display(status='Game Running')
            Flag = True
            return False
        else:
            return False

def Gaming(image):
    global last_answer
    global last_question
    global last_probability

    #GET RAW TEXT FROM IMAGE
    raw_question = unidecode.unidecode((pytesseract.image_to_string(image, lang='eng')).lower()).strip()

    #CLEAN THE QUESTION TEXT
    sliced_question = raw_question.split('\n')
    for slice_ in sliced_question:
        if len(slice_) > 10:
            question = slice_.strip()
            break
        else:
            question = ''

    #LOGIC TO DISPLAY THE ANSWER, PROBABILITY ETC..
    if question != '' and question != last_question:
        #TRY GO GET THE ANSWER IN CASE THE QUESTION MATCH 100%
        try:
            answer = db[question]
            if answer != last_answer:
                #CALL DISPLAY WITH ANSWER
                last_probability = '100'
                Display(question=question, answer=answer, probability='100')
                last_answer = answer
        
        #IF EXCEPTION RUN MEANS THE QUESTION DOESNT MATCH 100% IN DATABASE
        except:
            #RUN ALGORITHM AND GET ANSWER WITH THE BEST FITNESS        
            prob, question = calc_prob(dictionary=db, question=question)

            #SET THE CORRECT ANSWER IF THE PROBABILITY IS GREATER THAN 40% AND THE ANSWER IS DIFFERENT FROM THE ONE THAT IS ALREADY SET
            if prob > 0.4:
                answer = db[question]
                if answer != last_answer:
                    #CALL DISPLAY WITH ANSWER
                    if prob > 1:
                        probability = 100
                    else:
                        probability = prob * 100
                        
                    last_probability = probability
                    Display(question=question, answer=answer, probability=probability)
                    last_answer = answer
            else:
                return False

def SetDB(topic=False):
    global db

    #ARGUMENT NEED TO BE EITHER 'SAVE' OR 'LOAD'

    dbs = [f for f in os.listdir('databases')]

    if '.json' not in topic:
        topic = f'{topic}.json'

    #LOGIC IF ARGUMENT EQUALS TO 'SAVE'
    if topic not in dbs:
        #GET THE KAHOOT LINKS 
        raw_topic = topic.replace('.json', '')

        Display(status='Getting Links')
        top_links = get_links(topic=raw_topic)

        Display(status=f'Building Database of {raw_topic}')
        db = get_answers(top_links)

        #SAVE THE DATE IN THE FILE SPECIFIED EARLIER
        with open(f'databases/{topic}', 'w') as f:
            f.write(str(db))

    
    #LOGIC IF ARGUMENT EQUALS TO 'LOAD'
    else:
        #LOAD THE DB FROM THE FILE SPECIFIED EARLIER
        Display(status='Loading Database')
        db = json.loads(open(f'databases/{topic}').read().replace('\'', '"'))

    
def SetTitle(title=False):
    if not title:
        return 'you need to specify a title' 

    system(f'title "{title}"')

def ClearWindow():
    if sys.platform.startswith('linux'):
        system('clear')
    else:
        system('cls')

def SetWindow():
    #SET HEIGHT AND WIDTH
    system('mode con:cols=65 lines=30')

    #CALL DISPLAY FUNCTION
    Display(status='Getting user topic input')
    






if __name__ == '__main__':
    #INIT COLORAMA AUTO-RESET
    colorama.init(autoreset=True)

    #INIT GLOBAL VARAIBLES
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    Flag = False
    last_question = ''
    last_answer = ''
    last_status = ''
    last_probability = ''
    db = None

    #SET WINDOW
    SetWindow()
    
    #SET DB BY SCRAPING OR LOADING
    SetDB(topic=str(input('       Topico: ')))

    #START THE MAIN FUNCTION
    Imaging()

    #for f in os.listdir('dictio'): print(f)
    
