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
from threading import Thread
import win32api, win32con
from ctypes import *

#NORMALIZER MODULE
import unidecode

#COLORIZED
import colorama

#SELF-MADE MODULES
from modules.db_management import *
from modules.algorithms import *

#IMAGING MODULES
import numpy as np
from PIL import ImageGrab, Image, ImageOps, ImageFilter
import pytesseract


# --SETTINGS--
autop = True

banner = '''\033[93m
       _  __   _   _  _  ___   ___ _____    ___  ___ _____ 
      | |/ /  /_\ | || |/ _ \ / _ \_   _|__| _ )/ _ \_   _|
      | ' <  / _ \| __ | (_) | (_) || ||___| _ \ (_) || |  
      |_|\_\/_/ \_\_||_|\___/ \___/ |_|    |___/\___/ |_|  
'''


#SET FUNCTIONS
def SetTitle(title=False):
    if not title:
        return 'you need to specify a title' 

    system(f'title "{title}"')

def SetWindow():
    #SET HEIGHT AND WIDTH
    system('mode con:cols=65 lines=35')

    #CALL DISPLAY FUNCTION
    Display(status='Getting user topic input')

def SetDB(topic=False):
    global db

    #ARGUMENT NEED TO BE EITHER 'SAVE' OR 'LOAD'

    dbs = [f for f in os.listdir('databases')]

    if '.json' not in topic:
        topic = f'{topic}.json'

    #LOGIC IF ARGUMENT EQUALS TO 'SAVE'
    if topic not in dbs:
        #GET LANGUAGE
        language = str(input('       Language (pt or en): '))

        #GET THE KAHOOT LINKS 
        raw_topic = topic.replace('.json', '')

        Display(status='Getting Links')
        top_links = get_links(topic=raw_topic, language=language)

        Display(status=f'Building Database of {raw_topic}')
        db = create_db(top_links)

        #SAVE THE DATE IN THE FILE SPECIFIED EARLIER
        with open(f'databases/{topic}', 'w') as f:
            f.write(str(db))

    
    #LOGIC IF ARGUMENT EQUALS TO 'LOAD'
    else:
        #LOAD THE DB FROM THE FILE SPECIFIED EARLIER
        Display(status='Loading Database')
        db = json.loads(open(f'databases/{topic}').read().replace('\'', '"'))


#INFORMATION PROCESSMENT FUNCTIONS
def Imaging():
    while True:
        #REAL TIME LOAD COORDS CONFIG
        coords = json.loads(open(f'coords.json').read())

        fullscreen_coords = coords['ingame']
        full_img = np.array(FilterImage(ImageGrab.grab(bbox=(fullscreen_coords['x-off'],fullscreen_coords['y-off'],fullscreen_coords['width'],fullscreen_coords['height']))))

        question_game_image = np.array(FilterImage(ImageGrab.grab(bbox=(fullscreen_coords['x-off'],fullscreen_coords['y-off']+5,fullscreen_coords['width'],400))))

        question_loading_image = np.array(FilterImage(ImageGrab.grab(bbox=(fullscreen_coords['x-off'],fullscreen_coords['y-off']+200,fullscreen_coords['width'],625))))

        #cv2.imshow('aa',  full_img)
        #cv2.imshow('bb',  question_game_image)
        #cv2.imshow('cc',  question_loading_image)

        while Waiting(full_img):
            Imaging()
        
        #GET RESPONSE FROM THE FUNCTION
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

    #CLEAN RAW QUESTION
    question = CleanRaw(raw_question)

    #LOGIC TO DISPLAY THE ANSWER, PROBABILITY ETC..
    if question != '' and question != last_question:
        #TRY GO GET THE ANSWER IN CASE THE QUESTION MATCH 100%
        try:
            answer = db[question]
            if answer != last_answer:
                #CALL DISPLAY WITH ANSWER
                last_probability = '100'
                last_answer = answer
                last_question = question
                Display(question=question, answer=answer, probability='100')

                #RUN AUTO PLAY IF THATS ON
                if autop:
                    #RUN AUTOPLAY
                    pass
                    
        
        #IF EXCEPTION RUN MEANS THE QUESTION DOESNT MATCH 100% IN DATABASE
        except:
            #RUN ALGORITHM AND GET ANSWER WITH THE BEST FITNESS        
            prob, question = identify_question(dictionary=db, question=question)

            #SET THE CORRECT ANSWER IF THE PROBABILITY IS GREATER THAN 40% AND THE ANSWER IS DIFFERENT FROM THE ONE THAT IS ALREADY SET
            if prob > 0.4:
                answer = db[question]
                if answer != last_answer:
                    #CALL DISPLAY WITH ANSWER
                    if prob > 1:
                        probability = 100
                    else:
                        probability = prob * 100
                        
                    last_answer = answer
                    last_question = question
                    last_probability = probability
                    Display(question=question, answer=answer, probability=probability)

            else:
                return False

