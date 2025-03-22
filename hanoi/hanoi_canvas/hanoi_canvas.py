from ipycanvas import MultiCanvas, hold_canvas
from IPython.display import clear_output
from ipywidgets import Button, Output


# Recursive Python function to solve the tower of hanoi
def TowerOfHanoiSolver(n, src, aux, dst):
  order = []
  def move(n, src, aux, dst):
    if n <= 0:
      return
    move(n-1, src, dst, aux)
    order.append(f"{src}{dst}")
    move(n-1, aux, src, dst)
    # ~~~~~~~~~~~~~~~~~~~~~~
  move(n, src, aux, dst)
  return n, str(src), str(aux), str(dst), order
#moves = TowerOfHanoiSolver(3, 'A', 'B', 'C')
#moves


class tripleDraw:
  def __init__(self, labels):
    m = MultiCanvas(n_canvases=2, width=800, height=300)
    self.m = m
    
    self.tower_width = 6
    self.base_height = 20
    self.tower_spacing = self.m.width // 3
    self.disk_height = 20
    self.disk_width_step = 30    
    self.colors = ['red', 'green', 'gray', 'navy', 'blue', 'olive', 'purple', 'orange']
    #
    m[0].clear()
    m[0].fill_style = 'black'
    m[0].fill_rect(0, 0, m.width, m.height)

    # Draw bases
    m[0].fill_style = 'brown'
    m[0].fill_rect(0, m.height - self.base_height, m.width, self.base_height)

    # Draw towers
    m[0].fill_style = 'gray'
    for i in range(3):
      m[0].fill_rect(m.width //6 + i*m.width //3, 10, self.tower_width, m.height-10-self.base_height)
    # Labels
    m[0].fill_style = 'white'
    m[0].font = "26px serif"
    for i in enumerate(labels): 
      m[0].fill_text(str(i[1]) ,m.width //6 + i[0]*m.width //3 - self.tower_width, m.height-2, self.tower_width*3)
    # ~~~~~~~~~~~~~~~~~~~~~~
  def draw(self, towers):
    m = self.m
    m[1].clear()
    m[1].font = "20px serif"
    with hold_canvas():
      for i, tower in enumerate(towers):
        for j, disk in enumerate(towers[tower][::-1]):
          disk_width = disk * self.disk_width_step
          m[1].fill_style = self.colors[disk % len(self.colors)]
          m[1].fill_rect(self.m.width //6 + i * self.tower_spacing-disk_width//2 + self.tower_width //2, 
            m.height - self.base_height - (j + 1) * self.disk_height, disk_width, 
            self.disk_height)
          m[1].fill_style = 'white'
          m[1].fill_text(f"{disk}".center(4), 
                         self.m.width //6 + i*m.width //3 - self.tower_width, 
                         self.m.height - self.base_height - j * self.disk_height - 3)
    # ~~~~~~~~~~~~~~~~~~


def play_hanoi(moves, canvas, show):
  def next_hanoi():
    triple = {moves[1]: list(range(1,moves[0]+1)), moves[2]:[], moves[3]:[]}
    for m in moves[4]:
      show(triple)
      yield f"{m[0]} {chr(0x27BC)} {m[1]}"
      
      pop = triple[m[0]].pop(0)
      triple[m[1]].insert(0,pop)
      if m is moves[4][-1]:
        show(triple)
    # ~~~~~~~~~~~~
  out = Output()
  nexth = next_hanoi()
  next_button = Button()
  def on_next_button_click(b):
    if b.description == 'Ready!':
      with out: clear_output()
    b.description = next(nexth, 'Ready!')
    # ~~~~~~~~~~~~~~~~~~~~~~~
  next_button.on_click(on_next_button_click)
  display(out)
  with out: display(canvas,next_button)
  on_next_button_click(next_button)

def TowerOfHanoiRunner(n, src, aux, dst):
  moves = TowerOfHanoiSolver(n, src, aux, dst)
  trDr = tripleDraw(moves[1:4])
  play_hanoi(moves, trDr.m, trDr.draw)
