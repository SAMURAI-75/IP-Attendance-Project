#Kenny


#Librearies need to be installed
import os.path 
import datetime 
import pickle 
import subprocess 
import numpy as np
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition_models

import util 
#from test import test


#blueprint for creating objects
class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'gray', self.login, fg = 'black')
        self.login_button_main_window.place(x=750, y=200)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        
        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = ' ./log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr,cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):

        unknown_img_path = './.face.jpg'
        
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition, self.db_dir, unknown_img_path']))
        name = output.split(',')[1][:-3]

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Oh no...', 'Unkown user. Please register new user or try again.')
        else:
            util.msg_box('Welcome back.', 'Welcome, {}'.format(name))
            with open(self.logpath, 'a') as f:
                f.write('{},{},\n'.format(name, datetime.datetime.now()))
                f.close()
        
        os.remove(unknown_img_path)

#Fouzan

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")
        
        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'grey', self.accept_register_new_user , fg = 'black')
        self.accept_button_register_new_user_window.place(x = 750, y = 300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'grey', self.try_again_register_new_user , fg = 'black')
        self.accept_button_register_new_user_window.place(x = 750, y = 300)


        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)


        self.add_img_to_label(self.capture_label)

        #bard code
        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)

        self.entry_text_register_new_user.place(x = 750, y = 150)

        self.text_label_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.text_label_register_new_user.place(x = 750, y = 70)


    def try_again_register_new_user(self):
        self.register_new_user_window_destroy()


    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        #bard code
        self.register_new_user_capture = Image.fromarray(self.most_recent_capture_arr)



    def start(self):
        self.main_window.mainloop()


    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0 , "end-1c")

        #bard code
        cv2.imwrite(os.path.join(self.db_dir , '{}.jpg'.format(name)) , np.array(self.register_new_user_capture))

        util.msg_box('Success!' , 'User was registered successfully')

        self.register_new_user_window.destroy()

if __name__ == "__main__": #idk what this means
    app = App()
    app.start()
