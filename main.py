import tkinter as tk
from PIL import Image, ImageTk
import time
import threading
import json

class TkLogicSimError(BaseException):
    def __init__(self, msg):
        self.msg = msg

class Circuit:
    def __init__(self, pre_items: list = [], pre_wires: list = []):
        if type(pre_items) != list or type(pre_wires) != list:
            raise TkLogicSimError(f'Pre-items or Pre-wires are not a list')
        self.items = pre_items
        self.wires = pre_wires

tpsstr = input('Enter TPS [25]: ')
if tpsstr == '': tpsstr = 25
tps = int(tpsstr) # Max Ticks / Second

first_click = None
second_click = None
mode = 'interact'
block = 'input'

def enableBuild(event=None):
    global mode
    mode = 'build'

def enableInteract(event=None):
    global mode
    mode = 'interact'

def enableWire(event=None):
    global mode
    mode = 'wire'

def on_click(event=None, block_idx=None) -> None:
    global tk_rendered, mode, block, first_click, second_click
    print(f'click at (x: {event.x}, y: {event.y}) (mode: {mode})')
    if mode == 'build':
        main_circuit.items.append([block,event.x,event.y,[False,False]])
        tk_rendered[0].append(None)
        tk_rendered = render(main_circuit)

root = tk.Tk()
root.geometry('768x512')
root.title('tk-logicsim')
root.configure(bg='#000000')
root.focus_force()

root.bind('<Button-1>', on_click)
root.bind('<Control-Key-1>', enableBuild)
root.bind('<Control-Key-2>', enableInteract)
root.bind('<Control-Key-3>', enableWire)

if tps > 25000: raise TkLogicSimError(f'TPS is too high. ({tps})')
if tps < 1: raise TkLogicSimError(f'TPS is too low ({tps})')

te = 0 # Ticks Elapsed
ttps = 0 # True Ticks / Second

INPUT_OFF = ImageTk.PhotoImage(Image.open('images/input_off.png').resize((50,50)))
INPUT_ON = ImageTk.PhotoImage(Image.open('images/input_on.png').resize((50,50)))
OUTPUT_OFF = ImageTk.PhotoImage(Image.open('images/output_off.png').resize((50,50)))
OUTPUT_ON = ImageTk.PhotoImage(Image.open('images/output_on.png').resize((50,50)))
AND = ImageTk.PhotoImage(Image.open('images/and.png').resize((50,50)))
XOR = ImageTk.PhotoImage(Image.open('images/xor.png').resize((50,50)))
NOT = ImageTk.PhotoImage(Image.open('images/not.png').resize((50,50)))
OR = ImageTk.PhotoImage(Image.open('images/or.png').resize((50,50)))

canvas = tk.Canvas(root, width=8192, height=8192, bg='black', highlightthickness=0, bd=0)
canvas.place(relx=0, rely=0, relwidth=1, relheight=1, anchor=tk.NW)
root.tk.call('lower', str(canvas))

print('TK-Logicsim started\n')

print('Controls:\n[Ctrl+1] to switch to build mode\n[Ctrl+2] to switch to interact mode\n')

def render(circuit: Circuit, verbose:bool=False) -> tuple:
    ##########
    #Blocks#
    ##########
    loaded_blocks = [None]*len(circuit.items)
    c = 0
    for i in circuit.items:
        if i[0] == 'input' and not i[3][0]:
            loaded_blocks[c] = tk.Button(root, image=INPUT_OFF, highlightthickness=0, borderwidth=0)
        elif i[0] == 'output' and not i[3][0]:
            loaded_blocks[c] = tk.Button(root, image=OUTPUT_OFF, highlightthickness=0, borderwidth=0)
        if i[0] == 'input' and i[3][0]:
            loaded_blocks[c] = tk.Button(root, image=INPUT_ON, highlightthickness=0, borderwidth=0)
        elif i[0] == 'output' and i[3][0]:
            loaded_blocks[c] = tk.Button(root, image=OUTPUT_ON, highlightthickness=0, borderwidth=0)
        elif i[0] == 'AND':
            loaded_blocks[c] = tk.Button(root, image=AND, highlightthickness=0, borderwidth=0)
        elif i[0] == 'XOR':
            loaded_blocks[c] = tk.Button(root, image=XOR, highlightthickness=0, borderwidth=0)
        elif i[0] == 'NOT':
            loaded_blocks[c] = tk.Button(root, image=NOT, highlightthickness=0, borderwidth=0)
        elif i[0] == 'OR':
            loaded_blocks[c] = tk.Button(root, image=OR, highlightthickness=0, borderwidth=0)

        loaded_blocks[c].place(x=i[1], y=i[2])

        loaded_blocks[c].configure(command=lambda i=c: toggle_input_or_output(i, circuit))
        c += 1
    c = 0

    #########
    #Wires#
    #########
    loaded_wires = []
    print('Render: ', end='') if verbose else ...
    for i in circuit.wires:
        xy_input_a = (circuit.items[i[0]][1], circuit.items[i[0]][2])
        xy_output_b = (circuit.items[i[1]][1], circuit.items[i[1]][2])
        print(xy_input_a, xy_output_b, sep=', ', end=' - ') if verbose else ...
        loaded_wires.append(canvas.create_line(xy_input_a[0]+50,xy_input_a[1]+25,xy_output_b[0]+50,xy_output_b[1]+25, width=2, fill='#ffffff'))
    print('Render End') if verbose else ...

    return (loaded_blocks, loaded_wires)

