import tkinter as tk
import class_tk
import copy
import add_data
import os

global stuff_all
stuff_all = []


def bas_main(vector):
    filename = r"C:\Users\jtpta\OneDrive\Pulpit\num_w_bfs\testData.txt"

    with open(filename, 'a+') as f:
        x = ','.join(map(str, vector))
        f.seek(0)
        lines = f.readlines()
        if not lines:
            f.write(f"{x}")
        else:
            f.write(f"\n{x}")


def process_drawing(drawn_array):
    global k
    usage_arr = copy.deepcopy(drawn_array)
    usage_arr2 = copy.deepcopy(drawn_array)

    vector = [0 for _ in range(10)]
    i = 0
    for _ in range(4):
        temp = copy.deepcopy(usage_arr)
        l, r = add_data.bfs(temp)
        vector[i], vector[i+1] = int(l), int(r)
        i = i+2       
        usage_arr = add_data.rotate(usage_arr)
    
    vector[8] = int(add_data.surround_bfs(usage_arr2))
    vector[9] = 9
    stuff_all.append(vector)
    bas_main(vector)




def main():
    root = tk.Tk()
    app = class_tk.DigitDrawer(root)
    root.mainloop()
    if class_tk.drawn_array_tk is not None:
        return class_tk.drawn_array_tk
    return None

if __name__ == "__main__":
    for i in range(5):
        result = main()
        if result is not None:
            process_drawing(result)