import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageTk
import numpy as np
import copy
import class_tk


global drawn_array
global vector

def rotate(original_array):
    given = copy.deepcopy(original_array)

    i = 0
    y = 0

    copyOfArr = [[0 for _ in range(len(given))]for _ in range(len(given[0]))]
    max = len(copyOfArr[0])-1
    min = 0

    for _ in range(len(given[0])):
        i = 0
        for _ in range(len(given)):
            copyOfArr[y][max-i] = given[i][y]
            i+=1
        y+=1
    return copyOfArr

def crop_to_content_edges(matrix):
    rows_with_content = np.any(matrix == 1, axis=1)
    cols_with_content = np.any(matrix == 1, axis=0)

    #fucking edgecase which took wayy to much time to find:
    if not np.any(rows_with_content) or not np.any(cols_with_content):
        return matrix
    
    # find proper box
    top = np.argmax(rows_with_content)
    bottom = len(rows_with_content) - np.argmax(rows_with_content[::-1]) - 1
    left = np.argmax(cols_with_content)
    right = len(cols_with_content) - np.argmax(cols_with_content[::-1]) - 1
    
    # crop to found box
    cropped = matrix[top:bottom+1, left:right+1]
    
    return cropped

def bfs(test_arr):
    dir = [(1, 0), (0, -1), (0, 1)]
    visited = set()
    queue = []
    queue.append((0, 0))
    while queue:
        curr = queue.pop(0)
        test_arr[curr[0]][curr[1]] = 2
        for a, b in dir:
            if 0 <= curr[0] + a < int(len(test_arr)) and 0 <= curr[1] + b < int(len(test_arr[0])) and test_arr[curr[0]+a][curr[1]+b] == 0 and (curr[0]+a, curr[1]+b) not in visited:
                queue.append((curr[0]+a, curr[1]+b))
                visited.add((curr[0]+a, curr[1]+b))
            else:
                pass

    test_arr = np.array(test_arr)
    #slice into 2 halves
    height, width = test_arr.shape
    mid_col = width // 2
    l_half = test_arr[:, :mid_col]
    r_half = test_arr[:, mid_col:]
 
    crop_l_half = crop_to_content_edges(l_half)
    crop_r_half = crop_to_content_edges(r_half)

     #count 0s in each half
    l_num_zeros = (np.count_nonzero(crop_l_half == 0) / (len(crop_l_half) * len(crop_l_half[0]))) * 100
    r_num_zeros = (np.count_nonzero(crop_r_half == 0) / (len(crop_r_half) * len(crop_r_half[0]))) * 100
    return round(l_num_zeros), round(r_num_zeros)

def surround_bfs(test_arr):
    dir = [(1, 0), (-1, 0), (0, -1), (0, 1)]
    visited = set()
    queue = []
    queue.append((0, 0))
    while queue:
        curr = queue.pop(0)
        test_arr[curr[0]][curr[1]] = 2
        for a, b in dir:
            if 0 <= curr[0] + a < int(len(test_arr)) and 0 <= curr[1] + b < int(len(test_arr[0])) and test_arr[curr[0]+a][curr[1]+b] != 1 and (curr[0]+a, curr[1]+b) not in visited:
                queue.append((curr[0]+a, curr[1]+b))
                visited.add((curr[0]+a, curr[1]+b))
            else:
                pass
    volume = len(test_arr) * len(test_arr[0])
    unvisited = volume - len(visited)
    unvisited_perc = round((unvisited / volume) * 100)
    return unvisited_perc

def water():
    global drawn_array
    global vector
    usage_arr = copy.deepcopy(drawn_array)
    usage_arr2 = copy.deepcopy(drawn_array)

    vector = [0 for _ in range(10)]
    i = 0
    for _ in range(4):
        temp = copy.deepcopy(usage_arr)
        l, r = bfs(temp)
        vector[i], vector[i+1] = l, r
        i = i+2       
        usage_arr = rotate(usage_arr)
    
    vector[8] = surround_bfs(usage_arr2)
    decide = 9#int(input("what num?"))
    vector[9] = decide

    import os

    directory = r"C:\Users\jtpta\OneDrive\Pulpit\num_w_bfs\trainingData"
    files = os.listdir(directory)
    numbers = []
    for f in files:
        if f.endswith(".txt") and f[:-4].isdigit():
            numbers.append(int(f[:-4]))

    next_num = max(numbers) + 1 if numbers else 0 

    filename = os.path.join(directory, f"{next_num}.txt")

    with open(filename, 'w') as f:
        f.write(','.join(map(str, vector)))

def assign_arr(arr):
    global drawn_array 
    drawn_array = copy.deepcopy(arr)

'''
def main():
    root = tk.Tk()
    app = class_tk.DigitDrawer(root)
    root.mainloop()
    if class_tk.drawn_array_tk is not None:
        assign_arr(class_tk.drawn_array_tk)
        return class_tk.drawn_array_tk
    return None

if __name__ == "__main__":
    result = main()
    if result is not None:
        water()
'''