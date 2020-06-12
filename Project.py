from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import os
import time
import shutil


####################################
########_USEFUL_FUNCTIONS_##########
####################################
def ShowError(error):
    errorbox = Tk()
    errorbox.withdraw()
    messagebox.showinfo("Error", error)


#####################################
def buttonselected(button, buttons):
    global selectedbutton
    selectedbutton = button
    for i in buttons:
        if (i == button):
            i.configure(bg="lightblue")
        else:
            i.configure(bg='SystemButtonFace')


#####################################
def space(word, numofspaces):
    space = ""
    for i in range(0, numofspaces - len(word)):
        space = space + " "
    return space


#####################################
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


########################################
def MakeUI():
    DestroyAll()
    #DrawGantt(['0.0-1000.0:p1', '3000.0-4000.0:p2'])

    global label1,entry1,label2,label3,entry3,label4,entry4,label5,label6,entry6,label7,entry7,label8,entry8,label9,entry9
    global entryTs
    global entrydistfreq,entryhr,entryhs
    
    origx=0
    origy=-70
    
    label1 = Label(GUI, text="Select Plant Type", bg="LightBlue", fg="white", font=("Times", 16), width=18, relief="ridge")
    label1.place(x=origx+20, y=origy+120)
    
    global planttype
    planttype = IntVar()
    
    buttonCont = Radiobutton(GUI, text="Continous", variable=planttype, value=1, bg="#d2d2d2", font=("Arial", 14),command=lambda:ShowContUI())
    buttonCont.place(x=origx+0, y=origy+160)
    buttonDisc = Radiobutton(GUI, text="Discrete", variable=planttype, value=2, bg="#d2d2d2", font=("Arial", 14),command=lambda:ShowDiscUI())
    buttonDisc.place(x=origx+150, y=origy+160)    


################################################
    global designtype
    designtype = IntVar()
    
    label6 = Label(GUI, text="Choose Design Criteria", bg="LightBlue", fg="white", font=("Times", 16), width=18, relief="ridge")
    label6.place(x=origx+400, y=origy+120 )  
    
    buttonContDes = Radiobutton(GUI, text="Continous-Design", variable=designtype, value=1, bg="#d2d2d2", font=("Arial", 14),command=lambda:contdesignUI())
    buttonContDes.place(x=origx+350, y=origy+160)
    buttonDiscDes = Radiobutton(GUI, text="Discrete-Design", variable=designtype, value=2, bg="#d2d2d2", font=("Arial", 14),command=lambda:discdesignUI())
    buttonDiscDes.place(x=origx+550, y=origy+160)
       

###########################################################
    
    label14 = Label(GUI, text="Disturbance", bg="LightBlue", fg="white", font=("Times", 16), width=15, relief="ridge")
    label14.place(x=origx+900, y=origy+120 )    

    label15 = Label(GUI, text="Freq(Hz):", bg="LightBlue", fg="white", font=("Times", 16), width=8,  relief="ridge")
    label15.place(x=origx+850, y=origy+160)
    entrydistfreq = Entry(GUI, font=("Times", 14), width=8)
    entrydistfreq.place(x=origx+1000, y=origy+160)
    entrydistfreq.insert(END,0)

        
    label16 = Label(GUI, text="Hr(Z):", bg="LightBlue", fg="white", font=("Times", 16), width=8, relief="ridge")
    label16.place(x=origx+850, y=origy+190)
    entryhr = Entry(GUI, font=("Times", 14), width=14)
    entryhr.place(x=origx+1000, y=origy+190)
    entryhr.insert(END,1)
    
    label17 = Label(GUI, text="Hs(Z):", bg="LightBlue", fg="white", font=("Times", 16), width=8, relief="ridge")
    label17.place(x=origx+850, y=origy+220)
    entryhs = Entry(GUI, font=("Times", 14), width=14)
    entryhs.place(x=origx+1000, y=origy+220)
    entryhs.insert(END,1)

    