def AutoPlay():
    last_action = ''

    def click(x,y):
        #BLOCKING USER INPUT 
        windll.user32.BlockInput(True)
        
        #MOVE CURSOR TO THE POSITION
        win32api.SetCursorPos((x,y))
        
        #PERFORM A CLICK 2 TIMES
        for i in range(2):
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            sleep(0.02) #This pauses the script for 0.02 seconds
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        
        #MOVE THE MOUSE TO THE MIDDLE OF THE BUTTONS
        win32api.SetCursorPos((1425,215))

        #ENABLE USER INPUT
        windll.user32.BlockInput(False)

    while True:
        coords = json.loads(open(f'coords.json').read())

        if any(last_answer == x for x in ['verdadeira', 'falsa', 'true', 'false', 'falso', 'verdadeiro']):
            #['verdadeiro', 'falso', 'true', 'false']
            fiftyfifty_left = coords['answer_5050_left']
            fiftyfifty_right = coords['answer_5050_right']

            fiftyfifty_left_btn = np.array(FilterImage(ImageGrab.grab(bbox=(fiftyfifty_left['x-off'],fiftyfifty_left['y-off'],fiftyfifty_left['width'],fiftyfifty_left['height']))))

            fiftyfifty_right_btn = np.array(FilterImage(ImageGrab.grab(bbox=(fiftyfifty_right['x-off'],fiftyfifty_right['y-off'],fiftyfifty_right['width'],fiftyfifty_right['height']))))
            
            raw_array = [fiftyfifty_left_btn, fiftyfifty_right_btn]

            #GET TEXT, CLEAN IT, AND ADD IT TO A CLEAN ARRAY
            clean_array = []
            for button in raw_array:
                raw_answer = unidecode.unidecode((pytesseract.image_to_string(button, lang='eng')).lower()).strip()
                clean_array.append(raw_answer)

            #CHECK SO WE DONT REPEAT THE SAME CLICK ACTION AS BEFORE
            if last_answer != last_action:

                #GET THE INDEX OF THE ANSWER
                algo_response = identify_answer_index(answer=last_answer, dictionary=clean_array)

                #IF a != False and probability > 0
                if algo_response:
                    if algo_response[0] > 0:
                        Display(lurdes_status='Let me help you!')

                        #OVERWRITE THE LAST ACTION WITH THE NEW ANSWER ACTION
                        last_action = last_answer

                        #DEFINE INDEX OF THE ANSWER
                        index = algo_response[1]

                        if index == 0:
                            click(coords["player_5050_left"]["x-off"], coords["player_5050_left"]["y-off"])
                            button = 'left'
                        elif index == 1:
                            click(coords["player_5050_right"]["x-off"], coords["player_5050_right"]["y-off"])
                            button = 'right'


                        sleep(1)
                        Display(lurdes_status=f'Clicked the {button} button ({last_answer})')
        else:
            #button_cords
            top_left = coords['answer_top_left']
            top_right = coords['answer_top_right']
            bottom_right = coords['answer_bottom_right']
            bottom_left = coords['answer_bottom_left']

            #BUTTONS IMAGE
            top_left_btn = np.array(FilterImage(ImageGrab.grab(bbox=(top_left['x-off'],top_left['y-off'],top_left['width'],top_left['height']))))
            top_right_btn = np.array(FilterImage(ImageGrab.grab(bbox=(top_right['x-off'],top_right['y-off'],top_right['width'],top_right['height']))))
            bottom_left_btn = np.array(FilterImage(ImageGrab.grab(bbox=(bottom_left['x-off'],bottom_left['y-off'],bottom_left['width'],bottom_left['height']))))
            bottom_right_btn = np.array(FilterImage(ImageGrab.grab(bbox=(bottom_right['x-off'],bottom_right['y-off'],bottom_right['width'],bottom_right['height']))))

            raw_array = [top_left_btn, top_right_btn, bottom_left_btn, bottom_right_btn]

            #GET TEXT, CLEAN IT, AND ADD IT TO A CLEAN ARRAY
            clean_array = []
            for button in raw_array:
                raw_answer = unidecode.unidecode((pytesseract.image_to_string(button, lang='eng')).lower()).strip()
                clean_array.append(raw_answer)

            #CHECK SO WE DONT REPEAT THE SAME CLICK ACTION AS BEFORE
            if last_answer != last_action:

                Display(lurdes_status='I\'am thinking..')

                #GET THE INDEX OF THE ANSWER
                algo_response = identify_answer_index(answer=last_answer, dictionary=clean_array)

                #IF a != False and probability > 0
                if algo_response:
                    if algo_response[0] > 0:

                        #OVERWRITE THE LAST ACTION WITH THE NEW ANSWER ACTION
                        last_action = last_answer

                        #DEFINE INDEX OF THE ANSWER
                        index = algo_response[1]

                        if index == 0:
                            click(coords["player_top_left"]["x-off"], coords["player_top_left"]["y-off"])
                            button = 'top left'
                        elif index == 1:
                            click(coords["player_top_right"]["x-off"], coords["player_top_right"]["y-off"])
                            button = 'top right'
                        elif index == 2:
                            click(coords["player_bottom_left"]["x-off"], coords["player_bottom_left"]["y-off"])
                            button = 'bottom left'
                        elif index == 3:
                            click(coords["player_bottom_right"]["x-off"], coords["player_bottom_right"]["y-off"])
                            button = 'bottom right'
                        
                        sleep(1)
                        Display(lurdes_status=f'Clicked the {button} button ({last_answer})')

