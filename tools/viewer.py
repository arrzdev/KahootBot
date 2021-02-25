import numpy as np
from PIL import ImageGrab, Image
import cv2
import json

while True:
    coords = json.loads(open('../coords.json').read())

    fullscreen_coords = coords['fullscreen']
    full_img = np.array(ImageGrab.grab(bbox=(fullscreen_coords['x-off'],fullscreen_coords['y-off'],fullscreen_coords['width'],fullscreen_coords['height'])))

    ingame_coords = coords['ingame']
    question_game_image = np.array(ImageGrab.grab(bbox=(ingame_coords['x-off'],ingame_coords['y-off'],ingame_coords['width'],ingame_coords['height'])))

    loading_coords = coords['loading']
    question_loading_image = np.array(ImageGrab.grab(bbox=(loading_coords['x-off'],loading_coords['y-off'],loading_coords['width'],loading_coords['height'])))


    cv2.imshow('FullImageCanvas', full_img)
    cv2.imshow('InGameCanvas', question_game_image)
    cv2.imshow('LoadingCanvas', question_loading_image)

    if cv2.waitKey(25) & 0xFF == ord('q'):  
            cv2.destroyAllWindows()
            break



