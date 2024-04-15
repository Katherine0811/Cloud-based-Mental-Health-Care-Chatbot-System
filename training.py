from tkinter import *
import tkinter.messagebox as tkMessageBox
import json
from itertools import chain

from chatterbot import ChatBot

from chatterbot.trainers import ListTrainer

# allow user to match best response for chatbot
from difflib import get_close_matches

from main import display_message

# Retrieve training data from "training_bank.json" file
def load_training_bank(file_path: str) -> dict:
    with open (file_path, 'r') as file:
        data: dict = json.load(file)
        return data

# Save new response from the "training_bank" dict to the "training_bank.json" file
def save_training_bank(file_path: str, data: dict):
    with open (file_path, 'w') as file:
        json.dump(data, file, indent = 2)

# Return the question that is closest to the user input if exists, else return none
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n = 1, cutoff = 0.9)
    return matches[0] if matches else None

# Get answer from the question retrieved by the function: find_best_match
def get_answer_for_question(question: str, training_bank: dict) -> str | None:
    for q in training_bank["questions"]:
        if q["question"] == question:
            return q["answer"]

# Chatbot process
def chat_bot_function(user_input):
    training_bank: dict = load_training_bank("training_bank.json")

    best_match: str | None = find_best_match(user_input, [q["question"] for q in training_bank["questions"]])

    # If best response exists, reply back
    if best_match:
        answer: str = get_answer_for_question(best_match, training_bank)
        return("trained", f'Bot: {answer}')
    # Else, prompt user to suggest an answer for training the chatbot
    else:
        print("trained",'Bot: I don\'t know the answer. Can You teach me?')
        new_answer: str = input('Type the answer or "skip" to skip: ')

        # User can skip to avoid answering
        if new_answer.lower() != 'skip':
            training_bank["questions"].append({"question": user_input, "answer": new_answer})
            save_training_bank("training_bank.json", training_bank)
            print("Bot: Thank you! I learned a new response!")

def train_chat_bot(training_bank, user_input):
    print('Bot: I don\'t know the answer. Can You teach me?')
    new_answer: str = input('Type the answer or "skip" to skip: ')

    # User can skip to avoid answering
    if new_answer.lower() != 'skip':
        training_bank["questions"].append({"question": user_input, "answer": new_answer})
        save_training_bank("training_bank.json", training_bank)

def train_chatterbot(message):
    #dictionary for the intent in the json file
    data ={}
        
    #counter to enumerate key and identify key
    count1=0

    # list to hold intents pattern and response for user and bot respectively
    list_questionkey=[]
    list_questionvalue=[]
    list_answerkey=[]
    list_answervalue=[]
        
    # dictionary to hold intents question and answer for user and bot respectively
    dict_question={}
    dict_answer={}
        
    data = load_training_bank("training_bank.json")

    for m in data["questions"]:
        count1 = count1 + 1
        dict_question[count1]=m["question"]
        dict_answer[count1]=m["answer"]


    # loop to dictionary to add value of dictionary to list for pattern and response
    for i, v in dict_question.items():
        list_questionkey.append(i)
        list_questionvalue.append(v)

    for i, v in dict_answer.items():
        list_answerkey.append(i)
        list_answervalue.append(v)
        

    # add all question and answer in one list sequentially to use for chatterbot training

    train_list=[]

    for q in list_questionvalue:
        train_list.append(q)
        for a in list_answervalue:
            train_list.append(a)

    
    # Create object of ChatBot class with Logic Adapter for best response match
    bot = ChatBot(
    'Mental Health Bot',
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    #storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.',
            #try these search algorithm for better match
            #--chatterbot.comparisons.LevenshteinDistance--#
            #--chatterbot.comparisons.JaccardSimilarity--#
            #--chatterbot.comparisons.SpacySimilarity--#
            "statement_comparison_function": 'chatterbot.comparisons.LevenshteinDistance'
        }
    ]
    )

    trainer = ListTrainer(bot)

    # add all question and answer in one list sequentially to use for chatterbot training

    train_list=[]

    train_list = list(chain.from_iterable(zip(list_questionvalue, list_answervalue)))

    trainer.train(train_list)

    #return bot trained data    
    response=bot.get_response(message)
    return response