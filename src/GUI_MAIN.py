# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import thread
import multiprocessing
from multiprocessing import Process
import main_flush
def ref_flush_main_dot_main(argv):
    print 1+1
    main_flush.main([])
    pass
def thread_start_multiprocess(argv):
    p = Process(target=ref_flush_main_dot_main, args=([],))
    p.start()
def start_main_flush():
    try:
        #thread.start_new_thread( main_flush.main, ([],) )
        #thread.start_new_thread( thread_start_multiprocess, ([],) )
        
        p = Process(target=ref_flush_main_dot_main, args=([],))
        p.start()
    except Exception as ex:
        print "unable to start flush",ex
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        #self.nameInput = Entry(self)
        #self.nameInput.pack()
        self.alertButton = Button(self, text='Start', command=start_main_flush)
        self.alertButton.pack()

    def hello(self):
        name = self.nameInput.get() or 'world'
        tkMessageBox.showinfo('Message', 'Hello, %s' % name)

        

def gui_main():
    rootw = Tk()
    rootw.geometry('200x100') 
    app = Application(rootw)
    # 设置窗口标题:
    app.master.title('Flush12306')
    # 主消息循环:
    rootw.mainloop()
    
if __name__=='__main__':
    #gui_main(sys.argv[1:])
    multiprocessing.freeze_support() 
    gui_main()