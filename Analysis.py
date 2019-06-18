#-------------------------------------------------------------------------------
# Name:        Analysis
# Purpose:
#
# Author:      Sébastien
#
# Created:     12/06/2019
# Copyright:   (c) Sébastien 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pandas
import csv
from tkinter import *


class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)

if __name__ == '__main__':
   root = Tk()
   lng = Checkbar(root, ['2012', '2013', '2014', '2015'])
   lng.pack(side=TOP,  fill=X)
   lng.config(relief=GROOVE, bd=2)

   def allstates():
      print(list(lng.state()))

   Button(root, text='Quit', command=root.destroy).pack(side=RIGHT)
   Button(root, text='Peek', command=allstates).pack(side=RIGHT)

   root.mainloop()




