###########################################################
    global removestablezeros
    removestablezeros = IntVar()
    Checkbutton(GUI, text="Remove Stable Zeros", variable=removestablezeros).place(x=origx+500, y=origy+500)

    
    ButtonSolve= Button(GUI, text="SOLVE", font=("Arial", 14), bg="lightgreen", command=lambda: solve())
    ButtonSolve.configure(height=1, width=15)
    ButtonSolve.place(x=origx+500, y=origy+580)
    
    label18 = Label(GUI, text="Ts:", bg="LightBlue", fg="white", font=("Times", 16), width=10, relief="ridge")
    label18.place(x=origx+0, y=origy+400)
    entryTs = Entry(GUI, font=("Times", 16), width=12)
    entryTs.place(x=origx+150, y=origy+400)



    ButtonGenCode= Button(GUI, text="Generate C Code", font=("Arial", 14), bg="lightgreen", command=lambda: generatecode())
    ButtonGenCode.configure(height=1, width=20)
    ButtonGenCode.place(x=origx+100, y=origy+580)


    ButtonSimulinkModel= Button(GUI, text="Make Simulink Model", font=("Arial", 14), bg="lightgreen", command=lambda: runsimulinkscript())
    ButtonSimulinkModel.configure(height=1, width=20)
    ButtonSimulinkModel.place(x=origx+100, y=origy+700)    

#####################################

def solve():#[Ts Bp Ap Hr Hs dist P Bm Am]
    
     parameters=list()
     parameters.append("function formatdata")
     parameters.append("Ts="+entryTs.get()+";")
     try:
       parameters.append("Bp="+entryBp.get()+";")
       parameters.append("Ap="+entryAp.get()+";")
     except:
         pass
     try: 
      parameters.append("num="+entrynum.get()+";")
      parameters.append("den="+entryden.get()+";")
      parameters.append("delay="+entrydelay.get()+";")
     except:
         pass
     try:
        parameters.append("w0reg="+entryregw.get()+";")
        parameters.append("zetareg="+entryregzeta.get()+";")     
        parameters.append("w0track="+entrytrackw.get()+";")
        parameters.append("zetatrack="+entrytrackzeta.get()+";")
     except:
         pass
     try:
        parameters.append("P="+entrypz.get()+";")
        parameters.append("Bm="+entrybm.get()+";")
        parameters.append("Am="+entryam.get()+";")
     except:
         pass
     parameters.append("Hr="+entryhr.get()+";")
     parameters.append("Hs="+entryhs.get()+";")
     parameters.append("distfreq="+entrydistfreq.get()+";")

     if (designtype.get()==1):
         parameters.append("contdesign=1;")
     if (designtype.get()==2):   
         parameters.append("contdesign=0;")

     if (planttype.get()==1):
         parameters.append("contplant=1;")
     if (planttype.get()==2):   
         parameters.append("contplant=0;")
         
     if (removestablezeros.get()==1):
         parameters.append("removestablezeroes=1;")
     if (removestablezeros.get()==0):   
         parameters.append("removestablezeroes=0;")       

     print (parameters)

     MakeMatlabScript(parameters)
     
     MakeSimulinkScript(parameters)


def MakeMatlabScript(parameters):
    lines=parameters.copy()
    
    makefirstheader(parameters[1:])

    with open('matlabscript.m', 'w') as newscript:
       with open('solveAsly.m', 'r') as oldscript:
           oldfilecontents=oldscript.read()
           for line in lines:
               newscript.write(line)
               newscript.write("\n")
           for oldlines in oldfilecontents:
               newscript.write(oldlines)
    try:
        os.remove("output.txt")
    except:
        pass
    os.system(' matlab -nosplash -nodesktop -r "diary output.txt; matlabscript; exit" ')

    while ( "output.txt" not in os.listdir()):
        continue
    
    time.sleep(2)
    showRST()