#DISPLAY FUNCTION
def Display(status=False, question=False, answer=False, probability=False, lurdes_status=False):
    if not question or not answer or not probability:
        question = last_question
        probability = last_probability
        answer = last_answer

    if not status:
        status = last_status

    if not lurdes_status:
        lurdes_status = 'I\'m alive!' 

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

    if len(status) < 48:
        status = f'{status}{(48-len(status))*" "}'

    #LURDES STATUS
    if len(lurdes_status) < 48:
        lurdes_status = f'{lurdes_status}{(48-len(lurdes_status))*" "}'
    else:
        lurdes_status = f'{lurdes_status[:46]}..'

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
      | {status} |
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

    if autop:
        print(f'''\033[94m
      |--------------------------------------------------|
      | \033[93mA.I:   \033[94m                                          |
      | \033[92m{lurdes_status}\033[94m |
      |--------------------------------------------------|
    ''')

    

#OTHER FUNCTIONS
def CleanRaw(text):
    #CLEAN THE QUESTION TEXT
    sliced_question = text.split('\n')
    for slice_ in sliced_question:
        if len(slice_) > 10:
            return slice_.strip()
            break
        else:
            return ''

def ClearWindow():
    if sys.platform.startswith('linux'):
        system('clear')
    else:
        system('cls')
    
def FilterImage(image):
    return ImageOps.grayscale(image).filter(ImageFilter.MinFilter(1)).filter(ImageFilter.SMOOTH_MORE).filter(ImageFilter.SMOOTH_MORE)


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

    #INIT AUTOPLAY IN CASE ITS TRUE
    if autop:
        t = Thread(target=(AutoPlay))
        t.start()


    #SET WINDOW
    SetWindow()
    #SET DB BY SCRAPING OR LOADING
    SetDB(topic=str(input('       Topico: ')),)
    #START THE MAIN FUNCTION
    Imaging()