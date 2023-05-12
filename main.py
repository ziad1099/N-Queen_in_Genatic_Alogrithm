from graphics import *
import time
import easygui
import random

'''
This is Simple genatic algorithm to solve n-queens problem 
"N-queen problem" is N*N chess board you want to put N queens on it but no Queen attack another 
so we use chromosome legthn = N (user input) and each gene is represent colum cell in each row (row = index(gene))
fitness funcation here is number of non attacking pair of queens (max fitness =n*(n-1)/2)
crossover used is  uniform crossover
mutation is change random gene to new random value 
perant selection we use roulette wheal selection 
GUI is cerated used Graphics lib

devolped with all love by Ziad Helay 
'''
#Gui funcations
def Board(n): #chess GUI
    global win
    win = GraphWin("nQueen",500,550)
    win.setBackground("#448AFF")
    color=True
    global board
    board=[[] for i in range(n)]
    for r in range(n):
        board[r]=[]
        if n%2==0:
            color=not color
        for c in range(n):
            board[r].append(Rectangle(Point(0,500-r*(500//n)),Point(0+(500//n),500-r*(500//n)-(500//n))))
            board[r][c].move((500//n)*c,0)
            if color:
                board[r][c].setFill("#303F9F")
            else:
                board[r][c].setFill("#FFFFFF")

            board[r][c].draw(win)
            color=not color



def txt(message):
    text=Text(Point(250,525),message)
    text.setStyle("bold")
    text.setSize(20)
    text.setTextColor("#212121")
    text.draw(win)
    return text
def delet_txt(text):
    text.undraw()
    del text

def put_in_board(choromosom):
    o=0
    global t
    t=[]
    a=0
    for i in choromosom:
        t.append(Text(board[o][i-1].getCenter(),"♛"))
        t[a].setSize(24)
        t[a].setOutline("black")
        t[a].setStyle("bold")
        t[a].draw(win)
        o+=1
        a+=1
def delet_Q():
    for i in t:
        i.undraw()
        del i

#GA Algorithm
def random_chromosome(size):
    return [ random.randint(1, nq) for _ in range(nq) ]

def fitness(solution):
    n = len(solution)
    conflicts = 0

    for i in range(n):
        for j in range(i+1, n):
            if solution[i] == solution[j] or abs(solution[i]-solution[j]) == abs(i-j):
                conflicts += 1

    return maxFitness-conflicts


def probability(chromosome, maxFitness):
    return fitness(chromosome) / maxFitness


def roulette_wheel_selection(population, probabilities):
    total = sum(probabilities)
    r = random.uniform(0, total)
    populationWithProbabilty = zip(population, probabilities)
    upto = 0
    for c, w in populationWithProbabilty:
        if upto + w >= r:
            return c
        upto += w

def crossover(x,y): #uniform crossover
    n=len(x)
    # u=[random.randint(0,1) for _ in range(n)]
    mask=random.choices([0,1],k=n)
    child=[]
    for i in range(n):
        if mask[i]==1:
            child.append(y[i])
        else:
            child.append(x[i])
    return child

def mutate(x):
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x


def generate_population(population, maxFitness):
    global mutation_probability
    # mutation_probability = 0.1
    new_population = []
    probabilities = [probability(n, maxFitness) for n in population]
    for _ in range(len(population)):
        x = roulette_wheel_selection(population, probabilities)
        y = roulette_wheel_selection(population, probabilities)
        child = crossover(x, y)
        if random.random() < mutation_probability:
            child = mutate(child)
        new_population.append(child)
        if fitness(child) == maxFitness: break
    
    return new_population

def mainLoop():

    try:
        population = [random_chromosome(nq) for _ in range(population_size)]
        generation = 1
        solved=True
        
        text=txt("Solving...")
        while True:
            population = generate_population(population, maxFitness)
            popFitness = max([fitness(n) for n in population])
            maxCh=[]
            for i in population:
                if fitness(i)==popFitness:
                    maxCh=i
            put_in_board(maxCh)

            if popFitness==maxFitness: break
            generation += 1
            if generation>max_generations:
                solved=False
                break
            time.sleep(delayed_time)
            delet_Q()
        
        delet_txt(text)
        if solved:
            message=f"Solved in generation {generation} !!"
            text=txt(message)
        else:
            message="No Solutions in this limit,try again!"
            text=txt(message)
            tryAgain=easygui.boolbox("Want to try again?","try again",("Try again","close"))
            if tryAgain:
                delet_Q()
                delet_txt(text)
                mainLoop()
        win.getKey()
    except:
        win.close()


if __name__ == "__main__":
    try:
        nq =int(easygui.enterbox("Enter Numbers of Queens!!","N-Queens"))
        maxFitness = (nq*(nq-1))/2
        
        if nq in [2,3]:
            easygui.msgbox("No Solutions for this N!!","Program finished")
            exit()
        check=easygui.boolbox('''Popluation Size = 100
                            \nMax Number of Generations =Ulimated
                            \nMutation percent = 10%
                            \nDelayed time= 0.01s''',"Basic parametars",("Continue","Modify?"))
        if not check:
            population_size=int(easygui.enterbox("Enter population size","population size"))
            max_generations=int(easygui.enterbox("Enter Max Number of Generations","max generations"))
            mutation_probability=float(easygui.enterbox("Enter Mutation percent% ","mutation probability"))/100
            delayed_time=float(easygui.enterbox("Enter Delayed time","delayed time"))
        else:
            population_size=100
            max_generations=sys.maxsize
            mutation_probability=0.1
            delayed_time=0.01
        
        Board(nq)
        mainLoop()
            
    except:
        try:
            win.close()
        except:
            print("End!!")

#Devolped by Ziad Helaly 