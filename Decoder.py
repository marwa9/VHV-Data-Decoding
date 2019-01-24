#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from Tkinter import *
import ttk
import os
import binascii
import math
import parseur

#################################################
#   EMV/Retail Tag decoder                      #
#   Version 1.0                                 #
#   By Telnet                                   #
#################################################


FORMAT_a = """
Alphabetic data elements contain a single character per byte. The permitted characters are alphabetic only (a to z and A to Z, upper and lower case).
"""
FORMAT_an ="""
Alphanumeric data elements contain a single character per byte. Thepermitted characters are alphabetic (a to z and A to Z, upper and lower case) and numeric (0 to 9).
"""
FORMAT_ans ="""
Alphanumeric Special data elements contain a single character per byte. The permitted characters and their coding are shown in the Common  Character Set table in Annex B of Book 4.
     There is one exception: The permitted characters for Application Preferred Name are the non-control characters defined in the ISO/IEC 8859 part designated in the Issuer Code Table Index associated
     with the Application Preferred Name.
"""
FORMAT_b ="""
These data elements consist of either unsigned binary numbers or bit combinations that are defined elsewhere in the specification.
"""
FORMAT_cn ="""
Compressed numeric data elements consist of two numeric digits(having values in the range Hex 0 to 9) per byte. These data elementsare left justified and padded with trailing hexadecimal F.
"""
FORMAT_n ="""
Numeric data elements consist of two numeric digits (having values in the range Hex 0 to 9) per byte. These digits are right justified and padded with leading hexadecimal zeroes. Other specifications
sometimes refer to this data format as Binary Coded Decimal (BCD) or unsigned packed.
"""
FORMAT_var ="""
Variable data elements are variable length and may contain any bit combination. Additional information on the formats of specific variable data elements is available elsewhere.
"""

ABOUT ="""
EMV/Retail Tag decoder  
Version 1.0
"""

HELP ="""
Please Read the READ_ME file
"""

TAG_WITH_IMAGE = ['9F27', '9F34','9F35']
def tag_has_image(tag):
    result = 0
    for  t in TAG_WITH_IMAGE:
        if t == tag:
            result = 1
            break
    return result
    

def format_promt():
    toplevel = Toplevel()
    toplevel.title("Data Format")
    format_type = ['a','an','ans','b','cn','n','var']
    format_text = [FORMAT_a,FORMAT_an,FORMAT_ans,FORMAT_b,FORMAT_cn,FORMAT_n,FORMAT_var]
    r = 0
    while r < 7:
        Label(toplevel, text=format_type[r], relief=RIDGE ,width=15).grid(row=r,column=0)
        Label(toplevel, text=format_text[r], relief=SUNKEN,width=150).grid(row=r,column=1)
        r = r + 1

def about_promt():
    toplevel = Toplevel()
    Label(toplevel, text=ABOUT, relief=RIDGE ,width=30).grid(row=0,column=0)
    toplevel.title("About")

def about_help():
    toplevel = Toplevel()
    Label(toplevel, text=HELP, relief=RIDGE ,width=30).grid(row=0,column=0)
    toplevel.title("Help")
    
def bcd_to_int(x):
    """
    This translates binary coded decimal into an integer
    TODO - more efficient algorithm
    >>> bcd_to_int(4)
    4
    >>> bcd_to_int(159)
    345
    """

    if x < 0:
        raise ValueError("Cannot be a negative integer")

    binstring = ''
    while True:
        q, r = divmod(x, 10)
        nibble = bin(r).replace('0b', "")
        while len(nibble) < 4:
            nibble = '0' + nibble
        binstring = nibble + binstring
        if q == 0:
            break
        else:
            x = q

    return int(binstring, 2)


def int_to_bcd(x):
    """
    This translates an integer into
    binary coded decimal
    >>> int_to_bcd(4)
    4
    >>> int_to_bcd(34)
    22
    """

    if x==0: return 0
    if x < 0:
        raise ValueError("Cannot be a negative integer")

    bcdstring = ''
    while x > 0:
        nibble = x % 16
        bcdstring = str(nibble) + bcdstring
        x >>= 4
    return int(bcdstring)


def StringToInt(strString):
    if (len(strString)>1): 
        if strString[:2]=="0x": return int(strString, 16)
    return int(strString)

def StringToHex(strString):
    return ''.join('%0.2X' % ord(x) for x in strString)

def DataToValue(strData, strType):
    #If type is numeric but Data is not numeric 
    if strType in lstNummericTypes:
        if strData[:2] !="0x" and not strData.isdigit(): return strData
    
    return StringToInt(strData)

def openFile():
    os.startfile(".\\HEXwrite.exe")
    
