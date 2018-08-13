import sys
import random
import numpy


# le a entrada
with open(sys.argv[1]) as file:
    info = file.readline()
    content = file.readlines()

rows, columns = info.split(' ')
rows = int(rows)
columns = int(columns)
map = [list(line.strip()) for line in content]

alfa = float(sys.argv[2])
gamma = float(sys.argv[3])
iterations = int(sys.argv[4])

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

ACTIONS = [LEFT, UP, RIGHT, DOWN]

GOAL = '0'
DEATH = '&'
WALL = '#'
EMPTY = '-'
PACMAN = 'p'

q_table = dict()


def get_start(rows, columns, map):
    i = j = 0
    while(map[i][j] != EMPTY):
        i = random.randint(1, rows-1)
        j = random.randint(1, columns-1)
    return (i, j)


def choose_action(state, ACTIONS):
    if random.uniform(0,1) < gamma:
        return random.choice(ACTIONS)
    else:
        return numpy.argmax(q(state))

def get_next_state(state, map, action):
    new_state = (0, 0)
    if action == UP:
        new_state = (state[0] - 1, state[1])
    elif action == DOWN:
        new_state = (state[0] + 1, state[1])
    elif action == RIGHT:
        new_state = (state[0], state[1] + 1)
    elif action == LEFT:
        new_state = (state[0], state[1] - 1)
    if map[new_state[0]][new_state[1]] == WALL:
        new_state = state
    return new_state


def move(map, state, new_state):
    map[new_state[0]][new_state[1]] = 'p'
    map[state[0]][state[1]] = '-'


def act(map, new_state, state):
    new_position = map[new_state[0]][new_state[1]]
    if new_position == GOAL:
        reward = 10
        episode = True
        map[state[0]][state[1]] = '-'
    elif new_position == DEATH:
        reward = -10
        episode = True
        map[state[0]][state[1]] = '-'
    elif new_position == EMPTY:
        reward = -1
        episode = False
        move(map, state, new_state)
    elif new_position == PACMAN:
        reward = -1
        episode = False
    return reward, episode

def q(state, action = None):
    if state not in q_table:
        q_table[state] = numpy.zeros(len(ACTIONS))

    if action is None:
        return q_table[state]
    return q_table[state][action]

def print_politica(map, rows, columns):
    file = open("pi.txt", "w+")
    for i in range (1, rows-1):
        for j in range (1, columns-1):
            state = (i, j)
            if (map[i][j] == EMPTY)  or (map[i][j] == PACMAN):
                politica = numpy.argmax(q(state))
                if politica == RIGHT:
                    map[i][j] = '>'
                elif politica == LEFT:
                    map[i][j] = '<'
                elif politica == UP:
                    map[i][j] = '^'
                elif politica == DOWN:
                    map[i][j] = 'v'
    for line in map:
        for item in line:
            file.write(item)
        file.write('\n')


def print_q(q_table):
    file = open("q.txt", "w+")
    for state in q_table:
        file.write(str(state[0]) + ',' + str(state[1]) + ', esquerda,' + str(q_table[state][0]) + '\n')
        file.write(str(state[0]) + ',' + str(state[1]) + ', acima,' + str(q_table[state][1]) + '\n')
        file.write(str(state[0]) + ',' + str(state[1]) + ', direita,' + str(q_table[state][2]) + '\n')
        file.write(str(state[0]) + ',' + str(state[1]) + ', abaixo,' + str(q_table[state][3]) + '\n')


while (iterations>0):
    total_reward = 0
    episode = False
    # gerar estado inicial
    start_state = get_start(rows, columns, map)
    map[start_state[0]][start_state[1]] = 'p'
    state = start_state
    while ((episode == False) and (iterations > 0)):
        action = choose_action(state, ACTIONS)
        new_state = get_next_state(state, map, action)
        reward, episode = act(map, new_state, state)
        total_reward += reward
        q(state)[action] = q(state, action) + alfa * (reward + gamma * numpy.max(q(new_state)) - q(state, action))
        state = new_state
        iterations = iterations - 1
        if episode == True:
            break

# gerar os arquivos

print_politica(map, rows, columns)
print_q(q_table)
