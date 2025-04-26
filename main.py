import tkinter as tk
from PIL import Image, ImageTk
import time
import threading
import json

def bitwiseAND(a:bool, b:bool) -> bool:
    return a and b

def bitwiseOR(a:bool, b:bool) -> bool:
    return a or b

def bitwiseNOT(a:bool) -> bool:
    return not a

def bitwiseXOR(a:bool, b:bool) -> bool:
    return a ^ b

class TkLogicSimError(BaseException):
    def __init__(self, msg):
        self.msg = msg

class Circuit:
    def __init__(self, pre_items: list = [], pre_wires: list = []):
        if type(pre_items) != list or type(pre_wires) != list:
            raise TkLogicSimError(f'Pre-items or Pre-wires are not a list')
        self.items = pre_items
        self.wires = pre_wires
    
    def add_wire(self, item1: int, item2: int) -> None:
        self.wires.append((item1, item2, []))
    
    def add_block(self, block: str, position: list) -> None:
        self.items.append((block, position, []))

tpsstr = input('Enter TPS [15]: ') # Max Ticks / Second
if tpsstr == '': tpsstr = 15
tps = int(tpsstr)

root = tk.Tk()
root.geometry('768x512')
root.title('tk-logicsim')
root.configure(bg='#000000') 

if tps > 20: raise TkLogicSimError(f'TPS is too high. ({tps})')
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

canvas = tk.Canvas(root, width=8192, height=8192, bg='black')
canvas.place(relx=0, rely=0, relwidth=1, relheight=1, anchor=tk.NW)
root.tk.call('lower', str(canvas))

print('TK-Logicsim started')

def render(circuit: Circuit) -> tuple:
    ##########
    #Blocks#
    ##########
    loaded_blocks = [None]*len(circuit.items)
    c = 0
    for i in circuit.items:
        if i[0] == 'Input' and not i[3][0]:
            loaded_blocks[c] = tk.Button(root, image=INPUT_OFF)
        elif i[0] == 'Output' and not i[3][0]:
            loaded_blocks[c] = tk.Button(root, image=OUTPUT_OFF)
        if i[0] == 'Input' and i[3][0]:
            loaded_blocks[c] = tk.Button(root, image=INPUT_ON)
        elif i[0] == 'Output' and i[3][0]:
            loaded_blocks[c] = tk.Button(root, image=OUTPUT_ON)
        elif i[0] == 'AND':
            loaded_blocks[c] = tk.Button(root, image=AND)
        elif i[0] == 'XOR':
            loaded_blocks[c] = tk.Button(root, image=XOR)
        elif i[0] == 'NOT':
            loaded_blocks[c] = tk.Button(root, image=NOT)
        elif i[0] == 'OR':
            loaded_blocks[c] = tk.Button(root, image=OR)

        loaded_blocks[c].place(x=i[1], y=i[2])

        loaded_blocks[c].configure(command=lambda i=c: toggle_input_or_output(i, circuit))
        c += 1
    c = 0

    #########
    #Wires#
    #########
    loaded_wires = []
    print('Render: ', end='')
    for i in circuit.wires:
        xy_input_a = (circuit.items[i[0]][1], circuit.items[i[0]][2])
        xy_output_b = (circuit.items[i[1]][1], circuit.items[i[1]][2])
        print(xy_input_a, xy_output_b, sep=', ', end=' - ')
        loaded_wires.append(canvas.create_line(xy_input_a[0]+50,xy_input_a[1]+25,xy_output_b[0]+50,xy_output_b[1]+25, width=2, fill='#ffffff'))
    print('Render End')

    return (loaded_blocks, loaded_wires)

citems = [['Input',35,35,[False,False]], ['Output',135,35,[False,False]]]
cwires = [[0,1]]

main_circuit = Circuit(citems, cwires)
tk_rendered = render(main_circuit)

def toggle_input_or_output(idx:int, circuit:Circuit) -> None:
    global tk_rendered
    if circuit.items[idx][3][0] == True:
        circuit.items[idx][3][0] = False
        circuit.items[idx][3][1] = False
    else:
        circuit.items[idx][3][0] = True
        circuit.items[idx][3][1] = True
    
    for i in tk_rendered[0]:
        i.destroy()
    
    canvas.delete('all')
    tk_rendered = render(main_circuit)

def tick(circuit:Circuit, rendered_circuit:tuple) -> None:
    for i in circuit.wires:
        circuit.items[i[1]][3][1] = circuit.items[i[0]][3][0]

    c = 0
    for i in circuit.items:
        i[3][0] = i[3][1]
        if i[3][0] == True:
            i[3][1] == True
        
        if i[0] == 'Input':
            rendered_circuit[0][c].configure(image=INPUT_ON if i[3][0] == True else INPUT_OFF)
        elif i[0] == 'Output':
            rendered_circuit[0][c].configure(image=OUTPUT_ON if i[3][0] == True else OUTPUT_OFF)
        else: ...
        c += 1
    c = 0
    # print(circuit.items, circuit.wires)


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