class Interface(Frame):
    
    """ This is the main window. 
    all widgets are introduced as attribute to this window"""
    def OnValidatevalue(self, P, d):
        valid_hex_char = lambda c: c in 'abcdef0123456789'
        return (len(P) < 5) and (all(valid_hex_char(z) for z in P.lower()))
    
    def __init__(self, fenetre, **kwargs): #Default variables
        self.rep_server = ''
        self.value_state = "disabled"
        self.text_server = ''
        self.etat = "EMV Tag Dictionary"
        self.XMLParseur = parseur.Parseur()
        self.XMLSection = 0
        
        
        Frame.__init__(self, fenetre, width=800, height=800, **kwargs)
        self.grid()
                
        #
        # Create widgets
        #
        
        # Menu
        self.menubar = Menu(self)

        filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Contact", command =self.update_etat_contact)
        filemenu.add_command(label="Contactless", command =self.update_etat_cless)
        filemenu.add_command(label="Retail", command =self.update_etat_retail)
        filemenu.add_command(label="Exit", command=self.quitter)

        Toolmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools", menu=Toolmenu)
        Toolmenu.add_command(label="Format", command=format_promt)
        Toolmenu.add_command(label="HexAscii", command=openFile)

        Helpmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=Helpmenu)
        Helpmenu.add_command(label="Help", command=about_help)
        Helpmenu.add_command(label="About", command=about_promt)       
        
        self.master.config(menu=self.menubar)
        
        # label 
        self.label_etat = Label(self, width=35, text=self.etat, fg = "black", font = "Helvetica 11 bold")
        self.label_etat.grid(column=0, row=0, columnspan=4, sticky=W, padx=5, pady=5)
        

        # Separator 
        self.separator_label = ttk.Separator(self, orient=HORIZONTAL)
        self.separator_label.grid(column=0, row=1, columnspan=4, sticky="ew")

        # label 
        self.label_select = Label(self, width=35, text="Select TAG:")
        self.label_select.grid(column=0, row=3, sticky="ew")

        # label 
        self.label_set_value = Label(self, width=20, text="Set Hex Value:")
        self.label_set_value.grid(column=1, row=3, sticky=W)
        
        #Combobox
        self.box_value = StringVar()
        self.box = ttk.Combobox(self, textvariable=self.box_value)
        self.box.bind('<<ComboboxSelected>>',self.get_information)
        self.box['values'] = self.XMLParseur.liste_tag_by_section(self.XMLSection)
        self.box.grid(column=0, row=4)

        # Value Entry
        self.var_value = StringVar()
        vcdmhex = (self.register(self.OnValidatevalue), '%P', '%d')
        self.entree_host = Entry(self, textvariable=self.var_value, width=20, state=self.value_state, validatecommand=vcdmhex)
        self.entree_host.grid(column=1, row=4, sticky=W)
        self.entree_host.bind("<Return>",self.decode_value)

        # button decode
        self.button_parse = Button(self,text=u"Parse",state=self.value_state, command=self.decode)
        self.button_parse.grid(column=2,row=4)

        # button help
        self.button_help = Button(self,text=u"Help",state=self.value_state, command=self.help_prompt)
        self.button_help.grid(column=3,row=4)
        
        #espace serveur
        self.espace_info = Listbox(self, width=80, height=20)
        self.espace_info.grid(column=0, row=5, columnspan=4, pady=5)
        self.espace_info.insert(END, self.text_server)	       

    def quitter(self):
        self.master.destroy()

    def insert_tag_info(self, dest, source):
        dest.delete(0,END)
        text = "--------------------------------------------------------------------------------------"
        dest.insert(END, text)
        text = "TAG:         0x" + source[0] 
        dest.insert(END, text)
        text = "NAME:      " + source[1]
        dest.insert(END, text)
        text = "FORMAT:      " + source[2]
        dest.insert(END, text)
        text = "LENGTH:      " + source[3]
        dest.insert(END, text)
        text = "DESCRIPTION: "
        dest.insert(END, text)
        text =  source[4]
        dest.insert(END, text)
        text = "--------------------------------------------------------------------------------------"
        dest.insert(END, text)
        
    def get_information(self, *event):
        tag = self.box_value.get()
        self.insert_tag_info(self.espace_info, self.XMLParseur.get_information(tag));
        if(int(self.XMLParseur.get_information(tag)[5]) == 1):
            self.value_state = "normal"
        else:
           self.value_state = "disabled"     
        self.entree_host['state'] = self.value_state
        self.button_parse['state'] = self.value_state
        if(tag_has_image(tag) == 1):
            self.button_help['state'] = "normal"
        else:
            self.button_help['state'] = "disabled"
      
    def update_etat_cless(self):
        self.etat = "Cless Tag Dictionary"
        self.label_etat['text'] = self.etat
        self.XMLSection = 1
        self.box['values'] = self.XMLParseur.liste_tag_by_section(self.XMLSection)
        
    def update_etat_contact(self):
        self.etat = "EMV Tag Dictionary"
        self.label_etat['text'] = self.etat 
        self.XMLSection = 0
        self.box['values'] = self.XMLParseur.liste_tag_by_section(self.XMLSection)

    def update_etat_retail(self):
        self.etat = "Retail Tag Dictionary"
        self.label_etat['text'] = self.etat
        self.XMLSection = 2
        self.box['values'] = self.XMLParseur.liste_tag_by_section(self.XMLSection)
        
    def decode_value(self, event):
        value = self.var_value.get()
        tag = self.box_value.get()
        tag_info_list = self.XMLParseur.get_information(tag)
        tag_items_list = self.XMLParseur.get_items(tag)
        print (StringToInt(value))
        
    def help_prompt(self):
        path = ".\\BMP\\" +self.box_value.get() + ".bmp" 
        logo = BitmapImage(file='9F27.xbm', foreground='red')
        toplevel = Toplevel()
        Label(toplevel, image=logo).grid()

    def decode(self):
        tag = self.box_value.get()
        information = self.XMLParseur.get_information(tag)
        index_list = self.XMLParseur.get_items(tag)
        value = self.var_value.get()
        
# Run the Decoder UI
fenetre = Tk()
fenetre.title("Decoder")
prog = Interface(fenetre)
prog.mainloop()

