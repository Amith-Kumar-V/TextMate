# -*- coding: utf-8 -*-
import Tkinter as tk
from ScrolledText import *
from googletrans import Translator
from tkFileDialog import askopenfile,asksaveasfile
from tkSimpleDialog import askstring
from tkMessageBox import askokcancel,showinfo
from tkFont import Font
from enchant import Dict 
from nltk import word_tokenize
from re import finditer,sub

class TkApp(tk.Tk):
    def __init__(self, className=" TextMate"):
        tk.Tk.__init__(self, className=className)
        self.textPad = ScrolledText(self, width=50, height=30, font=("Monospace Regular", 13), highlightthickness=0, bd=4, undo="True")
        self.iconbitmap(r'te.ico')
        self.textPad.pack()

        menu = tk.Menu(self)
        self.textPad.tag_config("bt", background="yellow")
        self.textPad.tag_config("kw", foreground="medium sea green")
        self.textPad.tag_config("com", foreground="red")
        self.textPad.tag_config("str", foreground="purple")
        self.config(menu=menu)
                      
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="New File", command=self.new_command, accelerator="Ctrl+N")
        self.bind_all("<Control-n>",self.new_command)
        filemenu.add_command(label="Open", command=self.open_command, accelerator="Ctrl+O")
        self.bind_all("<Control-o>",self.open_command)
        filemenu.add_separator()
        filemenu.add_command(label="Save", command=self.save_command, accelerator="Ctrl+S")
        self.bind_all("<Control-s>",self.save_command)
        filemenu.add_command(label="Save As", command=self.saveas_command, accelerator="Ctrl+Shift+S")
        self.bind_all("<Control-Shift-S>",self.saveas_command)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit_command, accelerator="Ctrl+Q")
        self.bind_all("<Control-q>",self.exit_command)

        editmenu=tk.Menu(menu)
        menu.add_cascade(label="Edit", menu=editmenu)
        editmenu.add_command(label="Undo", command=self.undo_command, accelerator="Ctrl+Z")
        editmenu.add_command(label="Redo", command=self.redo_command, accelerator="Ctrl+Shift+Z")
        self.bind_all("<Control-Shift-Z>",self.redo_command)
        editmenu.add_separator()
        editmenu.add_command(label="Cut", command=self.cut_command, accelerator="Ctrl+X")
        editmenu.add_command(label="Copy", command=self.copy_command, accelerator="Ctrl+C")
        editmenu.add_command(label="Paste", command=self.paste_command, accelerator="Ctrl+V")
        editmenu.add_separator()
        editmenu.add_command(label="Select All", command=self.selectall_command, accelerator="Ctrl+A")
        self.bind_all("<Control-a>",self.selectall_command)
        editmenu.add_command(label="Delete All", command=self.deleteall_command, accelerator="Ctrl+D")
        self.bind_all("<Control-d>",self.deleteall_command)

        formatmenu = tk.Menu(menu)
        menu.add_cascade(label="Format", menu=formatmenu)
        formatmenu.add_command(label="Font", command=self.font_command, accelerator="Ctrl+M")
        self.bind_all("<Control-m>",self.font_command)
        formatmenu.add_separator()
        formatmenu.add_command(label="Bold", command=self.bold_command, accelerator="Ctrl+B")
        self.bind_all("<Control-b>",self.bold_command)
        formatmenu.add_command(label="Italics", command=self.italic_command, accelerator="Ctrl+I")
        self.bind_all("<Control-i>",self.italic_command)
        formatmenu.add_command(label="Underline", command=self.underline_command, accelerator="Ctrl+U")
        self.bind_all("<Control-u>",self.underline_command)
        formatmenu.add_command(label="Bold-Italic", command=self.bolditalic_command)
        
        preferences = tk.Menu(menu)
        menu.add_cascade(label="Preferences", menu=preferences)
        preferences.add_radiobutton(label="Text Mode", command =self.text_command)
        preferences.add_radiobutton(label="Code Mode", command =self.code_command)
        
        toolsmenu = tk.Menu(menu)
        menu.add_cascade(label="Tools", menu=toolsmenu)
        toolsmenu.add_command(label="Find", command=self.find_command, accelerator="Ctrl+F")
        self.bind_all("<Control-f>",self.find_command)
        toolsmenu.add_command(label="Replace", command=self.replace_command, accelerator="Ctrl+H")
        self.bind_all("<Control-h>",self.replace_command)
        toolsmenu.add_separator()      
        toolsmenu.add_command(label="Spell Check", command=self.spellcheck_command)
        toolsmenu.add_command(label="Translate", command=self.translate_command)
        toolsmenu.add_command(label="Brace Matching", command=self.braces_command)
        toolsmenu.add_command(label="Document Comparision", command=self.comparedoc_command)
        
        helpmenu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="About", command=self.about_command)
        
    def new_command(self,*args):
        new=TkApp()

    def open_command(self,*args):
        data = self.textPad.get('1.0', 'end-1c')
        flag=0
        for i in data:
            if(i!='\n'):
                flag=1
                break
        if(not(flag)):
            file = askopenfile(mode='rb',title='Select a file')
            if file != None:
                self.deleteall_command(self,*args)
                contents = file.read()
                self.textPad.insert('1.0',contents)
                file.close()
        else:
            if(askokcancel("Save", "You have unsaved changes. Save?")):
                self.save_command(self,*args)
            file = askopenfile(mode='rb',title='Select a file')
            if file != None:
                self.deleteall_command(self,*args)
                contents = file.read()
                self.textPad.insert('1.0',contents)
                file.close()
        global filename
        if(file!=None):
            a=[x for x in str(file).split("'")]
            filename=a[1]

    def save_command(self,*args):
        contents = self.textPad.get('1.0','end-1c')
        global filename
        try:
            with open(filename, 'w') as outputFile:  
                outputFile.write(contents)         
        except IOError:                     
            self.saveas_command()    

    def saveas_command(self,*args):
        file = asksaveasfile(mode = 'w', title='Save As')
        if file != None:
            data = self.textPad.get('1.0', 'end-1c')
            file.write(data)
            file.close()
            global filename
            a=[x for x in str(file).split("'")]
            filename=a[1]
            
    def exit_command(self,*args):
        data = self.textPad.get('1.0', 'end-1c')
        flag=0
        for i in data:
            if(i!='\n'):
                flag=1
                break
        if(flag):
            if(askokcancel("Save", "Save before closing?")):
                self.save_command(self,*args)
            self.destroy()
        else:
            if(askokcancel("Quit", "Are you sure you want to quit?")):
                self.destroy()

    def code_command(self,*args):
        self.bind("<Key>",self.auto_indent,add="+")
        self.bind("<Return>",self.keep_indent)
        self.bind("<Key>",self.keywords_command,add="+")
        self.bind("<Key>",self.comment_command,add="+")
        self.bind("<Key>",self.string_command,add="+")

    def text_command(self,*args):
        self.unbind("<Key>")
        self.unbind("<Return>")

    def copy_command(self,*args):
        try:
            self.clipboard_clear()
            text = self.textPad.get("sel.first", "sel.last")
            self.clipboard_append(text)
        except:
            pass

    def paste_command(self,*args):
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.textPad.insert('insert', text)
        except:
            pass

    def cut_command(self,*args):
        try:
            self.copy_command()
            self.textPad.delete("sel.first", "sel.last")
        except:
            pass

    def selectall_command(self,*args):
        self.textPad.tag_add('sel','1.0', 'end')
        
    def deleteall_command(self,*args):
        self.textPad.delete('1.0', 'end')

    def undo_command(self,*args):
        try:
            self.textPad.edit_undo()
        except:
            pass

    def redo_command(self,*args):
        try:
            self.textPad.edit_redo()
        except:
            pass

    def find_command(self,*args):
        search=askstring("Find", "")
        if(search==None):
            return
        l=len(search)
        data = self.textPad.get('1.0', 'end-1c')
        ind=[m.start() for m in finditer(search,data)]
        for i in ind:
            corpus=data[:i]
            last=0
            line_no=1
            k=0
            for j in corpus:
                k+=1
                if(j=='\n'):
                    line_no+=1
                    last=k
            st=str(line_no)+'.'+str(i-last)
            end=str(line_no)+'.'+str(i-last+l)
            self.textPad.tag_add('bt',st,end)

    def replace_command(self,*args):
        search=askstring("Find", "")
        rep=askstring("Replace with", "")
        if(search==None or rep==None):
            return
        l=len(search)
        data = self.textPad.get('1.0', 'end-1c')
        ind=[m.start() for m in finditer(search,data)]
        for count in range(len(ind)):
            data = self.textPad.get('1.0', 'end-1c')
            if(search in data):
                i=data.index(search)
            corpus=data[:i]
            last=0
            line_no=1
            k=0
            for j in corpus:
                k+=1
                if(j=='\n'):
                    line_no+=1
                    last=k
            st=str(line_no)+'.'+str(i-last)
            end=str(line_no)+'.'+str(i-last+l)
            self.textPad.delete(st,end)
            self.textPad.insert(st,rep)
                
    def about_command(self,*args):
        label = showinfo("TextMate", "A small and lightweight text editor.\n© 2017. All rights reserved.")

    def braces_command(self,*args):
        data = self.textPad.get('1.0', 'end-1c')
        a=[]
        for i in data:
            if(i=='(' or i=='{' or i=='['):
                a.append(i)
            if(i==')'):
                if(a==[] or a[-1]!='('):
                    label = showinfo("Brace Matching","Parenthesis don't match")
                    return
                else:
                    a.pop()
            if(i=='}'):
                if(a==[] or a[-1]!='{'):
                    label = showinfo("Brace Matching","Curly braces don't match")
                    return
                else:
                    a.pop()
            if(i==']'):
                if(a==[] or a[-1]!='['):
                    label = showinfo("Brace Matching","Square braces don't match")
                    return
                else:
                    a.pop()
        if(a==[]):
            label = showinfo("Brace Matching","All braces match!")
        else:
            ch=a[-1]
            if(ch=='('):
                label = showinfo("Brace Matching","Parenthesis don't match")
                return
            elif(ch=='{'):
                label = showinfo("Brace Matching","Curly braces don't match")
                return
            else:
                label = showinfo("Brace Matching","Square braces don't match")
                return

    def spellcheck_command(self,*args):
        dic=Dict("en_US")
        data=word_tokenize(self.textPad.get('1.0', 'end-1c'))
        for word in data:
                if not dic.check(word) and word.isalpha():
                        suggestions_list=dic.suggest(word)
                        suggestions_str=""
                        for w in suggestions_list:
                                suggestions_str+=w+" "
                        showinfo("Suggestions for '"+word+"'\n",suggestions_str)
        showinfo("Spell Check","Finished checking!")
        
    def translate_command(self,*args):
        try:
                translator = Translator()
                text = self.textPad.get("sel.first", "sel.last")
                language = askstring("Translate", "Kannada | Hindi | Tamil | Telugu | English")
                if language.lower() == "kannada":
                        language = "kn"
                elif language.lower() == "hindi":
                        language = "hi"
                elif language.lower() == "telugu":
                        language = "te"
                elif language.lower() == "tamil":
                        language = "ta"
                elif language.lower() == "english":
                        language = "en"
                s = translator.translate(text, dest = language)
                self.textPad.delete("sel.first", "sel.last")
                self.textPad.insert('insert', s.text)
        except:
                pass

    def keywords_command(self,event):
        C_keywords=["auto","double","int","struct","break","else","long",
                    "switch","case","enum","register","typedef","char","extern",
                    "return","union","const","float","short","unsigned","do",
                    "continue","for","signed","void","default","goto","sizeof",
                    "volatile","if","static","while","printf","scanf","include"]
        for key in C_keywords:
            l=len(key)
            data = self.textPad.get('1.0', 'end-1c')
            ind=[m.start() for m in finditer(key,data)]
            for i in ind:
                corpus=data[:i]
                last=0
                line_no=1
                k=0
                for j in corpus:
                    k+=1
                    if(j=='\n'):
                        line_no+=1
                        last=k
                st=str(line_no)+'.'+str(i-last)
                end=str(line_no)+'.'+str(i-last+l)
                self.textPad.tag_add('kw',st,end)

    def comparedoc_command(self,*args):
        cmpfile = askopenfile(mode='rb',title='Select a file to compare with')
        if cmpfile != None:
            contents = cmpfile.read()
            cmpfile.close()
            data = self.textPad.get('1.0', 'end-1c')
            line=[x for x in contents.split("\n")]
            line1=[x for x in data.split("\n")]
            num=min(len(line),len(line1))
            x=1
            for i in range(num):
                s=str(line[i])
                s1=str(line1[i])
                s=sub(r'\s','',s)
                s1=sub(r'\s','',s1)
                if(s==s1):
                    xy=str(x)+'.0'
                    xy1=str(x)+'.54'
                    self.textPad.tag_add('sel',xy,xy1)
                x+=1

    def keep_indent(self,event):
        try:
            if self.brace_count != 0:
                text = self.brace_count*"	"
                self.textPad.insert('insert', text)
        except:
            pass

    brace_count = 0    
    def auto_indent(self,event):
        try:
            if event.char == '{':
                self.brace_count += 1
                text = "\n"+(self.brace_count*"	")		
                self.textPad.insert('insert', text)
            if event.char == '}':
                self.brace_count -= 1
                text = "\n"+(self.brace_count*"	")
                self.textPad.insert('insert', text)
        except:
                pass

    def comment_command(self,event):
        data = self.textPad.get('1.0', 'end-1c')
        search="\/\*"
        ind=[m.start() for m in finditer(search,data)]
        for i in ind:
            corpus=data[:i]
            last=0
            line_no=1
            k=0
            for j in corpus:
                k+=1
                if(j=='\n'):
                    line_no+=1
                    last=k
            st=str(line_no)+'.'+str(i-last)
            find=data[i+2:]
            flag=0
            if("*/" in find):
                la=(find.index("*/"))+1
                last1=0
                k=0
                for j in range(la):
                    k+=1
                    if(find[j]=='\n'):
                        flag=1
                        line_no+=1
                        last1=k
                if(flag==0):
                    end=str(line_no)+'.'+str(la+i-last+3)
                else:
                    end=str(line_no)+'.'+str(la-last1+1)
            else:
                end='end-1c'
            self.textPad.tag_add('com',st,end)

        data = self.textPad.get('1.0', 'end-1c')    
        ind1=[m.start() for m in finditer("//",data)]
        for i in ind1:
            corpus=data[:i]
            last=0
            line_no=1
            k=0
            for j in corpus:
                k+=1
                if(j=='\n'):
                    line_no+=1
                    last=k
            st=str(line_no)+'.'+str(i-last)
            end=str(line_no)+'.100'
            self.textPad.tag_add('com',st,end)

    def string_command(self,event):
        data = self.textPad.get('1.0', 'end-1c')
        search="\""
        ind=[m.start() for m in finditer(search,data)]
        bool=0
        for i in ind:
            bool+=1
            if(bool%2==0):
                continue
            corpus=data[:i]
            last=0
            line_no=1
            k=0
            for j in corpus:
                k+=1
                if(j=='\n'):
                    line_no+=1
                    last=k
            st=str(line_no)+'.'+str(i-last)
            find=data[i+1:]
            flag=0
            if("\"" in find):
                la=(find.index("\""))
                last1=0
                k=0
                for j in range(la):
                    k+=1
                    if(find[j]=='\n'):
                        flag=1
                        line_no+=1
                        last1=k
                if(flag==0):
                    end=str(line_no)+'.'+str(la+i-last+2)
                else:
                    end=str(line_no)+'.'+str(la-last1+1)
            else:
                end='end-1c'
            self.textPad.tag_add('str',st,end)
            
    def bold_command(self,*args):
        current_tags = self.textPad.tag_names()
        bold = Font(self.textPad, self.textPad.cget("font"))
        bold.config(weight="bold")
        self.textPad.tag_config("bld", font=bold)
        if "bld" in current_tags:
                self.textPad.tag_delete("bld", '1.0', 'end-1c')
        else:
                self.textPad.tag_add("bld", '1.0', 'end-1c') 	
                
    def italic_command(self,*args):
        current_tags = self.textPad.tag_names()
        italics = Font(self.textPad, self.textPad.cget("font"))
        italics.config(slant="italic")
        self.textPad.tag_config("ita", font=italics)
        if "ita" in current_tags:
                self.textPad.tag_delete("ita", '1.0', 'end-1c')
        else:
                self.textPad.tag_add("ita", '1.0', 'end-1c')

    def underline_command(self,*args):
        current_tags = self.textPad.tag_names()
        underline = Font(self.textPad, self.textPad.cget("font"))
        underline.config(underline=True)
        self.textPad.tag_config("und", font=underline)
        if "und" in current_tags:
                self.textPad.tag_delete("und", '1.0', 'end-1c')
        else:
                self.textPad.tag_add("und", '1.0', 'end-1c')
                
    def bolditalic_command(self,*args):
        current_tags = self.textPad.tag_names()
        bold_italic = Font(self.textPad, self.textPad.cget("font"))
        bold_italic.config(weight="bold",slant="italic")
        self.textPad.tag_config("bldita", font=bold_italic)
        if "bldita" in current_tags:
                self.textPad.tag_delete("bldita", '1.0', 'end-1c')
        else:
                self.textPad.tag_add("bldita", '1.0', 'end-1c')
           
    def font_command(self,*args):
        try:
                font_specs = askstring("Font", "Font Style-Font Size")
                font_specs = font_specs.split('-')
                new_font = Font(self.textPad, self.textPad.cget("font"))
                new_font.config(family=font_specs[0], size=font_specs[1])
                self.textPad.tag_config("newfont", font=new_font)
                self.textPad.tag_add("newfont", '1.0', 'end-1c')
        except:
                pass
            
if __name__ == '__main__':
    filename=''
    app = TkApp()
    app.mainloop()
