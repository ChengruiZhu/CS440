# configs
import random
import time

# state
# {0: {(0,1):True}, 1: {(1,2):True}, 2: kill_set}

# config global
height = 8
width = 8
line = 2 
minmax_max_depth = 3
alpha_max_depth = 4
to_print = False

search_methods = [1, 1] # 0 is minmax, 1 is alpah-beta
evaluation_functions = [3, 1]
# 0 - dumb offensive 1
# 1 - dumb defensive 1
# 2 - my offensive 2
# 3 - my defensive 2

# result global 
moves = [0,0]
nodes = [0,0]
total_rumtime = 0
total_turns = 0

# min_max search global temps
temp_node = 0
start_time = 0
end_time = 0

# opponent color
def get_opponent_color(color):
  if color == 0:
    return 1
  if color == 1:
    return 0
  # throw error
  return -1

# pieces type: a simple map<pos, isAlive>
def count_remaining(pieces):
  return sum(1 for i in pieces.values() if i is True)

# count True for map
def self_remaining(state, color):
  pieces = state[color]
  return count_remaining(pieces)

# count False for map
def opponent_remaining(state, color):
  op_color = get_opponent_color(color)
  pieces = state[op_color]
  return count_remaining(pieces)

# evaluation h1d
def evaluation_function_defensive(state, color):

  num_remaining = self_remaining(state, color)
  return 2 * num_remaining + random.random()

# evaluation h1o
def evaluation_function_offensive(state, color):
  global height 
  op_num_remaining = opponent_remaining(state, color)
  return 2 * (30 - op_num_remaining) + random.random()



def n_step_forwarding_position(pos, n, color):
  y, x = pos
  ret = []
  if color is 0:
    for i in range(1, n + 1):
      for j in range(-i, i + 1):
        ret.append((y + i, x + j)) 
  else:
    for i in range(1, n + 1):
      for j in range(-i, i + 1):
        ret.append((y - i, x + j)) 

  return ret

def n_step_surrounding_position(pos, n):
  y, x = pos
  ret = []
  for i in range(-n, n + 1):
    for j in range(-n, n + 1):
      ret.append((y + i, x + j)) 
  return ret

# avoid this position
def dont_wanna_die(pos):
  y, x = pos
  if color is 0:
    p1 = (y + 1, x - 1)
    p2 = (y + 1, x + 1)
  else:
    p1 = (y - 1, x - 1)
    p2 = (y - 1, x + 1)
  return (p1, p2)

# promote this position
def have_bro_covered(pos):
  y, x = pos
  if color is 0:
    p1 = (y - 1, x - 1)
    p2 = (y - 1, x + 1)
  else:
    p1 = (y + 1, x - 1)
    p2 = (y + 1, x + 1)
  return (p1, p2)

def calculate_distance(y, color):
  global height
  if color is 0:
    return y
  if color is 1:
    return (height - 1) - y


# rule 2 - value distance from base
# rule 2 - pivot distance max
# rule 2 - value connection + 1 for any surrounding group
def calculate_score(state, color):
  global height
  score = 0
  pieces = state[color]
  opponent_pieces = state[get_opponent_color(color)]
  self_pieces = pieces
  for pos, v in pieces.items():
    if v is True:
      y, x = pos
      distance_to_base = calculate_distance(y, color)
      value_factor  = 1.25**distance_to_base
      distance_score = value_factor  * distance_to_base
      if height == distance_to_base + 1:
        distance_score = 10000000

      bros = have_bro_covered(pos)
      bro_score = 0
      for bro in bros:
        if bro in self_pieces and self_pieces[bro] is True:
          bro_score = 5 * value_factor

      dies = dont_wanna_die(pos)
      die_score = 0
      for die in dies:
        if die in opponent_pieces and opponent_pieces[die] is True:
          die_score = 5 * value_factor

      score += distance_score + bro_score - die_score
  return score

def evaluation_function_defensive_new(state, color):
  defensive_factor = 0.8
  offensive_factor = 0.2
  opp_score = calculate_score(state, get_opponent_color(color))
  self_score = calculate_score(state, color)
  return defensive_factor * self_score - offensive_factor * opp_score


