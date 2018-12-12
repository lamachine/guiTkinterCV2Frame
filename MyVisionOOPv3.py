#!/usr/bin/python
# -*- coding: utf-8 -*-
import tkinter as tk
import datetime
from tkinter import ttk
from tkinter import filedialog
from tkinter.tix import *
import cv2
import argparse
from PIL import Image, ImageTk
import matplotlib
matplotlib.use('TkAgg')  # Backend change needed later, normally default is OK
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2TkAgg
from matplotlib.figure import Figure

LARGE_FONT = ('Verdana', 16)
MEDIUM_FONT = ('Verdana', 12)
SMALL_FONT = ('Verdana', 9)


def select_image():
    pass

class DoorGreeterCapture(tk.Tk):  # this class inherits from Tk

    def __init__(self):

        # self is standard name,
        # args are non-keyword arguments, variable and unknown qty
        # kwargs are key-work arguments, named and expected, typically dictionaries
        
        tk.Tk.__init__(self)

            # Changes to use ttk for better look across platforms
#        tk.Tk.iconbitmap(self,default='clienticon.ico')

        tk.Tk.wm_title(self, 'Door Greeter Application')

        container = tk.Frame(self)  # defining the object "container"

        container.pack(side='top', fill='both', expand=True)

                # pack (and grid) both populates and places your objects
                # pack is general and tight-fitting, grid is controlled locations

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  # dictionary ?? of all our frames

        for F in (SplashPage, CapturePage, IDPage, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(SplashPage)  # makes it visible in the start page


        menu = tk.Menu(self)
        self.config(menu=menu)

        file = tk.Menu(menu)
        file.add_command(label="Open Image", command = self.client_selectFile)
        file.add_command(label="Exit", command = self.client_exit)
        menu.add_cascade(label="File", menu=file)

        edit = tk.Menu(menu)
        edit.add_command(label="Copy")#, command = self.client_exit)
        edit.add_command(label="Show Image")#, command = self.show_img)
        edit.add_command(label="Show Text")#, command = self.show_txt)
        menu.add_cascade(label="Edit", menu=edit)

        pagelist = tk.Menu(menu)
        pagelist.add_command(label="Splash", command = self.show_frame(SplashPage))
        pagelist.add_command(label="Learning Video", command = self.show_frame(CapturePage))
        pagelist.add_command(label="Taught Video", command = self.show_frame(IDPage))
        menu.add_cascade(label="Page", menu=pagelist)

    def show_frame(self, cont):  # this is the function we called above

        frame = self.frames[cont]
        frame.tkraise()  # literally raises the frame to the top for visibilitys

    def client_exit(self):
        #CapturePage.vs.release()
        exit()

    def client_selectFile(self):
        self.path = filedialog.askopenfilename()
        


# a quick demo of passing a function with paramters

def qf(quickPrint):
    print(quickPrint)


class SplashPage(tk.Frame):

    def __init__(self, parent, controller):  #
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Start page', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Go to Capture Page',
                             command=lambda : \
                             controller.show_frame(CapturePage))
        button1.pack()

        button2 = ttk.Button(self, text='Go to Data Validation Page',
                             command=lambda : \
                             controller.show_frame(IDPage))
        button2.pack()

        button3 = ttk.Button(self, text='Go to graph page',
                             command=lambda : \
                             controller.show_frame(PageThree))
        button3.pack()


class CapturePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.vs = cv2.VideoCapture(0) # capture video frames, 0 is your default video camera
        self.output_path = './'  # store output path
        self.current_image = None  # current image from the camera

        #self.root = tk.Tk()  # initialize root window
        #self.protocol('WM_DELETE_WINDOW', self.destructor)

        self.panel = tk.Label(self)  # initialize image panel
        self.panel.grid(row=0, padx=10, pady=10)

        # create a button, that when pressed, will take the current frame and save it to file
        btn = ttk.Button(self, text="Snapshot!", command=self.take_snapshot)
        btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        button2 = ttk.Button(self, text='Go to Splash page',
                             command=lambda : \
                             controller.show_frame(SplashPage))
        button2.grid(row=1, column=1, padx=10, pady=10)

        # start a self.video_loop that constantly poles the video sensor
        # for the most recently read frame
        self.video_loop()

    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image
        self.after(30, self.video_loop)  # call the same function after 30 milliseconds

    def take_snapshot(self):
    
        """ Take snapshot and save it to the file """
        ts = datetime.datetime.now() # grab the current timestamp
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        p = os.path.join(self.output_path, filename)  # construct output path
        ret, snap = self.vs.read()

        if ret:
            cv2.imwrite("frame-" + filename , cv2.cvtColor(snap, cv2.COLOR_RGB2GRAY))

        #self.current_image.save(p, "JPEG")  # save image as jpeg file
        print("Image saved to " + filename + ".jpg")

    def destructor(self):
        """ Destroy the root object and release all resources """
        print("[INFO] closing...")
        self.destroy()
        #self.vs.release()  # release web camera
        #cv2.destroyAllWindows()  # it is not mandatory in this application


class IDPage(tk.Frame):
    


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Identification Page',
                          font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        panelA = None
        panelB = None

        button1 = ttk.Button(self, text='Back to Capture Page',
                             command=lambda : \
                             controller.show_frame(CapturePage))
        button1.pack()

        button2 = ttk.Button(self, text='Back to Start Page!!!',
                             command=lambda : \
                             controller.show_frame(SplashPage))
        button2.pack()

        button3 = ttk.Button(self, text='Select an image',
                             command=select_image)
        button3.pack()

        


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Graph Page!', font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text='Back to Start Page!!!',
                             command=lambda : \
                             controller.show_frame(SplashPage))
        button1.pack()

        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8],
               [5, 6, 1, 3, 8, 9, 3, 5])

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH,
                                    expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

panelA=None
panelB=None


#app = DoorGreeterCapture()
#app.mainloop()
if __name__ =="__main__":
    app = DoorGreeterCapture()
    app.mainloop
			
