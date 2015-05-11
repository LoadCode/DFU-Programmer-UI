# -*- coding: utf-8 -*-
##---------DFU Programmer UI-------------
##
##Cross Platform Graphic User Interface for DFU Programmer(R)
##Developed and Mantained By Julio César Echeverri M.  email: <julio.marulanda@outlook.com>
##website blogdelingeniero1.wordpress.com
##Release date version 1.27 ---May 1 of 2015
##



import subprocess
from Tkinter import *
import ttk
import tkMessageBox
import tkFileDialog


filePath = '' #Path of hexa file to be load in the MCU
targetMCU= ''
targets  = '''at89c51snd1c       at89c51snd2c       at89c5130          at89c5131        at89c5132
            at90usb1287        at90usb1286        at90usb1287-4k     at90usb1286-4k
            at90usb647         at90usb646         at90usb162         at90usb82
            atmega32u6         atmega32u4         atmega32u2         atmega16u4
            atmega16u2         atmega8u2
            at32uc3a0128       at32uc3a1128       at32uc3a0256       at32uc3a1256
            at32uc3a0512       at32uc3a1512       at32uc3a0512es     at32uc3a1512es
            at32uc3a364        at32uc3a364s       at32uc3a3128       at32uc3a3128s
            at32uc3a3256       at32uc3a3256s      at32uc3a4256s      at32uc3b064
            at32uc3b164        at32uc3b0128       at32uc3b1128       at32uc3b0256
            at32uc3b1256       at32uc3b0256es     at32uc3b1256es     at32uc3b0512
            at32uc3b1512       at32uc3c064        at32uc3c0128       at32uc3c0256
            at32uc3c0512       at32uc3c164        at32uc3c1128       at32uc3c1256
            at32uc3c1512       at32uc3c264        at32uc3c2128       at32uc3c2256
            at32uc3c2512
            atxmega64a1u       atxmega128a1u      atxmega64a3u       atxmega128a3u
            atxmega192a3u      atxmega256a3u      atxmega16a4u       atxmega64a4u       atxmega128a4u      atxmega256a3bu     atxmega64b1
            atxmega128b1       atxmega64b3        atxmega128b3       atxmega64c3
            atxmega128c3       atxmega256c3       atxmega384c3       atxmega16c4
            atxmega32c4        atxmega32A4U       stm32f4_B          stm32f4_C          stm32f4_E
            stm32f4_G
            '''


def Validation(output):
    #Returns 0 if an error has ocurred and 1 if everything goes right
    if output.find('no device present') != -1:
        tkMessageBox.showinfo(title = 'Connect Device',message = 'Please connect a device')
        return 0
    if output.find('github.com') != -1:
        tkMessageBox.showerror(title = 'Select Target',message = 'Please Select a Specific Device\nTo Be Programmed')
        return 0
    if output.find('Error opening') != -1: #File not selected correctly
        tkMessageBox.showinfo(title = 'Select File',message = 'File incorrectly selected \nPlease select a valid file.')        
        return 0
    if output.find('Error reading') != -1: #inconsistent file (not readable)
        tkMessageBox.showinfo(title = 'Invalid File',message = 'Inconsistent File (not readable) \nPlease Load a Valid File.')
        return 0
    if output.find('no se reconoce como un comando') != -1:
        tkMessageBox.showerror(title = 'DFU-Programmer not recognised',message='Please install dfu-programmer \nor locate the file in the appropriate folder')
        return 0
    if filePath == '':
        tkMessageBox.showerror(title = 'Select File',message='Please select a file to be loaded')
        return 0

    return 1

def LoadFileBtn():
    global filePath, SelFileSV
    filePath = tkFileDialog.askopenfilename(title = 'PythonLoad .HEX File',defaultextension = '.hex',filetypes = [('Hexa File','.hex')])
    out = filePath.split('/')
    print out
    if out == ['']:
        SelFileSV.set('No File')
    else:
        SelFileSV.set(out[len(out)-1])
    

def StartBtn():
    cmd = 'c:\dfu-programmer ' + targetMCU +' start'
    p = subprocess.Popen(cmd,shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE,stderr = subprocess.STDOUT)
    output = p.stdout.read()
    if output.find('no device present') != -1:
        tkMessageBox.showinfo(title = 'Connect Device',message = 'Please connect a device')
    
    
def ProgramBtn():
    global ProgressBR, ProgressBP, ProgSV, ReadSV, ValidationSV, WrittenSV

    ProgressBP.set(0)
    ProgSV.set('Not Programmed')
    ReadSV.set('No bytes Readed')
    ValidationSV.set('')
    WrittenSV.set('')
    
    ProgressBP.set(20)
    cmd = 'c:\dfu-programmer '+targetMCU + ' erase'
    p = subprocess.Popen(cmd,shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE,stderr = subprocess.STDOUT)
    output = p.stdout.read()
    ProgressBP.set(30)
    ProgressBR.set(20)
    valid = Validation(output)
    if valid == 1:
        cmd = 'c:\dfu-programmer '+targetMCU + ' flash '+'\"'+filePath+'\"'
        p = subprocess.Popen(cmd,shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE,stderr = subprocess.STDOUT)
        ProgressBP.set(60)
        output = p.stdout.read()
        valid = Validation(output)
        if valid != 0:
            ProgressBP.set(100)
            ProgSV.set(output[output.find('Program'):output.find('[')-1])
            ReadSV.set(output[output.find('Read',100):output.find('[',170)-1])
            ValidationSV.set(output[output.find('Valid',180):output.find('0x',230)-1])
            WrittenSV.set(output[output.find('Valid',180)+24:output.find(')',250)+2])
            for x in range(20,101):
                ProgressBR.set(x)
        else:
            ProgressBP.set(0)
            ProgressBR.set(0)
    else:
            ProgressBP.set(0)
            ProgressBR.set(0)

    
