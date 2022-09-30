import pyttsx3  
import datetime 
import speech_recognition as sr 
import webbrowser as wb
import os
import playsound
import time
import requests
from playsound import playsound
import msvcrt as m

def wait():
    m.getch()

KHEC_AI_assistant=pyttsx3.init()  
voice=KHEC_AI_assistant.getProperty('voices')
assistant_voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
KHEC_AI_assistant.setProperty('voice',assistant_voice_id)




import nltk
from nltk.stem import WordNetLemmatizer
# from nltk.corpus import stopwords
# stop_word =stopwords.words('english')
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import re
from keras.models import load_model
model = load_model('./chatbot_model.h5')
import json
import random
global base

#Creating GUI with tkinter
# import tkinter
from tkinter import *



# stop_word=["a","the","an","c'mon","co","co.","t's","un","unto","v","viz","vs","a","b","c","d","e","f","g","h","j","l","m","n","o","p","q","r","s","t","u","uucp","w","x","y","z"]
#--------
intents = json.loads(open('./intents.json').read())
words = pickle.load(open('./words.pkl','rb'))
classes = pickle.load(open('./classes.pkl','rb'))
#bot_name = "khec_Bot"

#--------

def cleaning(sentence):
    sentence= sentence.lower()
    sentence = re.sub(r"i'm","i am",sentence)
    sentence = re.sub(r"he's","he is",sentence)	
    sentence = re.sub(r"she's","she is",sentence)	
    sentence = re.sub(r"that's","that is",sentence)
    sentence = re.sub(r"what's","what is",sentence)	
    sentence = re.sub(r"where's","where is",sentence)		
    sentence = re.sub(r"\'ll","will",sentence)	
    sentence = re.sub(r"\'ve","have",sentence)	
    sentence = re.sub(r"\'re","are",sentence)	
    sentence = re.sub(r"\'d","will",sentence)	
    sentence = re.sub(r"won't","will not",sentence)	 
    sentence = re.sub(r"can't","cannot",sentence)	
    sentence = re.sub(r"[-()\"#/@;:<>=|.?,]","",sentence)
    sentence_words = nltk.word_tokenize(sentence)

    # filter_stopword=[t for t in sentence_words if t not in stop_word]
    filter_word = list(filter(lambda x: x in classes or words, sentence_words))
    print("###########_______###############---------------"+str(filter_word)+"______________##########################")
    return filter_word
#--------

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words=cleaning(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words) 
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
   
    # ERROR_THRESHOLD = 0.20

    results = [[i,r] for i,r in enumerate(res)]     #=> results=[[i,r],[i,r]....]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)  # x=[i,r]

    return_list = []
   
    return_list.append({"intent": classes[results[0][0]], "probability": str(results[0][1])})
    return return_list
    
def getResponse(ints, intents_json,tagging=False):
    if tagging == True:
        tag = ints
    else:
        tag = ints[0]['intent']
    
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(text):  
    if text in classes:
        res = getResponse(text,intents,tagging=True)
        print("This is my response==================>"+str(res))
        return res
    ints = predict_class(text, model)  
    prob=float(ints[0]['probability']) #filtering the highest
    # print(type(prob))
    print(prob)
    if prob > 0.77:
        res = getResponse(ints, intents)
    else:
        res="I can't get it,Can you please reformulae it and say or type again?"
    return res
        # ////////////////////////////////////////////////////////////////////////////////////////

def speak(audio):
    print('KHEC_AI_assistant: ' + audio)
    KHEC_AI_assistant.say(audio)
    KHEC_AI_assistant.runAndWait()

def time():
    Time=datetime.datetime.now().strftime('%I:%M: %p') 
    speak('It is')
    speak(Time)


def date():
    url= f'https://timesles.com/en/calendar/weeks/days/today/'
    wb.get().open(url)
    speak('This is the date today')


