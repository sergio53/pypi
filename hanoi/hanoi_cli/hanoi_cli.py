#!/usr/bin/env python3

import sys
from os import system, name
try:
  from IPython.display import clear_output
except:
  pass  

# Recursive Python function to solve the tower of hanoi
def TowerOfHanoi(n, src, aux, dst):
  order = []
  def move(n, src, aux, dst):
    if n <= 0:
      return
    move(n-1, src, dst, aux)
    order.append(f"{src}{dst}")
    move(n-1, aux, src, dst)
    # ~~~~~~~~~~~~~~~~~~~~~~
  move(n, src, aux, dst)
  return n, src, aux, dst, order

def tripleView(layers):
  def disk(n):
    if n>0:
      return (mult*n*lchar +str(n) +mult*n*lchar).center(2*mult*altitude+1)
    return '|'.center(2*mult*altitude+1)
  
  altitude = sum([len(_) for _ in layers.values()])
  mult = 2
  lchar = '#'
  #lchar = chr(0x25AC)
  #lchar = chr(0x2593)
  lchar = chr(0x2580)

  print()  
  for line in range(altitude,0,-1):
    names = list(layers)
    for ly in names:
      layer = layers[ly]
      if len(layer)<line:
        if ly is names[-1]:
          print(disk(0))
        else:
          print(disk(0),end=' ')
      else:
        d = disk(layer[len(layer)-line])
        if ly is names[-1]:
          print(d)
        else:
          print(d,end=' ')

  print('_'*altitude*mult + names[0] + '_'*altitude*mult, end=' ')
  print('_'*altitude*mult + names[1] + '_'*altitude*mult, end=' ')
  print('_'*altitude*mult + names[2] + '_'*altitude*mult)
  print()

from os import system, name  
def clear():
  if 'clear_output' in globals():
    clear_output()
  system('cls' if name == 'nt' else 'clear')

def play_hanoi(moves, show):
  triple = {moves[1]: list(range(1,moves[0]+1)), moves[2]:[], moves[3]:[]}
  for m in moves[4]:
    clear()
    show(triple)
    if len(input(f"{m[0]} {chr(0x27BC)} {m[1]}\t"))>0:
      clear()
      break
    pop = triple[m[0]].pop(0)
    triple[m[1]].insert(0,pop)
    if m is moves[4][-1]:
      clear()
      show(triple)
# -------------------------------------------------
def main():  
  clear()
  if len(sys.argv)!=2:
    N = int(input("Entrez le nombre de disques > "))
  else:
    N= int(sys.argv[1])
  moves = TowerOfHanoi(N,'A','B','C')
  play_hanoi(moves, tripleView)
if __name__ == '__main__':
  main()