def MakeSimulinkScript(parameters):
    
    lines=parameters.copy()

    with open('output.txt', 'r') as rst:
        RSTLINES = rst.read().split("\n")
        R=RSTLINES[3].split()
        S=RSTLINES[8].split()
        T=RSTLINES[13].split()
        
    Rline="R=["   
    for i in range(len(R)):
        Rline+=R[i]+" "
    Rline+="];"
    lines.append(Rline)
    
    Sline="S=["   
    for i in range(len(S)):
        Sline+=S[i]+" "
    Sline+="];"
    lines.append(Sline)
    
    Tline="T=["   
    for i in range(len(T)):
        Tline+=T[i]+" "
    Tline+="];"
    lines.append(Tline)


    with open('simulinkscript.m', 'w') as newscript:
       with open('SimulinkAsly.m', 'r') as oldscript:
           oldfilecontents=oldscript.read()
           for line in lines:
               newscript.write(line)
               newscript.write("\n")
           for oldlines in oldfilecontents:
               newscript.write(oldlines)

               
    
def runsimulinkscript():
        os.system(' matlab -nosplash -nodesktop -r "simulinkscript;" ')



def makefirstheader(parameters):
    lines=parameters.copy()
    
    with open('INPUT.h','w')  as file:
        file.write("#ifndef __INPUT__H__ \n")
        file.write("#define __INPUT__H__ \n \n")
        

        for line in lines:
          variable=line.split("=")[0]

          if ("[" in line):
              values=line[line.find("[")+1 : -2].split()

              for i in range(len(values)):
                 file.write("#define "+variable+"_"+str(i)+" "+values[i]+"\n")
              file.write("\n")

          else:
              value=line.split("=")[1][:-1]
              file.write("#define "+variable+" "+value+"\n \n")


        file.write("\n#endif \n")      
           
           

    
def showRST(): #displays rst in UI and make header file of RST

    with open('output.txt', 'r') as rst:
        lines = rst.read().split("\n")
        R=lines[3].split()
        S=lines[8].split()
        T=lines[13].split()
        
      
    entryRST = Text(GUI, font=("Times", 16), width=30,height=10)
    entryRST.place(x=900, y=500)

    
    entryRST.insert(END, "R=[")

        
    with open('RST.h','w')  as rstheader:
        rstheader.write("#ifndef __RST__H__ \n")
        rstheader.write("#define __RST__H__ \n \n")
        
        for i in range (0,len(R)):
            rstheader.write("#define R_"+str(i)+" "+R[i]+"\n")
            
            entryRST.insert(END,R[i]+", ")

            
        rstheader.write("\n")
        entryRST.insert(END,"]\nS=[")
        
        for i in range (0,len(S)):
            rstheader.write("#define S_"+str(i)+" "+S[i]+"\n")
            entryRST.insert(END,S[i]+", ")

        rstheader.write("\n")
        entryRST.insert(END,"]\nT=[")
        
        for i in range (0,len(T)):
            rstheader.write("#define T_"+str(i)+" "+T[i]+"\n")    
            entryRST.insert(END,T[i]+", ")
            
        rstheader.write("\n#endif \n")      
        entryRST.insert(END,"]\n")
        

        entryRST.insert(END,"\n\n   input header file saved as INPUT.h")
        entryRST.insert(END,"\n   RST header file saved as RST.h")


        entryRST.tag_add("start", 6.0, END)
        entryRST.tag_config("start", foreground="red")
        