def evaluation_function_offensive_new(state, color):
  #global height 
  #end_color = end_player(state, height)
  #if end_color > 0:
  #  if end_color == color:
  #    return float('inf')
  #  else:
  #    return float('-inf')

  defensive_factor = 0.2
  offensive_factor = 0.8
  opp_score = calculate_score(state, get_opponent_color(color))
  self_score = calculate_score(state, color)
  return defensive_factor * self_score - offensive_factor * opp_score

# TODO
# evaluation h2d h2o
def evaluation_function(state, color):
  global evaluation_functions
  e = evaluation_functions[color]
  if e == 0:
    return evaluation_function_offensive(state, color)
  elif e == 1:
    return evaluation_function_defensive(state, color)
  elif e == 2:
    return evaluation_function_offensive_new(state, color)
  elif e == 3:
    return evaluation_function_defensive_new(state, color)
  else:
    print('error evaluation_function')
    return evaluation_function_defensive_new(state, color)

# define state
# {0: {white pieces}, 1: {black peices}}
# return the init state
# type: state
def start_state(h, w, l):
  black_set = {}
  for i in range(l):
    for j in range(w):
      piece = (i,j)
      black_set[piece] = True 

  white_set = {}
  for i in range(l):
    for j in range(w):
      index_y = (h - 1) - i
      piece = (index_y,j)
      white_set[piece] = True
 
  kill_set = {}
  board = {0: black_set, 1: white_set, 2: kill_set}
  return board

# check if a state is end
# type: boolean
def is_end(state, h):
  black_pieces = state[0] 
  white_pieces = state[1] 

  first_row_index = 0
  last_row_index = h - 1 

  if self_remaining(state, 0) is 0:
    return True
  if self_remaining(state, 1) is 0:
    return True
  
  # reach last row
  # make sure alive?
  for piece in black_pieces:
    end_index = last_row_index
    if piece[0] is end_index:
      return True
  
  for piece in white_pieces:
    end_index = first_row_index
    if piece[0] is end_index:
      return True
  
  return False

# who is end
# 0 - black
# 1 - white
# -1 - not end
def end_player(state, h):
  black_pieces = state[0] 
  white_pieces = state[1] 

  first_row_index = 0
  last_row_index = h - 1 

  if self_remaining(state, 0) is 0:
    return True
  if self_remaining(state, 1) is 0:
    return True
  
  # reach last row
  # make sure alive?
  for piece in black_pieces:
    end_index = last_row_index
    if piece[0] is end_index:
      return 0
  
  for piece in white_pieces:
    end_index = first_row_index
    if piece[0] is end_index:
      return 1
  
  return -1
      
# color - color of piece to be killed
# only kill the piece if there is one
# since it's possible that the space is empty and the move is legal
def safe_kill(state, pos, depth, color):
  pieces = state[color]
  kill_set = state[2]
  if pos in pieces and pieces[pos] is True:
    pieces[pos] = False
    kill_set[(depth, pos)] = color
    
# revive only when there is a dead piece at correct level of move
# DFS ganrantee the each depth has one single move
def safe_revive(state, pos, depth):
  kill_set = state[2]
  if (depth, pos) in kill_set:
    color = kill_set[(depth, pos)]
    state[color][pos] = True
    del kill_set[(depth, pos)]

# move peice from origin to des
# assume all piece are alive when moving
# safe remove any piece at moving destination
def move_to(state, piece, move, depth, color):
  pieces = state[color]
  # may throw runtime error - make sure to keep it safe
  op_color = get_opponent_color(color) 
  safe_kill(state, move, depth, op_color)

  del pieces[piece]
  pieces[move] = True

  state[color] = pieces
  return state

#move_back(state, ori, des, color)
#existence of the piece is garanteesd
def move_back(state, origin, destination, depth, color):
  pieces = state[color]
  # may throw runtime error - make sure to keep it safe
  del pieces[destination]
  pieces[origin] = True
  safe_revive(state, destination, depth)

  state[color] = pieces
  return state