init_citems = [['input',35,35,[False,False]], ['input',35,135,[False,False]], ['AND',135,35,[False,False]], ['XOR',135,135,[False,False]], ['output',235,135,[False,False]], ['output',235,35,[False,False]]]
init_cwires = [[0,2], [0,3], [1,2], [1,3], [3,4], [2,5]]

main_circuit = Circuit(init_citems, init_cwires)
tk_rendered = render(main_circuit, True)

def toggle_input_or_output(idx:int, circuit:Circuit) -> None:
    global tk_rendered
    if circuit.items[idx][3][0] == True:
        circuit.items[idx][3][0] = False
        circuit.items[idx][3][1] = False
        tk_rendered[0][idx].configure(image=INPUT_OFF)
    else:
        circuit.items[idx][3][0] = True
        circuit.items[idx][3][1] = True
        tk_rendered[0][idx].configure(image=INPUT_ON)

def tick(circuit:Circuit, rendered_circuit:tuple) -> None:
    for item in circuit.items:
        if item[0] != 'input':
            item[3][1] = False

    inputs_to = [[] for _ in range(len(circuit.items))]

    for wire in circuit.wires:
        src, dst = wire
        inputs_to[dst].append(src)

    for idx, sources in enumerate(inputs_to):
        if circuit.items[idx][0] == 'input':
            continue

        if sources and circuit.items[idx][0] != 'AND' and circuit.items[idx][0] != 'NOT' and circuit.items[idx][0] != 'XOR':
            circuit.items[idx][3][1] = any(circuit.items[src][3][0] for src in sources)

        ## Logic
        if circuit.items[idx][0] == 'AND':
            if circuit.items[sources[0]][3][0] and circuit.items[sources[1]][3][0]:
                circuit.items[idx][3][1] = True
        elif circuit.items[idx][0] == 'NOT':
            circuit.items[idx][3][1] = not circuit.items[sources[0]][3][0]
        elif circuit.items[idx][0] == 'XOR':
            if circuit.items[sources[0]][3][0] ^ circuit.items[sources[1]][3][0]:
                circuit.items[idx][3][1] = True

    for idx, item in enumerate(circuit.items):
        item[3][0] = item[3][1]

        try:
            if item[0] == 'input':
                rendered_circuit[0][idx].configure(image=INPUT_ON if item[3][0] else INPUT_OFF)
            elif item[0] == 'output':
                rendered_circuit[0][idx].configure(image=OUTPUT_ON if item[3][0] else OUTPUT_OFF)
            else:
                ...
        except tk.TclError:
            print('tick: button does not exist, skipping.')
            pass
        except Exception as e:
            pass


def looptick() -> None:
    global te
    while True:
        time.sleep(1/tps)
        root.title(f'tk-logicsim ({te} ticks elapsed) ({ttps}/{tps} tps)')
        tick(circuit=main_circuit, rendered_circuit=tk_rendered)
        te += 1
    te = 0

def truetps() -> None:
    global te
    global ttps
    pte = te
    while True:
        time.sleep(0.5)
        cte = te
        ttps = 2 * (cte - pte)
        pte = cte
        

tlooptick = threading.Thread(target=looptick, daemon=True)
tlooptick.start()

ttruetps = threading.Thread(target=truetps, daemon=True)
ttruetps.start()

root.mainloop()