def generatecode(): # C CODE GENERATION

   with open('output.txt', 'r') as rst:
        lines = rst.read().split("\n")
        R=lines[3].split()
        S=lines[8].split()
        T=lines[13].split()
    
   
   part1="("+"("+tstring(T)+")\n"+"-"+"("+rstring(R)+")"+")\n"+sstring(S)+";"
   part2,part3,part4 = el7etaelyta7t(len(T),len(R),len(S))
   part2string=""
   part3string=""
   part4string=""


   for i in range (len(part2)):
      part2string+= part2[i]+"\n"

      
   for i in range (len(part3)):
      part3string+= part3[i]+"\n"

   for i in range (len(part4)):
      part4string+= part4[i]+"\n"      

   projects=[0]                   
   for folder in os.listdir():
      if (folder.split()[0]=="Project"):
         projects.append(int(folder.split()[1]))
         
   directory = "Project "+ str(max(projects)+1)
   
   os.mkdir(directory)

   tempfilespath= "temp/"
   with open(tempfilespath+'TempSubC','r') as c_code:
     lines=c_code.readlines()
     with open (directory+'\Subsystem.c','w') as file:
        for line in lines:
           
           if ("REPLACE1" in line):
               file.write(line.replace("REPLACE1",part1))
               continue
            
           if ("REPLACE2" in line):
               file.write(line.replace("REPLACE2",part2string))
               continue
           if ("REPLACE3" in line):
               file.write(line.replace("REPLACE3",part3string))
               continue
           if ("REPLACE4" in line):
               file.write(line.replace("REPLACE4",part4string))
               continue   
           file.write(line)

   with open(tempfilespath+'TempSubH','r') as c_code:
     lines=c_code.readlines()
     with open (directory+'\Subsystem.h','w') as file:
        for line in lines:
           
           if ("T_SIZE" in line):
               file.write(line.replace("T_SIZE",str(len(T)-1)))
               continue         
           if ("R_SIZE" in line):
               file.write(line.replace("R_SIZE",str(len(R)-1)))
               continue
           if ("S_SIZE" in line):
               file.write(line.replace("S_SIZE",str(len(S)-1)))
               continue          
           file.write(line)

   shutil.copyfile(tempfilespath+"ert_mainC", directory+"/ert_main.c")
   shutil.copyfile(tempfilespath+"rtwtypesH", directory+"/rtwtypes.h")
   shutil.copyfile(tempfilespath+"Subsystem_privateH", directory+"/Subsystem_private.h")
   shutil.copyfile(tempfilespath+"Subsystem_typesh", directory+"/Subsystem_types.h")
   shutil.copyfile(tempfilespath+"Project", directory+"/"+directory + ".uvprojx")
   
   shutil.copyfile("RST.h", directory+"/"+"RST.h")
   shutil.copyfile("INPUT.h", directory+"/"+"INPUT.h")



   

   label= Label(GUI,text="C Code Generated! Saved at /"+directory,bg="#d2d2d2",fg="Green",font=("Times", 18))
   label.place(x=50,y=550)
   GUI.after(4000,lambda:label.destroy()) 



def tstring(t):

   t_part=""
   for i in range (0,len(t)):
           t_part += " " + "T_"+str(i)

           if(i==0):
             t_part += " * Subsystem_U.In1"

           else:
              t_part += " * Subsystem_DW.Tz_states["+str(i-1)+"]"

           if(i!=len(t)-1):
               t_part += " +"

   return t_part

def rstring(r):

   r_part=""
   for i in range (0,len(r)):
           r_part += " " + "R_"+str(i)

           if(i==0):
             r_part += " * Subsystem_U.In2"

           else:
              r_part += " * Subsystem_DW.Rz_states["+str(i-1)+"]"

           if(i!=len(r)-1):
               r_part += " +"

   return r_part


def sstring(s):

   s_part=""
   for i in range (1,len(s)):

           s_part += " -"
           s_part += " " + "S_"+str(i)  
           s_part += " * Subsystem_DW.uSz_states["+str(i-1)+"]"


   return s_part

