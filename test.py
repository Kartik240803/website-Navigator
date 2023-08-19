import requests
import speech_recognition as sr
import pyttsx3
from bs4 import BeautifulSoup
import time
import keyboard
import pyperclip
from selenium.webdriver.common.by import By
from selenium import webdriver


time.sleep(5)
def get_chrome_url():
    keyboard.press_and_release('ctrl+l')
    time.sleep(0.5) 
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.5)
    url = pyperclip.paste()
    print(url)
    return url
url = get_chrome_url()
driver = webdriver.Chrome()

driver.get(url)
time.sleep(2)



link_elements = driver.find_elements(By.TAG_NAME, "a")
links = [link.get_attribute("href") for link in link_elements]


def get_paragraph_word_length(paragraph):
    
    words = paragraph.split()
    word_length = len(words)
    return word_length

def information(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
    else:
        print("Failed to fetch the page.")
        exit()
    
    title = soup.title

    if title is not None:
       
        page_title = title.get_text()
        speak(f"You are on the {page_title} page")
    else:
        print("Title element not found.")
    
    paragraphs = soup.find_all('p')
    if paragraphs:
        for paragraph in paragraphs:

            length = get_paragraph_word_length(paragraph.get_text())
            j = 1
            if(length>15 & j==1):
                speak(paragraph.get_text())
                speak("Do you want to hear more?")
                i = 1
                while(i):
                    q=listen()
                    if(q!=""):
                        if 'yes' in q :
                            i = 0
                        elif 'no' in q :
                            i,j = 0,0
                    
                    else:
                        speak("Do you want to hear more?")
                if (j==0) :
                    break
                       
                
    else:
        print("No paragraphs found on the page.")

    forms = soup.find_all('form')

    if forms:
        for form in forms:
            speak("There is form on the page ")
            print(soup.find('form')['id'])
            form_elements = form.find_all('input label')
            for element in form_elements:
                if 'id' in element.attrs:
                    element_id = element['id']
                else:
                 element_id = None
                print(f"Tag: {element.get_text()}, ID: {element_id}")
    else:
        print("No forms found on the page.")


def listen():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language="en")
        
    except:
         return ""
    
    query =str(query).lower()
    
    return query

def speak(text):
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voices',voices[0].id)
    engine.setProperty('rate',155)
    print("")
    print(f"You {text}")
    print("")
    engine.say(text)
    engine.runAndWait()

while(1):
    query = listen()
   
    query = query.replace("take","")
    query = query.replace(" ","")
    query = query.replace("navigate","")
    query = query.replace("to","")
    query = query.replace("the","")
    query = query.replace("page","")
    print(query)

    if query ==("quite"):
       
        break
    elif query ==("bye"):
        
        break
    elif "home" in query :
        driver.get(url)
    elif "information" in query :
        url1  = get_chrome_url()
        information(url1)
    elif query == "" :
        speak("")
           
    elif query != "":
        print(len(links))
        
        for i in range(len(links)):
            if query in links[i]:
                print("if")
                driver.get(links[i])
                break
                
        else:
            speak("No page found on the website you are trying to reach")



