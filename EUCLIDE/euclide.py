todo_list = """
  &midpoint $1 $2 $3
  // $1-midpoint result
  // $2-irst point 
  // $3-second point
  
  = ab $2 $3
  @ Ca $2 $3
  @ Cb $3 $2
  + p1,p2 Ca Cb
  = p1p2 p1 p2
  + $1 ab p1p2
"""
import math
from ipycanvas import Canvas, MultiCanvas, hold_canvas
import ipywidgets as widgets
from IPython.display import display, clear_output, Javascript, Audio
import os
import sys
import numpy as np
import json

# Словарь групп на французском
# Формат: 'Название группы': (('Французское имя', 'EnglishName'), ...)
COLOUR_GROUPS = {
    'Серые': (
        'Black', 'DimGray', 'Gray', 'DarkGray', 'Silver', 'LightGray', 'Gainsboro', 'WhiteSmoke', 'White'
    ),
    'Синие': (
        'MidnightBlue', 'Navy', 'DarkBlue', 'MediumBlue', 'Blue', 'RoyalBlue', 'SteelBlue', 
        'DodgerBlue', 'DeepSkyBlue', 'SkyBlue', 'LightSkyBlue', 'AliceBlue'
    ),
    'Зеленые': (
        'DarkGreen', 'Green', 'ForestGreen', 'SeaGreen', 'MediumSeaGreen', 'LimeGreen', 
        'Lime', 'LawnGreen', 'Chartreuse', 'SpringGreen', 'MediumSpringGreen', 'PaleGreen'
    ),
    'Красные/Розовые': (
        'DarkRed', 'Red', 'FireBrick', 'Crimson', 'IndianRed', 'PaleVioletRed', 
        'DeepPink', 'HotPink', 'LightPink', 'Pink', 'MistyRose'
    ),
    'Желтые/Оранжевые': (
        'DarkOrange', 'Orange', 'Gold', 'Yellow', 'LightYellow', 'LemonChiffon', 'PapayaWhip'
    ),
    'Коричневые': (
        'Maroon', 'SaddleBrown', 'Sienna', 'Brown', 'Chocolate', 'Peru', 'SandyBrown', 'BurlyWood', 'Tan'
    ),
    'Фиолетовые': (
        'Indigo', 'Purple', 'DarkMagenta', 'DarkOrchid', 'MediumPurple', 'Thistle', 'Plum', 'Violet', 'Magenta'
    )
}
COLORS_FR = {
    'Gris': (
        ('Noir', 'Black'), ('Gris foncé', 'DimGray'), ('Gris', 'Gray'), 
        ('Argent', 'Silver'), ('Gris clair', 'LightGray'), ('Blanc', 'White')
    ),
    'Bleus': (
        ('Bleu nuit', 'MidnightBlue'), ('Marine', 'Navy'), ('Bleu foncé', 'DarkBlue'), 
        ('Bleu royal', 'RoyalBlue'), ('Bleu ciel', 'SkyBlue'), ('Bleu doddger', 'DodgerBlue')
    ),
    'Verts': (
        ('Vert foncé', 'DarkGreen'), ('Vert', 'Green'), ('Vert forêt', 'ForestGreen'), 
        ('Vert mer', 'SeaGreen'), ('Lime', 'Lime'), ('Vert printemps', 'SpringGreen')
    ),
    'Rouges/Roses': (
        ('Rouge foncé', 'DarkRed'), ('Rouge', 'Red'), ('Crimson', 'Crimson'), 
        ('Rose profond', 'DeepPink'), ('Rose chaud', 'HotPink'), ('Rose', 'Pink')
    ),
    'Jaunes/Oranges': (
        ('Orange foncé', 'DarkOrange'), ('Orange', 'Orange'), ('Or', 'Gold'), 
        ('Jaune', 'Yellow'), ('Citron', 'LemonChiffon')
    ),
    'Bruns': (
        ('Marron', 'Maroon'), ('Brun selle', 'SaddleBrown'), ('Chocolat', 'Chocolate'), 
        ('Sienne', 'Sienna'), ('Beige', 'Beige')
    ),
    'Violets': (
        ('Indigo', 'Indigo'), ('Pourpre', 'Purple'), ('Magenta', 'Magenta'), 
        ('Violet', 'Violet'), ('Prune', 'Plum')
    )
}