#welcome and wish Goodmorning,afternoon,evening with time duration
def welcome(): 
    hour=datetime.datetime.now().hour
    if hour >=3 and hour <12:
        speak('Good morning,Welcome to kHEC')
    elif hour >=12 and hour <18:
        speak('Good afternoon,Welcome to kHEC')
    elif hour >=18 and hour <21:
        speak('Good evening ,Welcome to kHEC')
    elif hour >=21 and hour <24:
        speak('Good night and have a nice dream boss!')
    elif hour >=0 and hour <3:
        speak('It is late, let us take a nap')
    speak('How can I help you now?')



#listening... check internet status
def command(): 
    
    if internetstatus==1:
        print(' ')
        print('Listening . . .')
        print(' ')
       
        c=sr.Recognizer()
        with sr.Microphone() as source:
            c.pause_threshold=1
            audio=c.listen(source)    
        try:
            query = c.recognize_google(audio,language='en-US')
          

        except sr.UnknownValueError:
            print('Sorry, I did\'t get that.( Try typing the command)😁: ')
            query = str(input('your favor is: '))
        
        return query

    if internetstatus==2:
        print('No internet! If your pc have connected to the internet, type: internet')
        print('Or if your pc have not connected to the internet,')
        query = str(input('Try typing your command: '))
        return query

