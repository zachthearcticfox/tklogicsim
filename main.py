import tkinter as tk
from PIL import Image, ImageTk

class Circuit:
    def __init__(self, pre_items: list = [], pre_wires: list = []):
        if type(pre_items) != list or type(pre_wires) != list:
            raise Exception(f'Pre-items or Pre-wires are not a list')
        self.items = pre_items
        self.wires = pre_wires
    
    def add_wire(self, item1: int, item2: int):
        self.wires.append((item1, item2, []))
    
    def add_block(self, block: str, position: list):
        self.items.append((block, position, []))

root = tk.Tk()
root.geometry('768x512')
root.title('tk-logicsim')

INPUT_OFF = ImageTk.PhotoImage(Image.open('images/input_off.png').resize((74,74)))
INPUT_ON = ImageTk.PhotoImage(Image.open('images/input_on.png').resize((74,74)))
OUTPUT_OFF = ImageTk.PhotoImage(Image.open('images/output_off.png').resize((74,74)))
OUTPUT_ON = ImageTk.PhotoImage(Image.open('images/output_on.png').resize((74,74)))
AND = ImageTk.PhotoImage(Image.open('images/and.png').resize((74,74)))
XOR = ImageTk.PhotoImage(Image.open('images/xor.png').resize((74,74)))
NOT = ImageTk.PhotoImage(Image.open('images/not.png').resize((74,74)))
OR = ImageTk.PhotoImage(Image.open('images/or.png').resize((74,74)))

canvas = tk.Canvas(root, width=8192, height=8192, bg='white');canvas.pack(anchor=tk.NW)

print('tklogicsim alpha (0.0.1-win64)')

def render_circuit(circuit: Circuit):
    items = circuit.items
    wires = circuit.wires

    loaded = []

    for item in items:
        match item[0]:
            case 'Input': tmp = tk.Button(root, image=INPUT_OFF); loaded.append(tk.Button(root, image=INPUT_OFF))
            case 'Output': tmp = tk.Button(root, image=OUTPUT_OFF); loaded.append(tk.Button(root, image=INPUT_ON))
            case 'AND': tmp = tk.Button(root, image=AND); loaded.append(tk.Button(root, image=AND))
            case 'XOR': tmp = tk.Button(root, image=XOR); loaded.append(tk.Button(root, image=XOR))
            case 'NOT': tmp = tk.Button(root, image=NOT); loaded.append(tk.Button(root, image=NOT))
            case 'OR': tmp = tk.Button(root, image=OR); loaded.append(tk.Button(root, image=OR))
        tmp.place(x=item[1], y=item[2])
        del tmp

    for wire in wires:
        x0,y0,x1,y1 = items[wire[0]][1],items[wire[0]][2],items[wire[1]][1],items[wire[1]][2]
        canvas.create_line(x0,y0,x1,y1,width=5)

main_circuit = Circuit([('Input',0,0), ('Input',0,100), ('AND',200,50), ('Output',350,100)], [(0,2),(1,2),(2,3)])

render_circuit(main_circuit)

root.mainloop()