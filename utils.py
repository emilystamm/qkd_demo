# utils.py
import time, sys
def PrintSendQubit(a, b, lefttoright=True, bit = False, num_tabs=5, icon = "", pause= .3):
   result = ""
   basis = "+"
   if icon == "":
      if (a == 1):
         if bit: icon = "0"
         else: 
            # icon = "|0>"
            icon = "| "
         # result = "0"
      elif (b == 1):
         if bit: icon = "1"
         else: 
            # icon = "|1>"
            icon = "- "
         result = "1"
      else :
         # icon = str(a) + "|0>+"+ str(b) + "|1>"
         basis = "x"
         if (str(b) =='-1/rt(2)') : 
            result = "1"
            icon = "\ "
         else: 
            result = "0"
            icon = "/ "
   result = icon
   for i in range(num_tabs):
      if lefttoright: 
         if bit: s = "\t"*i + icon
         else: s = basis + " , " + str(result) + "\t"*i + icon
      else: 
         if bit: s = "\t"*(num_tabs-i) + icon
         else: s = "\t"*(num_tabs-i) + icon + basis + " , " + str(result) 
      print(s)
      WriteOver(pause)
   if bit: s = icon
   else: 
      if lefttoright: s = basis + " , " + str(result) 
      else: s = "\t"*(num_tabs)  + basis + " , " + str(result) 
   print(s)
   
   sys.stdout.write("\033[F") #back to previous line
   

def PrintMeasureQubit(basis, result, num_tabs=0):
   # print("\t"* num_tabs + basis + " , " + str(result))
   if (basis == "x"):
      if (result == 0): print("\t"* num_tabs + basis + " , / ")
      else: print("\t"* num_tabs + basis + " , \ ")
   else:
      if (result == 0): print("\t"* num_tabs + basis + " , | ")
      else: print("\t"* num_tabs + basis + " , - ")




def WriteOver(pause):
   time.sleep(pause)
   sys.stdout.write("\033[F") #back to previous line
   sys.stdout.write("\033[K") #clear line


   