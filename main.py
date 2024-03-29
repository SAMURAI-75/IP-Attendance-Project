#Kenny


#Librearies need to be installed
import pandas as pd
import matplotlib.pyplot as plt
import os.path 
import time
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
        self.main_window.geometry("1200x520+200+100")

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'gray', self.login, fg = 'black')
        self.login_button_main_window.place(x=800, y=100)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=800, y=250)

        self.users_list_button_main_window = util.get_button(self.main_window, 'Attendance', 'gray',self.user_list, fg='black')
        self.users_list_button_main_window.place(x = 800, y = 400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        
        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'


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
        
        unknown_img_path = "/Users/fouzan/Documents/Python Projects/IP Project/.face.jpg"
        
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        output = str(subprocess.check_output(['face_recognition', self.db_dir,unknown_img_path]))
        print(output)
        n1 = output.split(',')[::-1]
        n2 = n1[0].split('\\')

        namedis = "Welcome" , n2[0]
        
        print(n2[0])
        
        
        if n2[0] == 'unknown_person' or n2[0] == 'no_persons_found' :
            util.msg_box("Login", 'Unkown Person Login Attempt')
                         
        else:
            util.msg_box("Login", namedis)
            f = open("log.txt", "a")
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            l = [str(n2[0]) ,' ', str(current_time), "\n"]
            fin = ''
            for i in l:
                fin += (i)
            f.write(str(fin))

        os.remove(unknown_img_path)

#Fouzan

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+220+120")
        
        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'grey', self.accept_register_new_user , fg = 'black')
        self.accept_button_register_new_user_window.place(x = 750, y = 300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try Again', 'grey', self.try_again_register_new_user , fg = 'black')
        self.try_again_button_register_new_user_window.place(x = 750, y = 400)


        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)


        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x = 750, y = 150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window,"Please Enter Your Name:")
        self.text_label_register_new_user.place(x = 750, y = 100)


    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()


    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)


        self.register_new_user_capture = Image.fromarray(self.most_recent_capture_arr)



    def start(self):
        self.main_window.mainloop()


    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0 , "end-1c")
        if name == '':
            util.msg_box('No Name','No name was provided')
            self.register_new_user_window.destroy()
        else:
            
            cv2.imwrite(os.path.join(self.db_dir , '{}.jpg'.format(name)) , np.array(self.register_new_user_capture))

            util.msg_box('Success!' , 'User was registered successfully')

            self.register_new_user_window.destroy()

    def user_list(self):

        def live_graph():
            
            #extracting info from table and making a dataframe
            list_of_lines = []

            with open('log.txt') as f:
                lines = f.readlines()
                for i in lines:
                    list_of_lines.append(i.split())

            df = pd.DataFrame(list_of_lines,columns = ['Name','Date'])

            dfnames = df.groupby('Name')

            #graphs

            line = plt.plot(dfnames.size())
            plt.grid(True)
            #histogram = dfnames.size().plot(kind='hist')
            plt.title('Students Attendance Overall')
            plt.show()
        
        def sample_data_graph():

            #predefined values to create graphs
            import pandas as pd
            import numpy as np
            import matplotlib.pyplot as plt
            series1 = pd.Series([80,92,76,64,93],index=["Zanwar", "Leo", "Tasneem","Ryan","Hannah"])
            series2 = pd.Series([70,82,62,82,76],index=["Zanwar", "Leo", "Tasneem","Ryan","Hannah"])
            series3 = pd.Series([94,72,95,88,67],index=["Zanwar", "Leo", "Tasneem","Ryan","Hannah"])
            series4 = pd.Series([77,85,69,93,57],index=["Zanwar", "Leo", "Tasneem","Ryan","Hannah"])
            series5 = pd.Series([97,74,83,68,97],index=["Zanwar", "Leo", "Tasneem","Ryan","Hannah"])
            df = pd.DataFrame([series1, series2, series3, series4, series5], index= ["Jan","Feb","Mar","Apr","May"])
            print("Example 1:", df)
            df.plot(kind='bar', title='Attendance')
            plt.xlabel("Months")
            plt.ylabel('Percentage')
            plt.show()
            series6 = pd.Series([79,92,85,88], index=["Jan", "Feb", "Mar", "Apr"])
            print("Example 2:")
            print("Attendance% of Leo are:", series6)
            df1 = pd.DataFrame(series6)
            df1.plot(kind='bar', title='Leo Attendance%')
            plt.show()
            series7= pd.Series([79,97,87,83], index=["Jan", "Feb", "Mar","Apr"])
            series8= pd.Series([89,83,92,77], index=["Jan","Feb","Mar","Apr"])
            df2 = pd.DataFrame([series7,series8], index=["Leo", "Keanu"])
            print("Example 3:")
            print(df2)
            df2.plot(kind='bar', title="Attendance% of Leo and Keanu")
            plt.xlabel("Months")
            plt.ylabel("Percentage")
            plt.show()
            print("Example 4:")
            df.plot(kind='line', title="Attendance(Line graph)")
            plt.xlabel("Months")
            plt.ylabel("Percentage")
            plt.show()
            print("Example 5:")
            df.plot(kind='line', marker="*", markersize=10, linewidth=3, linestyle="--")
            plt.grid(True)
            plt.show()


        live_graph()
        sample_data_graph()


if __name__ == "__main__": #idk what this means
    app = App()
    app.start()

