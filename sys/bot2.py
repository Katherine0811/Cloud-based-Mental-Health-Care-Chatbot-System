from tkinter import *

import nltk

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

import json

import pickle

import numpy as np

from keras.models import Sequential

from keras.layers import Dense, Activation, Dropout

from keras.optimizers import SGD

import random



def getresponse(n,m):
    randm = random.randint(0,1)
    message = n[m][randm]
    return message


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

     
        
    data_file = open('intents.json').read()

    intents = json.loads(data_file)

    listp=[]
    listp1=[]
    listp2=[]
    listp3=[]

    dict1={}
    dict2={}

    for m in intents["intents"]:
        count1 = count1 + 1
        dict1[count1]=m["patterns"]
        dict2[count1]=m["responses"]


    for i, v in dict1.items():
        listp.append(i)
        listp1.append(v)

    for i, v in dict2.items():
        listp2.append(i)
        listp3.append(v)

    cn = 0
    ui=0
    
    for u in listp1:
        for b in u:
            cn = cn + 1
            if user in b:
                ui=b.index("Hey")
                break;


        
    user = user.capitalize()
    lcp= [u for u in listp1 if user in u]
    randm = random.randint(0,2)
    txt.insert(END, "\n" + "Bot -> "+str(lcp[ui][randm]))
    
    





   ## if user in listp:
   ##     txt.insert(END, "\n" + "Bot -> "+user)
  ##  else:
    ##    txt.insert(END, "\n" + "Bot -> "+str(rs))


    e.delete(0, END)
txt = Text(root)
txt.grid(row=0, column=0, columnspan=2)
e = Entry(root, width=100)
e.grid(row=1, column=0)
send = Button(root, text="Send", command=send).grid(row=1, column=1)
root.mainloop()