def has_self_piece(state, position, color):
  pieces = state[color]
  if position in pieces and pieces[position] is True:
    return True
  else:
    return False

def has_opponent_piece(state, position, color):
  opponent_color = get_opponent_color(color)
  pieces = state[opponent_color]
  if position in pieces and pieces[position] is True:
    return True
  else:
    return False

# check if the move is valid - straight
def is_valid_move_straight(state, move, color): 
  if has_self_piece(state, move, color) or has_opponent_piece(state, move, color):
    return False
  else:
    return True

# check if the move is valid - diagonal
def is_valid_move_diagonal(state, move, color):
  if has_self_piece(state, move, color):
    return False 
  return True

# check if the piece is on board 
def is_onboard(piece, w, h):
  y = piece[0]
  x = piece[1]
  if x < 0 or x >= w:
    return False
  if y < 0 and y >= h:
    return False
  return True

# generate explore item - do check move
# type: operation
def expand_piece(state, piece, color, w, h):
  # move type 1,2,3 - [direct, left, and right]
  # bound check
  # go direct check
  # piece check - diagnal rule
  # peice check - direct rule

  ret = [] 
  
  if not has_self_piece(state, piece, color):
    return ret

  y = piece[0]
  x = piece[1]

  if color is 0: # black go down 
    straight = (y + 1, x) 
    dig_left = (y + 1, x - 1)
    dig_right = (y + 1, x + 1)
    digs = [dig_left, dig_right]

  if color is 1: # white go up
    straight = (y - 1, x) 
    dig_left = (y - 1, x - 1)
    dig_right = (y - 1, x + 1)
    digs = [dig_left, dig_right]

  # for straight case
  if is_onboard(straight, w, h) and is_valid_move_straight(state, straight, color):
    move = (piece, straight, color)
    ret.append(move)

  # for diagonal cases  
  for dig in digs:
    if is_onboard(dig, w, h) and is_valid_move_diagonal(state, dig, color):
      move = (piece, dig, color)
      ret.append(move)

  return ret


# generate the exploring set
def expand_pieces(state, color, w, h):
  ret = []
  pieces = state[color]
  for piece in pieces.keys():
    ret += expand_piece(state, piece, color, w, h)
  return ret

# move_to with operation type enabled
# -- high-level interface
def operate(state, operation, depth):
  ori, des, color = operation
  move_to(state, ori, des, depth, color) 

# move_back with operation type enabled
# -- high-level interface
# |~hi
def undo(state, operation, depth):
  ori, des, color = operation
  move_back(state, ori, des, depth, color)

# return a valid move
# -- game-level interface
def minmax_search_wrapper(state, color, max_depth, w, h): 
  global temp_node
  global nodes
  global is_ab_search
  is_ab_search = False

  temp_node = 0
  score, operation =  minmax_search(state, color, max_depth, 0, w, h, None, None)

  nodes[color] += temp_node

  return operation

# ab_search_global temp
is_ab_search = False
def alpha_beta_search_wrapper(state, color, max_depth, w, h):
  global temp_node
  global nodes
  global is_ab_search
  is_ab_search = True

  temp_node = 0
  score, operation =  minmax_search(state, color, max_depth, 0, w, h, None, None)

  nodes[color] += temp_node

  return operation

def is_using_max(max_depth):
  turn = max_depth % 2
  if turn is 0:
    return True
  else:
    return False

# find max 
# def type - search result - tuple (score, operation)
def find_max(operations): 
  return max(operations, key=lambda item:item[0])

# find min
# def type - search result - tuple (score, operation)
def find_min(operations): 
  return min(operations, key=lambda item:item[0])

# is min 
def is_max(turn):
  if turn is 0:
    return True
  return False

