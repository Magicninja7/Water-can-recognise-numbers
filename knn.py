import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageTk
import numpy as np
from collections import Counter
import class_tk
import copy
import add_data

global k
k = 5


def test_for_optimal_k(vector, k):
    return prediction_func(vector, k)


def find_filenames():
    filename = r"C:\Users\jtpta\OneDrive\Pulpit\num_w_bfs\trainingData.txt"
    numbers = []
    with open(filename, 'r') as f:
        numbers = f.readlines()
    for i in range(len(numbers)):
        numbers[i] = numbers[i].strip()
    return numbers


def parse_dataset():
    trainingData = []
    trainingLabels = []
    filename = r"C:\Users\jtpta\OneDrive\Pulpit\num_w_bfs\trainingData.txt"
    numbers = find_filenames()
    for z in numbers:
        a, b, c, d, e, f, g, h, i, j = z.split(",")
        a, b, c, d, e, f, g, h, i, j = int(a), int(b), int(c), int(d), int(e), int(f), int(g), int(h), int(i), int(j)
        trainingData.append([a, b, c, d, e, f, g, h, i])
        trainingLabels.append(j)
    return trainingData, trainingLabels


def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((np.array(point1) - np.array(point2))**2))



def knn(training_data, training_labels, test_point, k):
    distances = []
    for i in range(len(training_data)):
        dist = euclidean_distance(test_point, training_data[i])
        distances.append((dist, training_labels[i]))
    distances.sort(key=lambda x: x[0])
    k_nearest_labels = [label for _, label in distances[:k]]
    return Counter(k_nearest_labels).most_common(1)[0][0]

def process_drawing(drawn_array):
    global k
    usage_arr = copy.deepcopy(drawn_array)
    usage_arr2 = copy.deepcopy(drawn_array)

    vector = [0 for _ in range(9)]
    i = 0
    for _ in range(4):
        temp = copy.deepcopy(usage_arr)
        l, r = add_data.bfs(temp)
        vector[i], vector[i+1] = int(l), int(r)
        i = i+2       
        usage_arr = add_data.rotate(usage_arr)
    
    vector[8] = int(add_data.surround_bfs(usage_arr2))

    return prediction_func(vector, k)


def prediction_func(vector, k):
    trainingData, trainingLabels = parse_dataset()
    prediction = knn(trainingData, trainingLabels, vector, k)
    return prediction


'''
def main():
    root = tk.Tk()
    app = class_tk.DigitDrawer(root)
    root.mainloop()
    if class_tk.drawn_array_tk is not None:
        return class_tk.drawn_array_tk
    return None

if __name__ == "__main__":
    result = main()
    if result is not None:
        process_drawing(result)
'''