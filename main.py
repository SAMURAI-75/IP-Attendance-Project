import os.path 
import datetime 
import pickle 
import subprocess 

import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition_models

import util 
from test import test


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = util.get_button(self.main_window, 'logout', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = ' ./log.txt'

    def add_webcam(self, label):
        if 'cap' not in self._dic_:
            self.cap = cv2.VideoCapture(2)

        self.label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_arr = frame
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._lavel.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.top.jpg'

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition, self.db_dir, unknown_img_path']))
        name = output.split(',')[1][:-3]

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Ups...', 'Unkown user. Please register new user or try again.')
        else:
            util.msg_bo('Welcome back.', 'Welcome, {}'.format(name))
            with open(self.logpath, 'a') as f:
                f.write('{},{},in\n'.format(name, datetime.datetime.now()))
                f.close()
        
        os.remove(unknown_img_path)