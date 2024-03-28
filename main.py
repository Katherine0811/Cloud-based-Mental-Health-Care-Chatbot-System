from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3

from training import *

#=======================================METHODS=======================================
def database():
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, firstname TEXT, lastname TEXT)")
    cursor.close()
    conn.close()

def login_form(panel):
    # Create Login Window
    panel.withdraw()
    loginFrame = Toplevel()
    loginFrame.title("Login Portal")
    loginFrame.geometry('1000x500')
    loginFrame.configure(background = '#DBD0C0')
    
    # Display Labels
    lbl_username = Label(loginFrame, text = "Username:", bg = '#DBD0C0', font = ('times', 15, 'bold'))
    lbl_username.place(x = 300, y = 200)
    lbl_password = Label(loginFrame, text = "Password:", bg = '#DBD0C0', font = ('times', 15, 'bold'))
    lbl_password.place(x = 300, y = 250)

    # User Input
    username = Entry(loginFrame, bg = '#DBD0C0', font = ('times', 15, 'bold'), width = 40)
    username.place(x = 450, y = 200)
    password = Entry(loginFrame, bg = '#DBD0C0', font = ('times', 15, 'bold'), width = 40, show = "*")
    password.place(x = 450, y = 250)

    # Display Buttons
    btn_login = Button(loginFrame, command = lambda: login(loginFrame, username, password), text = "Login", bg = '#FAEEE0', width = 20, height = 2, borderwidth = 3,
                       relief = "ridge", activebackground = '#F9E4C8', font = ('times', 15, 'bold'))
    btn_login.place(x = 300, y = 350)
    btn_register = Button(loginFrame, command = lambda: register_form(loginFrame), text = "Register", bg = '#FAEEE0', width = 20, height = 2, borderwidth = 3,
                       relief = "ridge", activebackground = '#F9E4C8', font = ('times', 15, 'bold'))
    btn_register.place(x = 600, y = 350)
    
    # Exit Protocol
    loginFrame.wm_protocol("WM_DELETE_WINDOW", lambda: exit(loginFrame, root))

def register_form(panel):
    # Create Register Window
    panel.withdraw()
    registerFrame = Toplevel()
    registerFrame.title("Register Portal")
    registerFrame.geometry('1000x500')
    registerFrame.configure(background = '#DBD0C0')

    # Display Labels
    lbl_username = Label(registerFrame, text = "Username:", bg = '#DBD0C0', font = ('times', 15, 'bold'))
    lbl_username.place(x = 300, y = 200)
    lbl_password = Label(registerFrame, text = "Password:", bg = '#DBD0C0', font = ('times', 15, 'bold'))
    lbl_password.place(x = 300, y = 250)
    lbl_firstname = Label(registerFrame, text = "Firstname:", bg = '#DBD0C0', font = ('times', 15, 'bold'))
    lbl_firstname.place(x = 300, y = 300)
    lbl_lastname = Label(registerFrame, text = "Lastname:", bg = '#DBD0C0', font = ('times', 15, 'bold'))
    lbl_lastname.place(x = 300, y = 350)

    # User Input
    username = Entry(registerFrame, bg = '#DBD0C0', font = ('times', 15, 'bold'), width = 40)
    username.place(x = 450, y = 200)
    password = Entry(registerFrame, bg = '#DBD0C0', font = ('times', 15, 'bold'), width = 40, show = "*")
    password.place(x = 450, y = 250)
    firstname = Entry(registerFrame, bg = '#DBD0C0', font = ('times', 15, 'bold'), width = 40)
    firstname.place(x = 450, y = 300)
    lastname = Entry(registerFrame, bg = '#DBD0C0', font = ('times', 15, 'bold'), width = 40)
    lastname.place(x = 450, y = 350)

    # Display Buttons
    btn_login = Button(registerFrame, command = lambda: register(username, password, firstname, lastname), text = "Register", bg = '#FAEEE0', width = 20, height = 2, borderwidth = 3,
                       relief = "ridge", activebackground = '#F9E4C8', font = ('times', 15, 'bold'))
    btn_login.place(x = 300, y = 400)
    lbl_register = Button(registerFrame, command = lambda: login_form(registerFrame), text = "Login", bg = '#FAEEE0', width = 20, height = 2, borderwidth = 3,
                       relief = "ridge", activebackground = '#F9E4C8', font = ('times', 15, 'bold'))
    lbl_register.place(x = 600, y = 400)
    
    # Exit Protocol
    registerFrame.wm_protocol("WM_DELETE_WINDOW", lambda: exit(registerFrame, root))

