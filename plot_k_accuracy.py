import knn
import os
import matplotlib.pyplot as plt

def find_filenames():
    filename = r"C:\Users\jtpta\OneDrive\Pulpit\num_w_bfs\testData.txt"
    numbers = []
    with open(filename, 'r') as f:
        numbers = f.readlines()
    for i in range(len(numbers)):
        numbers[i] = numbers[i].strip()
    return numbers


def parse_dataset():
    trainingData = []
    trainingLabels = []
    filename = r"C:\Users\jtpta\OneDrive\Pulpit\num_w_bfs\testData.txt"
    numbers = find_filenames()
    for z in numbers:
        a, b, c, d, e, f, g, h, i, j = z.split(",")
        a, b, c, d, e, f, g, h, i, j = int(a), int(b), int(c), int(d), int(e), int(f), int(g), int(h), int(i), int(j)
        trainingData.append([a, b, c, d, e, f, g, h, i])
        trainingLabels.append(j)
    return trainingData, trainingLabels


trainingData, trainingLabels = parse_dataset()
is_k_correct = []



for i in range(1, 50):
    res = []
    u = 0
    percentage_per_k = 0
    for y in trainingData:
        final_results_per_k = knn.test_for_optimal_k(y, i)
        final_results_per_k = int(final_results_per_k)
        correct_results_per_k = int(trainingLabels[u])
        u += 1
        if final_results_per_k == correct_results_per_k:
            percentage_per_k +=1
    percentage_per_k = percentage_per_k / len(trainingData)

    percentage_per_k *= 100
    is_k_correct.append(int(round(percentage_per_k)))


x = []
for i in range(1, 50):
    x.append(i)

print(is_k_correct)
plt.plot(x, is_k_correct)

plt.xlabel('k')
plt.ylabel('accuracy (in percentages)')
plt.title('accuracies of values of k')
plt.show()
