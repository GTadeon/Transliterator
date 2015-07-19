# -*- coding: utf-8 -*-
#Transliterator_OOP solucija

from Tkinter import*
import tkMessageBox
from tkFileDialog import askopenfilename, asksaveasfile
from PIL import Image, ImageTk, ImageDraw
import ImageGrab 
import os 
import subprocess

#-------------------------------------------------------------K L A S A-------------------------------------------------------------------

class Aplikacija:
    def __init__(self,master):
        self.master=master
        master.title("TRANSLITERATOR (OVP)")
        master.geometry("600x500+350+100")
        Aplikacija.MENU(self)
        Aplikacija.WIDGETI(self)
        return
    

    def info(self):
        tkMessageBox.showinfo(title="O Transliteratoru", message="Ovo je druga verzija programa (29.4.2015.)\nTrenutni najveci dozvoljeni unos iz tekstne datoteke: 36znakova po retku,max 7 redaka;ukupno:252znaka\npreporuca se ucitavanje utf8 kodiranih  .txt datoteka\nautor: Ivan Grobenski\nkontakt: ivgroben@ffzg.hr")
        return
    
    def zatvori(self):
        self.zatvaranje=tkMessageBox.askyesno(title="Zatvaranje programa ",message="Jeste li sigurni? ") #ovo vraca True ako korisnik stisne yes
        if self.zatvaranje==True:
            self.master.destroy()
            return

    def VratiEntry(self):
        self.kanvas3=Canvas(self.master,height=120,width=400,bg="#F0F0F0").place(x="7",y="20")
        self.entry=Entry(self.master,textvariable=self.Tekst,width=60).place(x="10",y="30")
        return
        
    def otvori(self): 
        self.ime_fajla=askopenfilename()
        if len(open(self.ime_fajla).read().decode('utf8'))>252:
            tkMessageBox.showwarning(title="Nedozvoljen unos",message="Tekstna datoteka (u ovoj verziji programa) smije imati najvise 252 znaka.")
        
        self.TekstDisplej=open(self.ime_fajla).read()
        self.kanvas2=Canvas(self.master,height=120,width=400,bg="#e0e0e0").place(x="7",y="20")
        lejbl2=Label(self.master,text=self.TekstDisplej,bg="#e0e0e0").place(x="60",y="23")
        
        vratiEntry=Button(self.master,text="EntryBox",command=self.VratiEntry).place(x="335",y="160") #vraca entrybox unos
        self.Tekst.set(open(self.ime_fajla).read())
        return


    def MENU(self):
        self.moj_meni=Menu(self.master)
        # File menu
        self.file_izbornik=Menu(self.moj_meni,tearoff=0)
        self.file_izbornik.add_command(label="Otvori",command=self.otvori) 
        self.file_izbornik.add_command(label="Izlaz", command=self.zatvori)
        self.moj_meni.add_cascade(label="File",menu=self.file_izbornik)  
        self.master.config(menu=self.moj_meni)
        # Help menu
        self.help_izbornik=Menu(self.moj_meni,tearoff=0)
        self.help_izbornik.add_command(label="O transliteratoru",command=self.info)
        self.moj_meni.add_cascade(label="Help",menu=self.help_izbornik)  
        self.master.config(menu=self.moj_meni)
        return

    
    def prevedi(self):
        rj={"\n":"razmak.png"," ":"razmak.png","a":"a.png",'b':"b.png",'c':'c.png','d':'d.png',u'č':u'č.png',u'ć':u'ć.png','e':'e.png','f':'f.png','g':'g.png','h':'h.png','i':'i.png','j':'j.png','k':'k.png','l':'l.png','m':'m.png','n':'n.png','o':'o.png','p':'p.png','r':'r.png','s':'s.png',u'š':u'š.png','t':'t.png','u':'u.png','v':'v.png','z':'z.png',u'ž':u'ž.png',u'đ':u'đ.png'}
        
        if 0<len(self.Tekst.get())<252:
            self.kanvas=Canvas(self.master,height=200,width=570,bg="#F2EEB3").place(x="7",y="225")

            self.x_kord=[5, 20, 35, 50, 65, 80, 95, 110, 125, 140, 155, 170, 185, 200, 215, 230, 245, 260, 275, 290, 305, 320, 335, 350, 365, 380, 395, 410, 425, 440, 455, 470, 485, 500, 515, 530, 545]
            self.y_kord=[225, 255, 285, 315, 345, 375, 405]
            
            self.k=0 #redni broj slova/slike po redu
            self.novi_red=0
            
            for slovo in self.Tekst.get().lower():
                if slovo in rj.keys():
                    self.load=Image.open(rj[slovo])
                    self.load=self.load.resize((15,25), Image.ANTIALIAS)
                    self.render=ImageTk.PhotoImage(self.load)
                    
                    self.k+=1
                    
                    for apcisa in range(self.k):
                        self.img=Label(self.master,image = self.render)
                        self.img.image = self.render
                        self.img.place(x=self.x_kord[self.k],y=self.y_kord[self.novi_red])
                    if (slovo=="\n") or (self.x_kord[self.k]==545): #provjera prijelaza u novi red
                        self.k=0
                        self.novi_red+=1 #cupanje nove y kord. za novi red                                   
                
        else:tkMessageBox.showwarning(title="Nedozvoljen unos",message="U ovoj verziji programa uneseni tekst smije sadrzavati najmanje 1, a najvise 252 znaka")
        return


    def ciscenje(self):
        self.kanvas=Canvas(self.master,height=201,width=570,bg="#F2EEB3").place(x="7",y="225")
        return
    
    def ScreenShotanje(self):
        #funkcija za screen shot canvasa s prevedenim tekstom
        self.slika=Image.open("slika.png") 
        self.slika=self.slika.resize((20,20),Image.ANTIALIAS)
        self.render=ImageTk.PhotoImage(self.slika)
        self.spremanje_slike= Button(self.master,image=self.render,command=spremanje)    
        self.spremanje_slike.image=self.render
        self.spremanje_slike.place(x="490",y="440")
        return
    
    def WIDGETI(self):
        #entry box, gumbi, kanvas:
        self.Tekst=StringVar()
        self.entry=Entry(self.master,textvariable=self.Tekst,width=60).place(x="10",y="30")
    
        self.gumb=Button(self.master,text="Prevedi!",command=self.prevedi).place(x="20",y="160")
        self.kanvas=Canvas(self.master,height=200,width=570,bg="#F2EEB3").place(x="7",y="225")
        self.lejbl=Label(self.master,text="Unesite tekst: ").place(x="7",y="3")
        
        self.ocisti=Button(self.master,text="Ocisti sve",command=self.ciscenje).place(x="7",y="440") #gumb za brisanje sadrzaja kanvasa
        
        self.ScreenShotanje()
        return

def spremanje(): 
    im=ImageGrab.grab(bbox=(375,377,940,580)) # X1,Y1,X2,Y2 screenshota
    pitaj = asksaveasfile(mode='w', defaultextension=".jpeg")
    output = pitaj.name #bez .name ne radi...
    im.save(output) #sprema sliku na lokaciju 
    putanjaFajla = os.path.abspath(output)  #otvara sliku u novom prozoru
    subprocess.Popen(r'explorer /select,"'+putanjaFajla+'"')
    return

#-------------------------------------------------------------I N S T A N C I R A NJ E--------------------------------------------------------------------
def main():
    root=Tk()
    app=Aplikacija(root)
    root.mainloop()
    return

main()