def el7etaelyta7t(t,r,s):
    tpart=list()
    rpart=list()
    spart=list()

    for i in range (t-2,-1,-1):
      if (i==0):
          tpart.append("Subsystem_DW.Tz_states["+str(i)+"] = Subsystem_U.In1;")
          break
                       
      tpart.append("Subsystem_DW.Tz_states["+str(i)+"] = Subsystem_DW.Tz_states[" +str(i-1) +"];")
                   
    for i in range (r-2,-1,-1):
      if (i==0):
          rpart.append("Subsystem_DW.Rz_states["+str(i)+"] = Subsystem_U.In2;")
          break
                       
      rpart.append("Subsystem_DW.Rz_states["+str(i)+"] = Subsystem_DW.Rz_states[" +str(i-1) +"];")
                   
    for i in range (s-2,-1,-1):
      if (i==0):
          spart.append("Subsystem_DW.uSz_states["+str(i)+"] = rtb_Sum1;")
          break
                       
      spart.append("Subsystem_DW.uSz_states["+str(i)+"] = Subsystem_DW.uSz_states[" +str(i-1) +"];")
                   

          
    return tpart,rpart,spart



def contdesignUI():
    
    origx=40
    origy=-70
    global label7,entryregw,label8,entryregzeta,label11,label12,entrytrackw,entrytrackzeta
    
    DestroyArea2()
    
    label6 = Label(GUI, text="Regulation Dynamics", bg="LightBlue", fg="white", font=("Times", 16), width=15, relief="ridge")
    label6.place(x=origx+380, y=origy+200 )    

    label7 = Label(GUI, text="ω0:", bg="LightBlue", fg="white", font=("Times", 16), width=8,  relief="ridge")
    label7.place(x=origx+350, y=origy+230)
    entryregw = Entry(GUI, font=("Times", 16), width=8)
    entryregw.place(x=origx+500, y=origy+230)

        
    label8 = Label(GUI, text="ζ:", bg="LightBlue", fg="white", font=("Times", 16), width=8, relief="ridge")
    label8.place(x=origx+350, y=origy+260)
    entryregzeta = Entry(GUI, font=("Times", 16), width=8)
    entryregzeta.place(x=origx+500, y=origy+260)


    label10 = Label(GUI, text="Tracking Dynamics", bg="LightBlue", fg="white", font=("Times", 16), width=15, relief="ridge")
    label10.place(x=origx+380, y=origy+310 )    

    label11 = Label(GUI, text="ω0:", bg="LightBlue", fg="white", font=("Times", 16), width=8,  relief="ridge")
    label11.place(x=origx+350, y=origy+340)
    entrytrackw = Entry(GUI, font=("Times", 16), width=8)
    entrytrackw.place(x=origx+500, y=origy+340)

        
    label12 = Label(GUI, text="ζ:", bg="LightBlue", fg="white", font=("Times", 16), width=8, relief="ridge")
    label12.place(x=origx+350, y=origy+370)
    entrytrackzeta = Entry(GUI, font=("Times", 16), width=8)
    entrytrackzeta.place(x=origx+500, y=origy+370)
    

     
def discdesignUI():
    
    global label9,entrypz,label12,entrybm,label13,entryam
    DestroyArea2()
    
    origx=40
    origy=-70
    label6 = Label(GUI, text="Regulation Dynamics", bg="LightBlue", fg="white", font=("Times", 16), width=15, relief="ridge")
    label6.place(x=origx+380, y=origy+200 )
    
    label9 = Label(GUI, text="P(Z):", bg="LightBlue", fg="white", font=("Times", 16), width=8, relief="ridge")
    label9.place(x=origx+350, y=origy+230)
    entrypz = Entry(GUI, font=("Times", 14), width=20)
    entrypz.place(x=origx+500, y=origy+230)
    
    label10 = Label(GUI, text="Tracking Dynamics", bg="LightBlue", fg="white", font=("Times", 16), width=15, relief="ridge")
    label10.place(x=origx+380, y=origy+310 )  
    
    label12 = Label(GUI, text="Bm(z):", bg="LightBlue", fg="white", font=("Times", 16), width=8, relief="ridge")
    label12.place(x=origx+350, y=origy+340)
    entrybm = Entry(GUI, font=("Times", 14), width=20)
    entrybm.place(x=origx+500, y=origy+340)

    label13 = Label(GUI, text="Am(Z):", bg="LightBlue", fg="white", font=("Times", 16), width=8, relief="ridge")
    label13.place(x=origx+350, y=origy+370)
    entryam= Entry(GUI, font=("Times", 14), width=20)
    entryam.place(x=origx+500, y=origy+370)

    