# #test and speak
def Test_Speak(query):
    os.system('cls')
    if "map" in query:
        url = f'https://www.google.com/maps/'
        wb.get().open(url)
        speak(f'This is google maps')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')

    elif "who is hod of computer department" in query:
        # os.system('cls')
        print('User: ' + query)
        speak(f'Our Dearest Er.Biskash Chawal sir.')
        speak(f'How can I help you now?')

    elif "who is head of computer department" in query:
        # os.system('cls')
        speak(f'Our Dearest Er.Biskash Chawal sir.')
        speak(f'How can I help you now?')

    elif "who is principal of your college" in query:
        # os.system('cls')
        speak(f'Er.Sujan maka sir.')
        speak(f'How can I help you now?')

    elif "what is your name" in query:
        # os.system('cls')
        speak(f'I am called as KHEC chatbot')
        speak(f'How can I help you now?')

    elif "how are you" in query:
        # os.system('cls')
        speak(f'Thank you for your concern,I am doing good')
        speak(f'How can I help you now?')

    elif "hello" in query:
        # os.system('cls')
        speak(f'Hello!!')
        speak(f'How can I help you now?')
    elif "how are you" in query:
        # os.system('cls')
        speak(f'I am feeling good today. Thank you')
        speak(f'How can I help you now?')
    elif "maps" in query:
        # os.system('cls')
        url = f'https://www.google.com/maps/'
        wb.get().open(url)
        speak(f'This is google maps')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')
    elif "glob" in query or "earth" in query: #all global or globe returns to this code
        # os.system('cls')
        url = f'https://earth.google.com/web/@16.24291914,105.7762962,-1110.77003945a,12946843.60659599d,35y,0h,0t,0r'
        wb.get().open(url)
        speak(f'This is google earth')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')
    elif 'translate' in query or 'dictionary' in query: 
        # os.system('cls')
        url=f'https://www.dict.cc/'
        wb.get().open(url)
        speak(f'This is german-english dictionary.')
        url2=f'https://jdict.net/'
        speak('...')
        speak('...')
        wb.get().open(url2)
        speak('this is Japanese-Vietnamese dictionary.')
        speak('...')
        url3=f'https://translate.google.com/'
        speak('...')
        wb.get().open(url3)
        speak('this is google translate.')
        url4=f'https://www.oxfordlearnersdictionaries.com/'
        speak('...')
        speak('...')
        wb.get().open(url4)
        speak(' and this is Oxford dictionary')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')

    elif 'google' in query: 
        # os.system('cls')
        speak('What should I search now?')
        search=command().lower()
        url=f'https://www.google.com/search?q={search}'
        wb.get().open(url)
        speak(f'I found something on Google for your search:')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')


    elif 'weather' in query or 'climate' in query: 
        # os.system('cls')
        url=f'https://www.google.com/search?q=weather'
        wb.get().open(url)
        speak(f'This is your local weather!')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do, boss?')

    elif 'type' in query: 
        # os.system('cls')
        speak('Which language do you want to type?')
        search=command().lower()
        if 'english' in search:
            url=f'https://10fastfingers.com/typing-test/english'
            wb.get().open(url)
            speak(f'Try your best with this English typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'vietnam' in search:
            url=f'https://10fastfingers.com/typing-test/vietnamese'
            wb.get().open(url)
            speak(f'Try your best with this Vietnamese typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'german' in search:
            url=f'https://10fastfingers.com/typing-test/german'
            wb.get().open(url)
            speak(f'Try your best with this German typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'japan' in search:
            url=f'https://10fastfingers.com/typing-test/japanese'
            wb.get().open(url)
            speak(f'Try your best with this Japanese typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'french' in search:
            url=f'https://10fastfingers.com/typing-test/french'
            wb.get().open(url)
            speak(f'Try your best with this French typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'france' in search:
            url=f'https://10fastfingers.com/typing-test/french'
            wb.get().open(url)
            speak(f'Try your best with this French typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'russia' in search:
            url=f'https://10fastfingers.com/typing-test/russian'
            wb.get().open(url)
            speak(f'Try your best with this Russian typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'nether' in search:
            url=f'https://10fastfingers.com/typing-test/dutch'
            wb.get().open(url)
            speak(f'Try your best with this Dutch typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'neder' in search:
            url=f'https://10fastfingers.com/typing-test/dutch'
            wb.get().open(url)
            speak(f'Try your best with this Dutch typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'hol' in search:
            url=f'https://10fastfingers.com/typing-test/dutch'
            wb.get().open(url)
            speak(f'Try your best with this Dutch typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'chin' in search:
            speak('Chinese simplified or Chinese Traditional? ')
            chinesetype=command().lower()
            if 'simple' in chinesetype:
                url=f'https://10fastfingers.com/typing-test/simplified-chinese'
                wb.get().open(url)
                speak(f'Try your best with this Chinese Simplified typing test!')
                speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
                wait()
                speak(f'what else you would like me to do?')
            elif 'simplif' in chinesetype:
                url=f'https://10fastfingers.com/typing-test/simplified-chinese'
                wb.get().open(url)
                speak(f'Try your best with this Chinese-Simplified typing test!')
                speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
                wait()
                speak(f'what else you would like me to do?')
            elif 'tradition' in chinesetype:
                url=f'https://10fastfingers.com/typing-test/traditional-chinese'
                wb.get().open(url)
                speak(f'Try your best with this Chinese-Traditional typing test!')
                speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
                wait()
                speak(f'what else you would like me to do?')
        elif 'korea' in search:
            url=f'https://10fastfingers.com/typing-test/korean'
            wb.get().open(url)
            speak(f'Try your best with this Korean typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'ital' in search:
            url=f'https://10fastfingers.com/typing-test/italian'
            wb.get().open(url)
            speak(f'Try your best with this Italian typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'spa' in search:
            url=f'https://10fastfingers.com/typing-test/spanish'
            wb.get().open(url)
            speak(f'Try your best with this Spanish typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'portug' in search:
            url=f'https://10fastfingers.com/typing-test/portuguese'
            wb.get().open(url)
            speak(f'Try your best with this Portuguese typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'thai' in search:
            url=f'https://10fastfingers.com/typing-test/thai'
            wb.get().open(url)
            speak(f'Try your best with this Thai typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')
        elif 'arab' in search:
            url=f'https://10fastfingers.com/typing-test/arabic'
            wb.get().open(url)
            speak(f'Try your best with this Arabic typing test!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            wait()
            speak(f'what else you would like me to do?')


    elif 'search' in query:
        # os.system('cls')
        speak('What should I search now boss?')
        search=command().lower()
        url=f'https://www.google.com/search?q={search}'
        wb.get().open(url)
        speak(f'I found something on Web for your search:')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')



    elif 'web' in query:
        # os.system('cls')
        speak('What should I search now boss?')
        search=command().lower()
        url=f'https://www.google.com/search?q={search}'
        wb.get().open(url)
        speak(f'I found something on Web for your search:')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')

    elif 'facebook' in query:
        # os.system('cls')
        url=f'https://www.facebook.com/'
        wb.get().open(url)
        speak(f'This is facebook for you')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')
    elif 'twitter' in query:
        # os.system('cls')
        url=f'https://twitter.com/'
        wb.get().open(url)
        speak(f'This is twitter for you')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')
    elif 'browser' in query:
        # os.system('cls')
        speak('What should I search now boss?')
        search=command().lower()
        url=f'https://www.google.com/search?q={search}'
        wb.get().open(url)
        speak(f'I found something on Web for your search:')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')


    elif 'look up' in query:
        # os.system('cls')
        speak('What should I search now boss?')
        search=command().lower()
        url=f'https://www.google.com/search?q={search}'
        wb.get().open(url)
        speak(f'I found something on Web for your search:')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')



    elif "youtube" in query:
        # os.system('cls')
        speak('What should I search on youtube now?')
        search=command().lower()
        url = f'https://youtube.com/search?q={search}'
        wb.get().open(url)
        speak(f'I found something on Youtube for your search:')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')
    
    elif ("quit" in query or "stop" in query or "bye" in query or "see you later" in query or "see you" in query) :
        # os.system('cls')
        speak("KHEC chatbot is signing off.Goodbye")
        playsound('C:/KHEC_CHAT/KhecVoiceBot/NEWAIASSISTANTBYBACH/assets/welcome_tone.mp3')
        quit()
    
    elif 'time' in query or 'clock' in query:
        # os.system('cls')
        time()
        speak(f'what else you would like me to do?')
    
    elif 'date' in query or 'day' in query or 'month' in query or 'year' in query:
        # os.system('cls')
        date()
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak(f'what else you would like me to do?')

    elif 'you can' in query: 
        # os.system('cls')
        speak('Primarily, I will try my best to give queries answer related to our khec college')
        speak('I can tell you the time and weather.')
        speak('I also can open browser or youtube.')
        # speak('In addition, I can open some review tests for your grade.')
        speak('Besides, I can open a typing test with many languages supported')
        speak('I can open translator, google maps and google earth too!')
        speak('So, what would you like me to do now boss?')
    elif 'ability' in query: 
        # os.system('cls')
        speak('Primarily, I will try my best to give queries answer related to our khec college')
        speak('I can tell you the time and weather.')
        speak('I also can open browser or youtube.')
        # speak('In addition, I can open some review tests for your grade.')
        speak('Besides, I can open a typing test with many languages supported')
        speak('I can open translator, google maps and google earth too!')
        speak('So, what would you like me to do now boss?')
    elif 'function' in query: 
        # os.system('cls')
        speak('Primarily, I will try my best to give queries answer related to our khec college')
        speak('I can tell you the time and weather.')
        speak('I also can open browser or youtube.')
        # speak('In addition, I can open some review tests for your grade.')
        speak('Besides, I can open a typing test with many languages supported')
        speak('I can open translator, google maps and google earth too!')
        speak('So, what would you like me to do now boss?')

    elif 'create you' in query:
        # os.system('cls')
        speak('Chatbot Team created me. How can I help you now, boss?')

    elif 'created you' in query: 
        # os.system('cls')
        speak('Chatbot Team created me. How can I help you now, boss?')
    elif 'made you' in query: 
        # os.system('cls')
        speak('Chatbot Team created me. How can I help you now, boss?')
    elif 'make you' in query: 
        speak('Chatbot Team created me. How can I help you now, boss?')
    elif 'help' in query: 
        # os.system('cls')
        speak('This is the instruction')
        os.startfile('C:/KhecVoiceBot/NEWAIASSISTANTBYBACH/instruction.docx')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak('So, what would you like me to do now?')
    elif 'instruct' in query: 
        # os.system('cls')
        speak('This is the instruction')
        os.startfile('C:/KhecVoiceBot/NEWAIASSISTANTBYBACH/instruction.docx')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak('So, what would you like me to do now?')
    elif 'how to use' in query: 
        # os.system('cls')
        speak('This is the instruction')
        os.startfile('C:/KhecVoiceBot/NEWAIASSISTANTBYBACH/instruction.docx')
        speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
        wait()
        speak('So, what would you like me to do now?')

    elif 'relax' in query:
        # os.system('cls')
        speak('Do you want to listen to music or play a game?')
        search=command().lower()
        if 'music' in search:
            speak('Hope you enjoy!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            os.startfile('C:/KhecVoiceBot/NEWAIASSISTANTBYBACH/chill songs.mp3')
            wait()
            speak(f'what else you would like me to do?')
            
        elif 'song' in search:
            speak('Hope you enjoy!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            os.startfile('C:/KhecVoiceBot/NEWAIASSISTANTBYBACH/chill songs.mp3')
            wait()
            speak(f'what else you would like me to do?')
            
        elif 'game' in search:
            speak('Hope you enjoy!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            os.startfile('C:/KhecVoiceBot/NEWAIASSISTANTBYBACH/ball.exe')
            wait()
            speak(f'what else you would like me to do?')
        
    elif 'stress' in query:
        # os.system('cls')
        speak('Do you want to listen to music or play a game?')
        search=command().lower()
        if 'music' in search:
            speak('Hope you enjoy!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            os.startfile('C:/KhecVoiceBot/NEWAIASSISTANTBYBACH/chill songs.mp3')
            wait()
            speak(f'what else you would like me to do?')
            
        elif 'song' in search:
            speak('Hope you enjoy!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            os.startfile('C:/KhecVoiceBot/NEWAIASSISTANTBYBACH/chill songs.mp3')
            wait()
            speak(f'what else you would like me to do?')
        elif 'game' in search:
            speak('Hope you enjoy!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            os.startfile('C:/KhecVoiceBot/NEWAIASSISTANTBYBACH/ball.exe')
            wait()
            speak(f'what else you would like me to do?')

    elif 'hang out' in query:
        # os.system('cls')
        print('Boss: ' + query)
        speak('Do you want to listen to music or play a game?')
        search=command().lower()
        if 'music' in search:
            speak('Hope you enjoy!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            os.startfile('C:/KhecVoiceBot/NEWAIASSISTANTBYBACH/chill songs.mp3')
            wait()
            speak(f'what else you would like me to do?')
            
        elif 'song' in search:
            speak('Hope you enjoy!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            os.startfile('C:/KhecVoiceBot/NEWAIASSISTANTBYBACH/chill songs.mp3')
            wait()
            speak(f'what else you would like me to do?')
            
        elif 'game' in search:
            speak('Hope you enjoy!')
            speak('Assistant is paused. You can later click on me and press any key on keyboard to resume me')
            os.startfile('C:/KhecVoiceBot/NEWAIASSISTANTBYBACH/ball.exe')
            wait()
            speak(f'what else you would like me to do?')

    else:
        res = chatbot_response(query)
        speak(res)
        speak(f'Is there anything sir?')
    return    

def Khec_chatBot(): 
    global base 
    # os.system('cls')
    speak('Welcome to KHEC Chatbot')
    playsound('C:/KHEC_CHAT/KhecVoiceBot/NEWAIASSISTANTBYBACH/assets/welcome_tone.mp3')
    welcome() 
    while True:
        query=command().lower() 
        Test_Speak(query)


if __name__ =='__main__':
    internetstatus=0
    url = "https://www.google.com/"
    timeout = 1.5
    try:
        request = requests.get(url, timeout=timeout)
        internetstatus=1
    except (requests.ConnectionError, requests.Timeout) as exception:
        internetstatus=2

    Khec_chatBot()