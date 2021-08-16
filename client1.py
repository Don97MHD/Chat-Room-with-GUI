#importing libraries
import tkinter
import socket
import threading
from tkinter import simpledialog, scrolledtext, filedialog
import random

#handle send text
def handle_send():
    try:
        msg = input_area.get('1.0', 'end')
        client_sock.send(msg.encode('utf-8'))
        input_area.delete('1.0', 'end')

    except socket.error as err:
        tkinter.Label(window, text=err, fg='white', bg='red').pack()

#handle send image file
def upload_file():
    filename = filedialog.askopenfilename(filetypes=[('Image Files', '*jpg'),('Image Files', '*jpeg'),('Image Files', '*png')])
    file = open(filename, 'rb')
    filedata = file.read()
    client_sock_file.sendall(filedata)
    file.close()

#shutdown program
def handle_stop():
    window.destroy()
    client_sock.close()
    client_sock_file.close()
    exit(0)

#define ask to enter username
windowask = tkinter.Tk()
windowask.withdraw()
#string value is intered
username = simpledialog.askstring('UserName', 'enter your name', parent=windowask)
#define main window
window = tkinter.Tk()
#title of window
window.title('Chat Room')
# background color
window['bg'] = '#7610B8'
#difine label on window
chat_label = tkinter.Label(window, text='CHATTING:', bg='grey')
#make that label show on window
chat_label.pack(padx=20, pady=5)
#difine box for text with scoral bar
txt = scrolledtext.ScrolledText(window, width=100, state='disabled')
#make this box show on window
txt.pack(padx=20, pady=5)
message_label = tkinter.Label(window, text='Message: ', bg='grey')
message_label.pack(padx=20, pady=5)
#make box for inter text to program
input_area = tkinter.Text(window, height=3)
input_area.pack(padx=20, pady=5)
#make bottoms
send_buttom = tkinter.Button(window, text='send', bg='lightblue', command=handle_send)
send_buttom.pack(padx=20, pady=5)
stop_buttom = tkinter.Button(window, text='Quit', bg='red', command=handle_stop)
stop_buttom.pack(padx=20, pady=5)
file_buttom = tkinter.Button(window, text='send photo', bg='lightblue', command=upload_file)
file_buttom.pack(padx=20, pady=5)

#handle ricievng files
def handle_recieve_file():
    while True:
        try:
            #recieve file data at max size 1MB
            file_msg = client_sock_file.recv(1000000)
            #make file on client device with random name
            randomname=str(int(1000*random.random()))+'.jpg'
            filename = open(randomname, 'wb')
            filename.write(file_msg)
            filename.close()
        except socket.error as err:
            client_sock_file.close()
            #print err message on window as label
            tkinter.Label(window,text=err,fg='white',bg='red')

            break
#handle recive text messages
def handle_recieve():
    while True:
        try:
            message = client_sock.recv(1024).decode('utf-8')
            #make box text activated to print message on it
            txt['state'] = 'normal'
            #print message on box
            txt.insert('end', message)
            #make each message show under the another
            txt.yview('end')
            #return box state to disabled to prevent edit it
            txt['state'] = 'disabled'
        except socket.error as err:
            client_sock.close()
            tkinter.Label(window, text=err, fg='white', bg='red').pack()
            break

#create two socket for text messages and image messages
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock_file = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    #connect each socket to server
    client_sock.connect(('127.0.0.1', 5555))
    #the first step is to send username to server
    client_sock.send(username.encode('utf-8'))
    client_sock_file.connect(('127.0.0.1', 5556))
except socket.error as err:
    tkinter.Label(window, text=err, fg='white', bg='red').pack()
#create threads to handle recive
th2 = threading.Thread(target=handle_recieve)
th_file = threading.Thread(target=handle_recieve_file)
#start threads
th2.start()
th_file.start()
#make the window awlways displays
window.mainloop()