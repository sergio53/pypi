pcode = {}

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

def redraw(*kv):
  with hold_canvas():  
    if len(kv) == 0:
      canvas_init()
      for k,v in pcode.items():
        redraw(k, v)
    else:
      k,v = kv
      Print(f"{k,v=}", clr=True)
      if v[0] == ".":   # point
        x,y = v[1:]
        if not x in pcode:
          # not link
          canvas.fill_style = 'green'
          canvas.fill_arc(x, y, 3, 0, 7)      
          canvas.fill_style = 'yellow'
          canvas.font = '16px sans-serif'
          canvas.fill_text(k, x+8, y-8)
      elif v[0] == "=": # segment
        canvas.stroke_style = 'peru'          
        if len(o1o2:=[pcode[_][1:] for _ in pcode[k][1:] if _ in pcode]) == 2:
          o1, o2 = o1o2
          canvas.stroke_line(o1[0], o1[1], o2[0], o2[1])
      elif v[0] == "@": # circle
        if len(v[1:]) ==2:
          # @ cAB A B
          o1, o2 = pcode[v[1]][1:], pcode[v[2]][1:]
          radius = math.sqrt((o1[0] - o2[0])**2 + (o1[1] - o2[1])**2)
        elif len(v[1:]) ==3:
          # @ cBCA B C A
          o1, o2, o3 = pcode[v[1]][1:], pcode[v[2]][1:], pcode[v[3]][1:]
          Print(f"{o1, o2, o3=}")
          radius = math.sqrt((o2[0] - o3[0])**2 + (o2[1] - o3[1])**2)
        Print(f"{radius=}")
        canvas.begin_path()
        canvas.stroke_style = 'gold'
        canvas.arc(o1[0], o1[1], radius, 0, 2 * math.pi)
        canvas.stroke()
      elif v[0] == "+": # intersect
        sh1, sh2 = pcode.get(v[1]), pcode.get(v[2])
        if None in (sh1, sh2):
          return
        if sh1[0] == "@" and sh2[0] == "@":
          # пересечение окружностей
          p1234 = pcode[sh1[1]][1:], pcode[sh1[2]][1:], pcode[sh2[1]][1:], pcode[sh2[2]][1:]
          p1, p2= get_circles_intersection(*p1234)
          lb1, lb2 = k.split(',')
          pcode[lb1] = ('.', *p1); pcode[lb2] = ('.', *p2)      
      else:
        return

def handle_cmd(cmd):
  lbl = cmd.split()
  pcode[lbl[1]] = (lbl[0], *lbl[2:])
    
def handle_term(sender):
  valstrip = sender.value.strip()
  Print("{valstrip=}")
  if valstrip[0] == '.':
    return
  if valstrip == '?':
    # загружаем разметку
    sender.value = editor.value = ""
    for k,v in pcode.items():
      editor.value += " ".join((k, v[0], '' if v[0]=="." else " ".join(v[1:]))) + '\n'      
  else:
    handle_cmd(valstrip)
    redraw()
    Display(pcode, clr=True)
    editor.value += f"{valstrip}\n"
    sender.value = ""

def handle_click(x, y):
  lbl = terminal.value.split()
  if lbl[0] == '.':
    # добавить (изменить) точку
    #'A': ('.', ('12.3', '13.45')),
    pcode[lbl[1]] = ['.', x, y]
  else:
    Print(f"{terminal.value=}")
    handle_cmd(terminal.value)    
  redraw()
  Display(pcode, clr=True)
canvas.on_mouse_down(handle_click)

terminal.on_submit(handle_term)

#run_btn.on_click(E.run)
