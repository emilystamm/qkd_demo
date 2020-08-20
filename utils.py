# utils.py
import time, sys
def PrintSendQubit(basis, qubit, lefttoright=True, bit = False, num_tabs=5, icon = "", pause= .310, start_tab=0):
   if basis == "+":
      if (qubit  == 0):
         icon = "| "
      else:
         icon = "- "
   else:
      if (qubit == 0):
         icon = "/ "
      else:
         icon = "\ "
   for i in range(num_tabs):
      if lefttoright: 
         if bit: s = "\t"*(i + start_tab) + icon
         else: s = basis + " , " + str(icon) + "\t"*(i + start_tab) + icon
      else: 
         if bit: s = "\t"*(num_tabs-i) + icon
         else: s = "\t"*(num_tabs-i) + icon + basis + " , " + str(icon) 
      print(s)
      WriteOver(pause)
   if bit: s = icon
   elif (start_tab ==0): 
      if lefttoright: s = "\t"*(start_tab) + basis + " , " + str(icon) 
      else: s = "\t"*(num_tabs - start_tab)  + basis + " , " + str(icon) 
   print("\t"*(start_tab) + s)
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


   