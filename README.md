// ABOUT //

KahootBot is program that gives you the answer to any question from your teacher kahoot.
Using ComputerVision, Pytesseract etc...
Works from meeting screenshare: (Google-Meet, Zoom, Microsoft-Teams, Jitsi)
Thanks to, https://github.com/TitanHZZ, for tips and support.

// HOW TO USE GUIDE //

 PRE-REQUISITES:
- Windows version > 8.0
- Python version > 3.7
- Dependencies on requirements.txt
- Native pytesseract installed and of course custom language if thats the case


 STEP-BY-STEP TUTORIAL:
- Change your Pytesseract path to meet your Path
- Fixate the google meet screenshare
- Change coords.cfg file to get the current sizes for your screen (test with tools/viewer.py)
- Start the script by typing: python main.py 
- Have Fun :)



// TO-DO //
- Set db by (topic, language, creation...) instead of link (top 4)
- Create updateDB.py
- Auto-answer with win32 or pyautogui
- Add a way to change the percentage of winning with auto-answer that we want
- Change the design ?