# def type - search result - tuple (score, operation)
def minmax_search(state, color, max_depth, depth, w, h, alpha, beta):
  global temp_node
  global is_ab_search
  # expand first
  # max / min the search  
  turn = depth % 2
  ret = [] # find min or max of the result
  

  # base case
  if (depth is max_depth):
    operation = (-1, -1)
    value = evaluation_function(state, color)
    return (value, operation)

  temp_node += 1
  # you have to online min or max, otherwise you can't cut
  operations = expand_pieces(state, color, w, h)
  for operation in operations: 
      operate(state, operation, depth)
      value, prev_op = minmax_search(state, color, max_depth, depth + 1, w, h, alpha, beta)
      ret.append((value, operation))
      undo(state, operation, depth)
      # check every time
      if is_ab_search is True:
        if is_max(turn): 
          if beta is not None and value >= beta:
            break
          if alpha is None or value > alpha:
            alpha = value
        else:
          if alpha is not None and value <= alpha:
            break
          if beta is None or value < beta:
            beta = value
  # so the real important thing is to rank  
  #print('branching factor', len(ret), 'depth', depth)
  if is_max(turn):
    max_operation = find_max(ret) 
    return max_operation
  else:
    min_operation = find_min(ret)
    return min_operation

search_ab = False
# search for the nextmove
# game-level interface
def search_next_move(state, color, max_depth, w, h):
  global search_ab
  if search_ab is True:
    print('alpha beta', color)
    operation = alpha_beta_search_wrapper(state, color, max_depth, w, h)
  else:
    print('minmax ', color)
    operation = minmax_search_wrapper(state, color, max_depth, w, h)
  return operation

def change_color(color):
  return (color + 1) % 2

def get_winner_color(color_of_last_player):
  return change_color(color_of_last_player) 

# game-level
# debug tool
# CLI graphic interface
def print_board(state, ori, w, h):

  brd = '===='
  for i in range(w):
    brd += '='

  num = '   '
  for i in range(w):
    num += str(i)
  print(num)
  print('')
  
  for j in range(h):
    board = str(j) + '  '
    for i in range(w):
      if (j, i) == ori:
        board += ' '
      elif (j, i) in state[0] and state[0][(j, i)] is True:
        board += 'X'
      elif (j, i) in state[1] and state[1][(j, i)] is True:
        board += 'O'
      else:
        board += ' '
    print(board)
  print(brd)
 

def print_summary(state, color):
  global nodes
  global moves

  black = 0
  white = 1

  winner = get_winner_color(color)
  if winner is 0:
    print('Winner: Black')
  else:
    print('Winner: White')

  print('Moves(Black): ' + str(moves[black])) 
  print('Moves(White): ' + str(moves[white])) 

  print('Nodes(Black): ' + str(nodes[black])) 
  print('Nodes(White): ' + str(nodes[white])) 

  print('Nodes/Turn(Black): ' + str(nodes[black] / float(moves[black]))) 
  print('Nodes/Turn(White): ' + str(nodes[white] / float(moves[white]))) 

  avg = (nodes[black] + nodes[white]) / float(moves[black] + moves[white]) 
  print('Avg Nodes(Both): ' + str(avg))
  
# -- game-level procedural control
game_state = start_state(height, width, line)
color = 0 # black first
depth  = 0

print_board(game_state, (-1, -1), width, height)
# count time
start_time = time.time()
while (not is_end(game_state, height)):
  moves[color] += 1

  search_method = search_methods[color]
  if search_method == 0:
    search_ab = False
    maxdepth = minmax_max_depth
  else:
    search_ab = True
    maxdepth = alpha_max_depth
  next_move_operation = search_next_move(game_state, color, maxdepth, width, height)
  operate(game_state, next_move_operation, depth)
    
  print_board(game_state, next_move_operation[0], width, height)
  color = change_color(color)
  depth += 1
  
end_time = time.time()
duration = end_time - start_time
print("END OF GAME")
print_board(game_state, next_move_operation[0], width, height)
print("Duration: " + str(duration)) 
print_summary(game_state, color)
print("Duration Per Move:" + str(duration / sum(moves)))

b_captured = sum(1 for v in game_state[2].values() if v is 0)
w_captured = sum(1 for v in game_state[2].values() if v is 1) 
print("Captured (Black):" + str(b_captured))
print("Captured (White):" + str(w_captured))
