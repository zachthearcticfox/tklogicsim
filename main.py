import tkinter as tk

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

print('tklogicsim alpha')

main_circuit = Circuit()

root.mainloop()