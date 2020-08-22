# Ghazal Sadeghian(9533054) - Project 2


numOfActions = 0
result = {}
H = {}
s = None
a = None
actions = None
blueE = False
redE = False
mushroomNum = 0
reds = []
blues = []
obstacles = []
f = open("Mario.txt", "r")
lines = f.read().splitlines()
n = int(lines[0])
m = int(lines[1])
ss = lines[2]
k = int(lines[3])
mushroomNum = 2 * k
for i in range(k):
    reds.append(lines[4 + i])
for j in range(k):
    blues.append(lines[4 + k + j])

for o in range(4 + (2 * k), len(lines)):
    obstacles.append(lines[o])
f.close()


def LRTA(ss):
    global numOfActions
    global n
    global m
    global H
    global result
    global s
    global a
    if isGoal(ss):
        a = "finish"
        return a
    else:
        if ss not in H.keys():
            H[ss] = heuristic(ss)
        if s is not None:
            result[(s, a)] = ss

            H[s] = min(LrtaCost(s, b, result.get((s, b)), H) for b in getActions(n, m, s))
            print("H from state: ", s, "changed to: ", H[s])

        a = min(getActions(n, m, ss), key=lambda b: LrtaCost(ss, b, result.get((ss, b)), H))
        numOfActions = numOfActions + 1
        print("prev state: ", s, " state: ", ss, " selected action: ", a)

        s = ss
        return a


def isGoal(ss):
    global blueE
    global redE
    checkMushrooms(ss)
    if (blueE == True) and (redE == True):
        return True
    else:
        return False


def checkMushrooms(ss):
    global mushroomNum
    global blueE
    global redE
    global reds
    global blues
    if ss in reds:
        print("RED mushroom found!!!")
        mushroomNum = mushroomNum - 1
        reds.remove(ss)
        redE = True
    elif ss in blues:
        print("BLUE mushroom found!!!")
        mushroomNum = mushroomNum - 1
        blues.remove(ss)
        blueE = True


def heuristic(s):
    return minManhattanDistance(s)


def minManhattanDistance(ss):
    global reds
    global blues
    min = 20000
    for red in reds:
        amount = abs(int(ss.split()[0]) - int(red.split()[0])) + abs(int(ss.split()[1]) - int(red.split()[1]))
        if amount < min:
            min = amount
    for blue in blues:
        amount = abs(int(ss.split()[0]) - int(blue.split()[0])) + abs(int(ss.split()[1]) - int(blue.split()[1]))
        if amount < min:
            min = amount

    return min


def maxManhattanDistance(ss):
    global reds
    global blues
    max = 0
    totalMushrooms = reds + blues
    if ss in totalMushrooms:
        totalMushrooms.remove(ss)
    for x in totalMushrooms:
        for y in totalMushrooms:
            amount = abs(int(x.split()[0]) - int(y.split()[0])) + abs(int(x.split()[1]) - int(y.split()[1]))
            if amount > max:
                max = amount
    return max


def numOfRemainingMushrooms(ss):
    global mushroomNum
    global reds
    global blues
    totalMushrooms = reds + blues
    if ss in totalMushrooms:
        res = mushroomNum - 1
        return res
    else:
        return mushroomNum


def LrtaCost(s, a, ss, H):
    # print(s, a, ss)
    if ss is None:
        return heuristic(s)
    else:
        try:
            return 1 + H[ss]
        except:
            return 1 + heuristic(ss)


def getActions(row, col, state):
    moves = []
    targetRow = int(state.split()[0])
    targetCol = int(state.split()[1])

    # moving up
    if targetRow < row:
        moves.append("R")
    # moving right
    if targetCol < col:
        moves.append("U")
    # moving down
    if targetRow > 1:
        moves.append("L")
    # moving left
    if targetCol > 1:
        moves.append("D")

    return moves


out = LRTA(ss)
while out != "finish":

    if out == "R":
        ss = str(int(s.split()[0]) + 1) + " " + (s.split()[1])
        if ss in obstacles:
            ss = s
    elif out == "L":
        ss = str(int(s.split()[0]) - 1) + " " + (s.split()[1])
        if ss in obstacles:
            ss = s
    elif out == "U":
        ss = (s.split()[0]) + " " + str(int(s.split()[1]) + 1)
        if ss in obstacles:
            ss = s
    elif out == "D":
        ss = (s.split()[0]) + " " + str(int(s.split()[1]) - 1)
        if ss in obstacles:
            ss = s

    out = LRTA(ss)
print("prev state: ", s, " state: ", ss, " selected action: ", a)
print("Number of actions: ", numOfActions)