def get_circles_intersection(p1, p2, p3, p4):
  # Окружность 1: центр p1, точка на ободе p2
  # Окружность 2: центр p3, точка на ободе p4
  # p1,..,p4 list[x,y]
  x1, y1 = p1
  x2, y2 = p2
  x3, y3 = p3
  x4, y4 = p4
  r1 = math.sqrt((x2-x1)**2 + (y2-y1)**2)
  r2 = math.sqrt((x4-x3)**2 + (y4-y3)**2)
  d = math.sqrt((x3-x1)**2 + (y3-y1)**2)
  if d > r1 + r2 or d < abs(r1 - r2) or d == 0:
    return [] # Нет пересечений
  a = (r1**2 - r2**2 + d**2) / (2 * d)
  h = math.sqrt(max(0, r1**2 - a**2))
  x0 = x1 + a * (x3 - x1) / d
  y0 = y1 + a * (y3 - y1) / d
  rx = -(y3 - y1) * (h / d)
  ry = (x3 - x1) * (h / d)
  return [(x0 + rx, y0 + ry), (x0 - rx, y0 - ry)]

def get_lines_intersection(p1, p2, p3, p4):
    """
    Находит точку пересечения двух отрезков.
    Возвращает [x, y] или None, если отрезки не пересекаются.    
    """
    # Пример использования:
    # seg1 = [[0, 0], [10, 10]]
    # seg2 = [[0, 10], [10, 0]]
    # Print(get_lines_intersection(*seg1, *seg2)) # Вывод: [5.0, 5.0]
    
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    # Знаменатель (определитель)
    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    
    # Если знаменатель 0, отрезки параллельны
    if denom == 0:
        return None

    # Параметры положения точки пересечения на прямых
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom

    # Если ua и ub лежат в диапазоне от 0 до 1, то пересечение внутри отрезков
    if 0 <= ua <= 1 and 0 <= ub <= 1:
        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)
        return [x, y]

    return None

def get_circle_line_intersection(c_center, c_point, l_p1, l_p2, tol=1e-9):
    """
    Находит точки пересечения окружности и прямой.
    
    :param c_center: (x, y) центра окружности
    :param c_point: (x, y) точки на окружности
    :param l_p1: (x, y) первая точка на прямой
    :param l_p2: (x, y) вторая точка на прямой
    :param tol: погрешность для обработки чисел с плавающей точкой
    :return: список кортежей [(x1, y1), ...] точек пересечения (0, 1 или 2 точки)
    """
    cx, cy = c_center
    px, py = c_point
    x1, y1 = l_p1
    x2, y2 = l_p2
    
    # 1. Вычисляем квадрат радиуса окружности
    r_sq = (px - cx)**2 + (py - cy)**2
    
    # 2. Сдвигаем систему координат, делая центр окружности точкой (0, 0)
    x1_rel, y1_rel = x1 - cx, y1 - cy
    x2_rel, y2_rel = x2 - cx, y2 - cy
    
    # 3. Применяем стандартный алгоритм пересечения
    dx = x2_rel - x1_rel
    dy = y2_rel - y1_rel
    dr_sq = dx**2 + dy**2
    D = x1_rel * y2_rel - x2_rel * y1_rel
    
    # Вычисляем дискриминант
    discriminant = r_sq * dr_sq - D**2
    
    # Нет пересечений
    if discriminant < -tol:
        return []
    
    # Прямая касается окружности (одна точка)
    if abs(discriminant) < tol:
        x = (D * dy) / dr_sq
        y = (-D * dx) / dr_sq
        return [(x + cx, y + cy)]
    
    # Прямая пересекает окружность (две точки)
    sqrt_disc = math.sqrt(discriminant)
    sgn_dy = 1 if dy >= 0 else -1
    
    x_a = (D * dy + sgn_dy * dx * sqrt_disc) / dr_sq
    x_b = (D * dy - sgn_dy * dx * sqrt_disc) / dr_sq
    y_a = (-D * dx + abs(dy) * sqrt_disc) / dr_sq
    y_b = (-D * dx - abs(dy) * sqrt_disc) / dr_sq
    
    return [(x_a + cx, y_a + cy), (x_b + cx, y_b + cy)]

