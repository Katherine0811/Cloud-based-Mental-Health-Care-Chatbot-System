import json
# allow user to match best response for chatbot
from difflib import get_close_matches

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
def chat_bot():
    training_bank: dict = load_training_bank("training_bank.json")
    
    # Loop conversation until user prompt to exit
    while True:
        user_input: str = input('You: ')

        if user_input.lower() == "quit":
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in training_bank["questions"]])

        # If best response exists, reply back
        if best_match:
            answer: str = get_answer_for_question(best_match, training_bank)
            print(f'Bot: {answer}')
        # Else, prompt user to suggest an answer for training the chatbot
        else:
            print('Bot: I don\'t know the answer. Can You teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            # User can skip to avoid answering
            if new_answer.lower() != 'skip':
                training_bank["questions"].append({"question": user_input, "answer": new_answer})
                save_training_bank("training_bank.json", training_bank)
                print("Bot: Thank you! I learned a new response!")

if __name__ == "__main__":
    chat_bot()