def register(username, password, firstname, lastname):
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()

    # Retrieve value from user input
    username = username.get()
    password = password.get()
    firstname = firstname.get()
    lastname = lastname.get()

    # User input validation
    if username == "" or password == "" or firstname == "" or lastname == "":
        warn = "Please complete the required field!"
        tkMessageBox.showerror('', warn)
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ?", [username])
        if cursor.fetchone() is not None:
            warn = "Username is already taken"
            tkMessageBox.showerror('', warn)
        else:
            cursor.execute("INSERT INTO `member` (username, password, firstname, lastname) VALUES(?, ?, ?, ?)", [username, password, firstname, lastname])
            conn.commit()
            tkMessageBox.showinfo('Account Status', 'Successfully Created!')
    cursor.close()
    conn.close()

def login(panel, username, password):
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()

    # Retrieve value from user input
    username = username.get()
    password = password.get()

    # User input validation
    if username == "":
        warn = "Username can't be empty!"
        tkMessageBox.showerror('', warn)
    elif password == "":
        warn = "Password can't be empty!"
        tkMessageBox.showerror('', warn)
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?", [username, password])
        if cursor.fetchone() is not None:         
            cursor.close()
            conn.close()
            tkMessageBox.showinfo('Login Status', 'Logged in Successfully!')
            chat_bot(panel)
        else:
            warn = "Invalid Username or password"
            tkMessageBox.showerror('', warn)

def chat_bot(panel):
    panel.withdraw()
    chatbotFrame = Toplevel()
    chatbotFrame.title("Chatbot")
    chatbotFrame.geometry('1000x500')
    chatbotFrame.configure(background = '#DBD0C0')

    chat_history = Text(chatbotFrame, state='disabled', wrap='word')
    chat_history.place(x = 50, y = 80)
    
    user_input = Entry(chatbotFrame, width = 100)
    user_input.place(x = 50, y = 50)
    user_input.bind('<Return>', lambda _: send_message(user_input, chat_history))
    
    btn_send = Button(chatbotFrame, text = "Send", command = lambda: send_message(user_input, chat_history))
    btn_send.place(x = 660, y = 50)

    # Exit Protocol
    chatbotFrame.wm_protocol("WM_DELETE_WINDOW", lambda: exit(chatbotFrame, panel))

    # TO DO:
        # Capture user input
        # Call training.py and pass down the user input to the chatbot function
        # Return respond and display in the screen

def send_message(user_input, chat_history):
    message = user_input.get()
    if message:
        user_input.delete(0, 'end')
        display_message(f"You: {message} \n", chat_history)
        # This function will not work I believe
            # response = chat_bot_function(message.lower())
        response = "dummy text \n"
        display_message(response, chat_history)

def display_message(message, chat_history):
    chat_history.configure(state='normal')
    chat_history.insert('end', message)
    chat_history.configure(state='disabled')

# Exit Toplevel Window Function
def exit(panel_old, panel_new):
    panel_old.withdraw()
    panel_new.deiconify()


# Exit Program Function
def on_closing():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()

#========================================INITIALIZATION===================================
if __name__ == '__main__':

    root = Tk()
    root.title("Chatbot System Started")
    
    width = 640
    height = 480
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)

    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)
    root.configure(background = '#FAEEE0')

    # Menubar Widget
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label = "Exit", command = on_closing)
    menubar.add_cascade(label = "File", menu = filemenu)
    root.config(menu = menubar)

    database()
    chat_bot(root)
    root.mainloop()
   
