import tkinter as tk
from PIL import Image, ImageTk

class TkLogicSimError(BaseException):
    def __init__(self, msg):
        self.msg = msg

class Circuit:
    def __init__(self, pre_items: list = [], pre_wires: list = []):
        if type(pre_items) != list or type(pre_wires) != list:
            raise TkLogicSimError(f'Pre-items or Pre-wires are not a list')
        self.items = pre_items
        self.wires = pre_wires
    
    def add_wire(self, item1: int, item2: int):
        self.wires.append((item1, item2, []))
    
    def add_block(self, block: str, position: list):
        self.items.append((block, position, []))

root = tk.Tk()
root.geometry('768x512')
root.title('tk-logicsim')

INPUT_OFF = ImageTk.PhotoImage(Image.open('images/input_off.png').resize((50,50)))
INPUT_ON = ImageTk.PhotoImage(Image.open('images/input_on.png').resize((50,50)))
OUTPUT_OFF = ImageTk.PhotoImage(Image.open('images/output_off.png').resize((50,50)))
OUTPUT_ON = ImageTk.PhotoImage(Image.open('images/output_on.png').resize((50,50)))
AND = ImageTk.PhotoImage(Image.open('images/and.png').resize((50,50)))
XOR = ImageTk.PhotoImage(Image.open('images/xor.png').resize((50,50)))
NOT = ImageTk.PhotoImage(Image.open('images/not.png').resize((50,50)))
OR = ImageTk.PhotoImage(Image.open('images/or.png').resize((50,50)))

canvas = tk.Canvas(root, width=8192, height=8192, bg='white')
canvas.place(relx=0, rely=0, relwidth=1, relheight=1, anchor=tk.NW)
root.tk.call('lower', str(canvas))

print('tklogicsim')

def render(circuit: Circuit):
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
        loaded_wires.append(canvas.create_line(xy_input_a[0]+50,xy_input_a[1]+25,xy_output_b[0]+50,xy_output_b[1]+25, width=2))
    print('Render End')

    return (loaded_blocks, loaded_wires)

main_circuit = Circuit([['Input',35,35,[False]], ['NOT',135,35,[]], ['Output',235,35,[False]]], [[0,1], [1,2]])
tk_rendered = render(main_circuit)

def toggle_input_or_output(idx:int, circuit:Circuit):
    global tk_rendered
    if circuit.items[idx][3][0] == True:
        circuit.items[idx][3][0] = False
    else:
        circuit.items[idx][3][0] = True
    
    for i in tk_rendered[0]:
        i.destroy()
    
    canvas.delete('all')
    tk_rendered = render(main_circuit)
    print(circuit.items, circuit.wires)

root.mainloop()