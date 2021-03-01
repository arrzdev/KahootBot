import numpy as np
from PIL import ImageGrab, Image
import cv2
import json

while True:
    coords = json.loads(open('../coords.json').read())

    fullscreen_coords = coords['fullscreen']
    full_img = np.array(ImageGrab.grab(bbox=(fullscreen_coords['x-off'],fullscreen_coords['y-off'],fullscreen_coords['width'],fullscreen_coords['height'])))
    cv2.imshow('FullImageCanvas', full_img)

    #question_game_image = np.array(ImageGrab.grab(bbox=(fullscreen_coords['x-off'],fullscreen_coords['y-off']+5,fullscreen_coords['width'],370)))
    #cv2.imshow('InGameCanvas', question_game_image)

    #question_loading_image = np.array(ImageGrab.grab(bbox=(fullscreen_coords['x-off'],fullscreen_coords['y-off']+200,fullscreen_coords['width'],625)))
    #cv2.imshow('LoadingCanvas', question_loading_image)


    '''
    VIEW BUTTONS UI
    top_left = coords['top_left']
    top_right = coords['top_right']
    bottom_right = coords['bottom_right']
    bottom_left = coords['bottom_left']
    
    top_left_btn = np.array(ImageGrab.grab(bbox=(top_left['x-off'],top_left['y-off'],top_left['width'],top_left['height'])))
    top_right_btn = np.array(ImageGrab.grab(bbox=(top_right['x-off'],top_right['y-off'],top_right['width'],top_right['height'])))
    bottom_left_btn = np.array(ImageGrab.grab(bbox=(bottom_left['x-off'],bottom_left['y-off'],bottom_left['width'],bottom_left['height'])))
    bottom_right_btn = np.array(ImageGrab.grab(bbox=(bottom_right['x-off'],bottom_right['y-off'],bottom_right['width'],bottom_right['height'])))

    cv2.imshow('top_left', top_left_btn)
    cv2.imshow('top_right', top_right_btn)
    cv2.imshow('bottom_right', bottom_right_btn)
    cv2.imshow('bottom_left', bottom_left_btn)
    '''

    if cv2.waitKey(25) & 0xFF == ord('q'):  
            cv2.destroyAllWindows()
            break