is_Voila = 'VOILA_REQUEST_URL' in os.environ
canvas = Canvas(width=1210, height=650) if is_Voila else Canvas(width=1100, height=500)

# Скрипт
editor = widgets.Textarea(
  #value = script_example.strip(),
  #placeholder='Введите ваш скрипт здесь...',
  layout=widgets.Layout(width='98%', height='100%')
)

# Терминал (командная строка)
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

# Кнопка запуска
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

def Print(*argv, clr=False, **kwarg):
  if is_Voila: return
  with L_out:
    if len(argv)==0:
      clear_output()
      return
    if clr: clear_output()
    print(*argv, **kwarg)
def Display(*argv, clr=False):
  if is_Voila: return
  with R_out:
    if clr: clear_output()
    display(*argv)
  
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

def termed():
  editor.value += f"{terminal.value}\n"
  terminal.value = ""; 

class engine():
  def __init__(self):
    self.pcode = {}
    self.macros = {}
    canvas.on_mouse_down(self.handle_click)
    self.restore()
    
  def save(self, filename="engine_state.json"):
    #Сохраняет текущие pcode и macros в JSON-файл.
    data = {
      'pcode': self.pcode,
      'macros': self.macros
    }
    try:
      with open(filename, 'w', encoding='utf-8') as f:
        # indent=4 делает файл читаемым для человека
        json.dump(data, f, ensure_ascii=False, indent=4)
      Print(f"✅ Данные сохранены в {filename}")
    except Exception as e:
      Print(f"❌ Ошибка сохранения: {e}")
    
  def restore(self, filename="engine_state.json"):
    """Загружает pcode и macros из JSON-файла."""
    try:
      with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
      self.pcode = data.get('pcode', {})
      self.macros = data.get('macros', {})
      Print(f"🔄 Данные успешно загружены из {filename}")
      Display(self.pcode, clr=1)
      Display(self.macros)
      # После загрузки данных вызываем перерисовку экрана
      #self.redraw()
    except FileNotFoundError:
      Print(f"⚠️ Файл {filename} не найден.")
    except Exception as e:
      Print(f"❌ Ошибка загрузки: {e}")    
    
  def reset(self):
    canvas.fill_style = '#2c3e50'
    canvas.fill_rect(0, 0, canvas.width, canvas.height)   
  
  def __repr__(self):
    display(vars(self))
    return ""
  
  def redraw(self, *kv):
    with hold_canvas():
      if len(kv) == 0:
        self.reset()
        Print()        
        for k,v in self.pcode.items():
          self.redraw(k, v)
      else:
        k,v = kv
        Print(f"{k=}; {v=}")
        if v[0] == ".": # point
          x,y = v[1:]
          canvas.fill_style = 'green'
          canvas.fill_arc(x, y, 3, 0, 7)      
          canvas.fill_style = 'yellow'
          canvas.font = '16px sans-serif'
          canvas.fill_text(k, x+8, y-8)
        elif v[0] == "=": # segment
          canvas.stroke_style = 'peru'          
          #o1o2 = [self.pcode[_][1:] for _ in self.pcode[k][1:] if _ in self.pcode]
          if len(o1o2:=[self.pcode[_][1:] for _ in self.pcode[k][1:] if _ in self.pcode]) == 2:
            o1, o2 = o1o2
            canvas.stroke_line(o1[0], o1[1], o2[0], o2[1])
        elif v[0] == "@": # circle
          #k='C1', v=('@', 'A', 'B')
          #o1, o2 = [self.pcode[_][1] for _ in self.pcode[k][1]]
          o1, o2 = v[1:]
          o1, o2 = self.pcode[v[1]][1:], self.pcode[v[2]][1:]
          radius = math.sqrt((o1[0] - o2[0])**2 + (o1[1] - o2[1])**2)
          canvas.begin_path()
          canvas.stroke_style = 'gold'
          canvas.arc(o1[0], o1[1], radius, 0, 2 * math.pi)
          canvas.stroke()
        elif v[0] == "+": # intersect
          sh1, sh2 = self.pcode.get(v[1]), self.pcode.get(v[2])
          if None in (sh1, sh2):
            return
          if sh1[0] == "@" and sh2[0] == "@":
            # пересечение окружностей
            p1234 = self.pcode[sh1[1]][1:], self.pcode[sh1[2]][1:], self.pcode[sh2[1]][1:], self.pcode[sh2[2]][1:]
            p1, p2= get_circles_intersection(*p1234)
            lb1, lb2 = k.split(',')
            self.pcode[lb1] = ('.', *p1); self.pcode[lb2] = ('.', *p2)
            self.redraw(lb1, ('.', *p1)); self.redraw(lb2, ('.', *p2))
            self.display()
          elif sh1[0] == "=" and sh2[0] == "=":
            # пересечение прямых  
            #get_lines_intersection(p1, p2, p3, p4)
            sh1, sh2 = self.pcode[v[1]], self.pcode[v[2]]
            p1234 = self.pcode[sh1[1]][1:], self.pcode[sh1[2]][1:], self.pcode[sh2[1]][1:], self.pcode[sh2[2]][1:]
            xy = get_lines_intersection(*p1234)
            self.redraw(k, ('.', *xy))
            self.display()
          elif sh1[0] == "@" and sh2[0] == "=":
            # пересечение окружности и прямой прямой
            # get_circle_line_intersection(c_center, c_point, l_p1, l_p2, tol=1e-9)
            p1234 = self.pcode[sh1[1]][1:], self.pcode[sh1[2]][1:], self.pcode[sh2[1]][1:], self.pcode[sh2[2]][1:]
            p1, p2= get_circle_line_intersection(*p1234)
            lb1, lb2 = k.split(',')
            self.pcode[lb1] = ('.', *p1); self.pcode[lb2] = ('.', *p2)
            self.redraw(lb1, ('.', *p1)); self.redraw(lb2, ('.', *p2))
            self.display()
            
  def display(self):
    Display(self.pcode, clr=1)

  def run(self, b):
    if editor.value[0] == '&':
      # регистрируем макрокоманду в self.macros      
      s1 = editor.value.split('&')
      s1 = s1[1].split('\n')
      s0 = s1[0].split()
      self.macros[s0[0]] = s1[0] , "\n".join([_ for _ in s1[1:] if _])      
      editor.value = ""
      Display(self.macros, clr=1)
    else:
      for cmd in editor.value.split('\n'):
         if len(cmd):
            self.cmd_exec(cmd, show=False)
      self.redraw()          
    
  def handle_click(self, x, y):
    lbl = terminal.value.split()
    if lbl[0] == '.':
      # добавить (изменить) точку
      #'A': ('.', ('12.3', '13.45')),
      self.pcode[lbl[1]] = ['.', x, y]
      #termed()
      self.display()
      self.redraw()
  
  def terminal(self, sender):
    #Print(f"{sender.value=}")
    valstrip = sender.value.strip()
    if valstrip == '%save':
      sender.value = editor.value = ""
      self.save()
    if valstrip == '%restore':
      sender.value = editor.value = ""
      self.restore()
    elif valstrip == "#":
      # чистим pcode
      sender.value = editor.value = ""
      self.pcode = {}
      self.display()
      self.redraw()
    elif valstrip == "##":
      # чистим macros
      sender.value = editor.value = ""
      self.macros = {}
      self.display()
      self.redraw()
    elif valstrip == "###":
      # чистим pcode & macros
      sender.value = editor.value = ""
      self.macros = {}
      self.display()
      self.redraw()
    elif valstrip == '?':
      # загружаем разметку
      self.display()
      sender.value = editor.value = ""
      for k,v in self.pcode.items():
        editor.value += " ".join((k, v[0], '' if v[0]=="." else " ".join(v[1:]))) + '\n'      
    elif valstrip[0] == '&':
      if len(valstrip) == 1:
        # загружаем перечень макрокоманд в editor
        editor.value = "\n".join([_ for _ in self.macros])
        if self.macros == {}:
          sender.value = ""
      elif valstrip[1:] in self.macros:
        # загружаем текст макрокоманды в editor для просмотра/редактирования
        sender.value = ""
        #editor.value = "\n".join((valstrip, self.macros[valstrip[1:]]))        
        editor.value = "&"+"\n".join((self.macros[valstrip[1:]]))
    else:
      self.cmd_exec(sender.value)

  def cmd_exec(self, cmd, show=True):
    val = cmd.split()
    if val[0] == '.':
      return
    elif val[0][0] == '!':
      # Исполняем макрокоманду
      # val[0][0], val[0][1:], val[1:]
      body = E.macros[val[0][1:]]
      n = 0
      for _ in val[1:]:
        n += 1
        body = body.replace(f"${n}", _)
      for cmd in body.split('\n'):
         if len(cmd):
            self.cmd_exec(cmd, show=False)
      self.redraw()
      termed()
    elif val[0] == '#':
      """удалить(если есть) объектЫ
      # p1,p2 p1 p2 p1p2 """
      for _ in val[1:]:
        self.pcode.pop(_, None)
      self.display()
      if show:
        self.redraw()
        termed()
    elif val[0] == "=":
      # отрезок
      if val[2] in self.pcode and val[3] in self.pcode:
        self.pcode[val[1]] = (val[0], val[2], val[3])
        self.display()
        if show:
          self.redraw()
          termed()
    elif val[0] == "@":
      # окружность по центру и точке
      if val[2] in self.pcode and val[3] in self.pcode:
        self.pcode[val[1]] = (val[0], val[2], val[3])
        self.display()
        if show:
          self.redraw()
          termed()
    elif val[0] == "+":
      # пересечение линий
      if val[2] in self.pcode and val[3] in self.pcode:
        self.pcode[val[1]] = (val[0], val[2], val[3])
        if ',' in val[1]:
          lb1, lb2 = val[1].split(',')
          self.pcode[lb1] = self.pcode[lb2] = ('.', -1,-1 )
        self.display()
        if show:
          self.redraw()
          termed()
        
  def first(self):
    self.redraw()
    return
    self.reset()
    canvas.fill_style = 'skyblue'  # Цвет заливки
    canvas.stroke_style = 'black'   # Цвет контура
    canvas.font = "86px serif"
    invite = "Euclide est à votre service !" #"Voilà!"  
    # Устанавливаем режим выравнивания
    canvas.text_align = 'center'    # Горизонтальное центрирование
    canvas.text_baseline = 'middle' # Вертикальное центрирование
    # Теперь указываем координаты ровно посередине холста
    canvas.fill_text(invite, canvas.width / 2, canvas.height / 2)
# class engine(): -----------------------------------------------------------------------
E = engine()

import warnings
#with warnings.catch_warnings():
#  warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
terminal.on_submit(E.terminal)

"""
def handle_enter(change):
  # 'change.new' — это строка текста, которая сейчас в поле
  # 'change.old' — старое значение

  # Срабатывает только тогда, когда значение реально изменилось и было подтверждено Enter
  if change['name'] == 'value':
    E.terminal(change['owner'])
# Запрещаем отправку при каждом вводе буквы
terminal.continuous_update = False
terminal.observe(handle_enter, names='value')
"""

run_btn.on_click(E.run)

canvas.on_client_ready(E.first)
clear_output()
display(out)
with out: 
  display(app_ui)

None