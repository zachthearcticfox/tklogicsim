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

print('tklogicsim alpha (0.0.2-win64)')

def render(circuit: Circuit):
    ##########
    #Blocks#
    ##########
    loaded_blocks = []
    c = 0
    for i in circuit.items:
        match i[0]:
            case 'Input':
                loaded_blocks.append(tk.Button(root, image=INPUT_OFF))
            case 'Output':
                loaded_blocks.append(tk.Button(root, image=OUTPUT_OFF))
            case 'AND':
                loaded_blocks.append(tk.Button(root, image=AND))
            case 'XOR':
                loaded_blocks.append(tk.Button(root, image=XOR))
            case 'NOT':
                loaded_blocks.append(tk.Button(root, image=NOT))
            case 'OR':
                loaded_blocks.append(tk.Button(root, image=OR))

        loaded_blocks[c].place(x=i[1], y=i[2])
        c += 1
    c = 0

    #########
    #Wires#
    #########
    for i in circuit.wires:
        xy_input_a = (circuit.items[i[0]][1], circuit.items[i[0]][2])
        xy_output_b = (circuit.items[i[1]][1], circuit.items[i[1]][2])
        print(xy_input_a, xy_output_b, sep=', ')
        canvas.create_line(xy_input_a[0]+50,xy_input_a[1]+25,xy_output_b[0]+50,xy_output_b[1]+25, width=2)

    return loaded_blocks

main_circuit = Circuit([['Input',0,0,[False]], ['Input',0,75,[False]], ['AND',150,35,[]], ['Output',225,35,[False]]], [[0,2], [1,2], [2,3]])
render(main_circuit)

root.mainloop()