def ShowDiscUI():
    global label2,entryBp,label3,entryAp       
    origx=0
    origy=-70
    
    DestroyAll()
   # MakeUI()

    label2 = Label(GUI, text="Bp(Z):", bg="LightBlue", fg="white", font=("Times", 16), width=10,  relief="ridge")
    label2.place(x=origx+0, y=origy+210)
    entryBp = Entry(GUI, font=("Times",14), width=20)
    entryBp.place(x=origx+150, y=origy+210)
    
    
    label3 = Label(GUI, text="Ap(Z): ", bg="LightBlue", fg="white", font=("Times", 16), width=10, relief="ridge")
    label3.place(x=origx+0, y=origy+240)
    entryAp = Entry(GUI, font=("Times", 14), width=20)
    entryAp.place(x=origx+150, y=origy+240)
           

def ShowContUI():
           
    global label2,entrynum,label3,entryden,label5,entrydelay     
       
    origx=0
    origy=-70
    DestroyAll()
   # MakeUI()

    label2 = Label(GUI, text="Plant Num:", bg="LightBlue", fg="white", font=("Times", 16), width=10,  relief="ridge")
    label2.place(x=origx+0, y=origy+210)
    entrynum = Entry(GUI, font=("Times", 14), width=20)
    entrynum.place(x=origx+150, y=origy+210)
    
    
    label3 = Label(GUI, text="Plant Den:", bg="LightBlue", fg="white", font=("Times", 16), width=10, relief="ridge")
    label3.place(x=origx+0, y=origy+240)
    entryden = Entry(GUI, font=("Times", 14), width=20)
    entryden.place(x=origx+150, y=origy+240)
    

    
    label5 = Label(GUI, text="Delay:", bg="LightBlue", fg="white", font=("Times", 16), width=10, relief="ridge")
    label5.place(x=origx+0, y=origy+270)
    entrydelay = Entry(GUI, font=("Times",14), width=20)
    entrydelay.place(x=origx+150, y=origy+270)

                      
#####################################


######################################
######################################
def main():
    global GUI, B0, B1, B2, B3

    GUI = Tk()
    GUI.title("RST SOLVER")
    GUI.configure(bg='#d2d2d2')
    GUI.minsize(0, 800)
    GUI.resizable(0, 0)

    labelbanner = Label(GUI, text="RST SOLVER", font=("Arial", 30), bg='lightblue', relief="ridge", fg="White")
    labelbanner.grid(columnspan=4, padx=500, sticky='ew')

    MakeUI()

    GUI.mainloop()



##########################
##########################

def DestroyAll():  # make sure that area we use is clear before placing objects

    try:
      label2.destroy()
      entryBp.destroy()
      label3.destroy()
      entryAp.destroy() 
    except:
        pass
    try:
       label2.destroy()
       entrynum.destroy()
       label3.destroy()
       entryden.destroy()
       entrydelay.destroy()
       label5.destroy()
    except:
        pass
    
def DestroyArea2():    
    try:
        label7.destroy()
        entryregw.destroy()
        label8.destroy()
        entryregzeta.destroy()
        label11.destroy()
        label12.destroy()
        entrytrackw.destroy()
        entrytrackzeta.destroy()
    except:
        pass

    try:
        label9.destroy()
        entrypz.destroy()
        label12.destroy()
        entrybm.destroy()
        label13.destroy()
        entryam.destroy()
    except:
        pass

##########################
##########################

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom

main()

#try:
 #   main()
#except:
    #ShowError("Error Happened, Please Check Your Inputs!")

