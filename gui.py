from tkinter import *
import tkinter.filedialog
import lifelib, os, sys, math, imageio

sess = lifelib.load_rules('b3s23')
lt = sess.lifetree(n_layers = 1, memory = 1000)

def clean_files():
    #Delete old image files from /img.
    imagefiles = os.listdir(os.getcwd() +'/img')
    for x in imagefiles:
        os.remove(os.getcwd() + '/img/' + x)
window = Tk()
window.minsize(800, 600)
window.title('GUI')

#Object frontend:
#window.mainloop()
def makeimage(apgcode):
    pt = lt.pattern(apgcode)
    image = pt.make_gif(filename = os.getcwd() + '/img/' + apgcode + '.gif')
#def makeobjpage(apgcode):
apgcode = 'xs5_253'
#Create the frontend for a given apgcode.
makeimage(apgcode)
imgfile=os.getcwd() + '/img/'+apgcode+'.gif'
photo = PhotoImage(file=imgfile)
print(imgfile)
print(photo)
photolabel = Label(window, image=photo)
photolabel.pack()
photolabel.place(x=0,y=0)
    #photolabel.place(x=0,y=0)

apgcodelabel = Label(window, text = apgcode, font = ('Arial', 25))
apgcodelabel.pack()
apgcodelabel.place(x=350,y=0)
##makeobjpage('xs5_253')
window.mainloop()
    