def DevSelected():
    global listbox, targetMCU, top, root, SelDevSV
    item = listbox.curselection()
    targetMCU = listbox.get(item[0])
    root.lift() #Returns the control to root window
    SelDevSV.set(targetMCU[0:2].upper()+targetMCU[2:len(targetMCU)])
    top.destroy()



def MCUSel():
    global root, listbox, top
    top = Toplevel(root) 
    top.lift(aboveThis=root)  #sets this window appear on top of the root window
    top.grab_set()
    top.title('Device Selection')
    top.geometry("200x230+%d+%d" % (root.winfo_rootx()+40,root.winfo_rooty()+20))
    listTargets = StringVar()
    listTargets.set(targets)

    frame = Frame(top)
    frame.place(x='10m',y='5m')
    yScroll = ttk.Scrollbar(frame,orient = VERTICAL)
    yScroll.grid(column=2,row=1,sticky = N+S)
    listbox = Listbox(frame,listvariable = listTargets,width = 15,activestyle = 'none',yscrollcommand=yScroll.set)
    listbox.grid(row=1,sticky = N+W)
    yScroll['command'] = listbox.yview
    BtnSel = ttk.Button(top, text = 'Select Device',command = DevSelected,takefocus=False)
    BtnSel.place(x='10m',y='50m')
    
def initGUI():

    global root, top, SelDevSV, SelFileSV, ProgressBR, ProgressBP, ProgSV, ReadSV, ValidationSV, WrittenSV
    root = Tk()
    root.geometry('500x300+50+20')
    root.title('Atmel DFU-Programmer UI ')

    #initial sets
    SelDevSV = StringVar()
    SelDevSV.set('No Device')
    SelFileSV = StringVar()
    SelFileSV.set('No File')
    ProgressBP = IntVar()
    ProgressBR = IntVar()
    ProgressBR.set(0)
    ProgressBP.set(0)
    ProgSV = StringVar()
    ProgSV.set('Not Programmed')
    ReadSV = StringVar()
    ReadSV.set('No bytes Readed')
    ValidationSV = StringVar()
    WrittenSV = StringVar()
    ValidationSV.set('')
    WrittenSV.set('')
    
    
    #Buttons Section
    FrameBtns = ttk.Frame(root)
    FrameBtns.place(x = '12m', y = '7m')
    BtnDevSel = ttk.Button(FrameBtns, text = 'Device Selection',command = MCUSel,takefocus=False)
    BtnDevSel.pack(side = LEFT,padx = 4)
    BtnLoadFile = ttk.Button(FrameBtns, text = ' Load File ',command = LoadFileBtn,takefocus=False)
    BtnLoadFile.pack(side = LEFT,padx = 4)
    BtnProgram = ttk.Button(FrameBtns, text = 'Program Device',command = ProgramBtn,takefocus=False)
    BtnProgram.pack(side = LEFT,padx = 4)
    BtnStart = ttk.Button(FrameBtns, text = 'Restart Device',command = StartBtn,takefocus=False)
    BtnStart.pack(side = LEFT,padx = 4)
    ttk.Style().configure("TButton", padding=6,relief="flat")

    #File and Device Selected
    FrameSelection = ttk.Frame(root)
    FrameSelection.place(x = '12m', y = '25m')
    TagSelDev = ttk.Label(FrameSelection,text = 'Selected Device')
    TagSelDev.pack(side = LEFT, padx=4)
    LblSelDev = ttk.Label(FrameSelection,textvariable = SelDevSV,background = '#fff')
    LblSelDev.pack(side = LEFT, padx=4)
    TagSelFile = ttk.Label(FrameSelection,text = '       Selected File')
    TagSelFile.pack(side = LEFT, padx=4)
    LblSelFile = ttk.Label(FrameSelection,textvariable = SelFileSV,background = '#fff')
    LblSelFile.pack(side = LEFT, padx=4)

    # Progress Bar
    FrameProgBarUp = ttk.Frame(root)
    FrameProgBarUp.place(x = '12m', y = '37m')
    ProgressBarProgramming = ttk.Progressbar(FrameProgBarUp,orient=HORIZONTAL, length=200,variable = ProgressBP, mode='determinate', )
    ProgressBarProgramming.pack(side = LEFT,pady = 10)
    LblProgBytes = ttk.Label(FrameProgBarUp,textvariable = ProgSV)
    LblProgBytes.pack(side = LEFT, padx = 15)
    FrameProgBarLow = ttk.Frame(root)
    FrameProgBarLow.place(x = '12m', y = '49m')
    ProgressBarReading = ttk.Progressbar(FrameProgBarLow,orient=HORIZONTAL, length=200, variable = ProgressBR, mode='determinate')
    ProgressBarReading.pack(side = LEFT, pady = 10)
    LblReadingBytes = ttk.Label(FrameProgBarLow,textvariable = ReadSV)
    LblReadingBytes.pack(side = LEFT,padx = 15)

    #Validation
    FrameLow = ttk.Frame(root)
    FrameLow.place(x = '12m', y = '60m')
    LblValidation = ttk.Label(FrameLow,textvariable = ValidationSV)
    LblValidation.pack(pady = 5)
    LblWrittenBytes = ttk.Label(FrameLow, textvariable = WrittenSV)
    LblWrittenBytes.pack()

    root.mainloop()


initGUI()

