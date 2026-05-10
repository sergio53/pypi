import math
from ipycanvas import Canvas, MultiCanvas, hold_canvas
import ipywidgets as widgets
from IPython.display import display, clear_output, Javascript, Audio
import os
import sys
import numpy as np
import json

is_Voila = 'VOILA_REQUEST_URL' in os.environ
canvas = Canvas(width=1210, height=650) if is_Voila else Canvas(width=1100, height=500)

editor = widgets.Textarea(
  layout=widgets.Layout(width='98%', height='100%')
)

terminal = widgets.Text(
  placeholder='Введите команду здесь ...',
  layout=widgets.Layout(width='98%')
)

editor_font_size = "11pt" 
custom_style = widgets.HTML(f"""
<style>
    .custom-editor textarea {{
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace !important;
        font-size: {editor_font_size} !important;
        line-height: .9 !important;
        padding: 10px !important;
        border: 1px solid #bdc3c7 !important;
        border-radius: 4px !important;
    }}
    .custom-terminal input {{ 
        /*background-color: #1e1e1e !important;*/
        /*color: #00ff00 !important;*/ /* Классический зеленый текст */
        color: #00008b !important; /* Темно-синий текст */
        font-family: 'Consolas', monospace !important;
        font-size: {editor_font_size} !important;
        border: 2px solid #444 !important;    
     }}
</style>
""")

editor.add_class('custom-editor')
terminal.add_class('custom-terminal')

run_btn = widgets.Button(
  description="ИСПОЛНИТЬ СКРИПТ",
  button_style='success',
  layout=widgets.Layout(width='98%', height='40px')
)

left_box = widgets.VBox([custom_style, editor, run_btn, terminal], layout=widgets.Layout(width='18%'))

out = widgets.Output()
if not is_Voila:
  L_out = widgets.Output(layout=widgets.Layout(width='50%', border='1px solid #ccc'))
  R_out = widgets.Output(layout=widgets.Layout(width='50%', border='1px solid #ccc'))
  dev_UI = widgets.HBox([L_out, R_out], layout=widgets.Layout(border='1px solid #ccc'))
  
right_box = widgets.VBox(
  [canvas], 
  layout=widgets.Layout(
    width=f"{canvas.width+10}px",
    height=f"{canvas.height+10}px",
    border='1px solid #ccc',
    display='flex',
    align_items='center',  # Центрируем холст внутри
    justify_content='center'
  )
)
app_UI = widgets.HBox([left_box, right_box], layout=widgets.Layout(border='1px solid #ccc'))
if is_Voila:
  app_ui = app_UI
else:
  app_ui = widgets.VBox([app_UI, dev_UI], layout=widgets.Layout(border='1px solid #ccc'))

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def canvas_init():
  canvas.fill_style = '#2c3e50'
  canvas.fill_rect(0, 0, canvas.width, canvas.height)  
canvas.on_client_ready(canvas_init)

clear_output()
display(out)
with out: 
  display(app_ui)
None  