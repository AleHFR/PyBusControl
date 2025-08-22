########### Preâmbulo ###########
# Imports do python
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog

# Imports do projeto
import widget_manager as wm
import custom_widgets as cw
import utils as ut

class Widget:
    def __init__(self):
        self.modbus = None
        self.style = None
    
    def style(self, style):
        self.style = style