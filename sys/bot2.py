from tkinter import *

# import nltk

# from nltk.stem import WordNetLemmatizer

# lemmatizer = WordNetLemmatizer()

import json

import pickle

import numpy as np

# from keras.models import Sequential

# from keras.layers import Dense, Activation, Dropout

# from keras.optimizers import SGD

import random


root = Tk()
root.title("Chatbot")
def send():
    send = "You -> "+e.get()
    txt.insert(END, "\n"+send)
    user = e.get().lower()

    # Load data from intents.json
    count1 = 0   
    data_file = open('intents.json').read()
    intents = json.loads(data_file)

    # list to hold intents pattern and response for user and bot respectively
    list_patternkey=[]
    list_patternvalue=[]
    list_responsekey=[]
    list_responsevalue=[]

    # dictionary to hold intents pattern and response for user and bot respectively
    dict_pattern={}
    dict_response={}

    #loop and add values of patterns and response to dictioanry
    for m in intents["intents"]:
        count1 = count1 + 1
        dict_pattern[count1]=m["patterns"]
        dict_response[count1]=m["responses"]

    # loop to dictionary to add value of dictionary to list for pattern and response
    for i, v in dict_pattern.items():
        list_patternkey.append(i)
        list_patternvalue.append(v)

    for i, v in dict_response.items():
        list_responsekey.append(i)
        list_responsevalue.append(v)

    # counter variable to keep track of list and dictionary index
    cn = 0
    
    # list declaration for list comprehension to filter user input with pattern in intent file
    plcp =[]

    # loop to get index of response for bot to reply user
    for u in list_patternvalue:
        plcp = [b for b in u if user.capitalize() in b]
        cn = cn + 1
        if user.capitalize() in plcp:
            break

    #randomize bot response based on intent 
    user = user.capitalize()
    lcp= [u for u in list_patternvalue if user in u]
    reslistlen = len(list_responsevalue[cn])
    randm = random.randint(0,reslistlen)
    cn = cn-1
    
    # print bot response to screen
    txt.insert(END, "\n" + "Bot -> "+str(list_responsevalue[cn][randm]))
    
    e.delete(0, END)
    
txt = Text(root)
txt.grid(row=0, column=0, columnspan=2)
e = Entry(root, width=100)
e.grid(row=1, column=0)
send = Button(root, text="Send", command=send).grid(row=1, column=1)
root.mainloop()



