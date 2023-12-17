# Ihre Matrix
matrix = [[1, 2, 3],
          [4, 5, 6]]

# Drehen Sie die Matrix um 90 Grad
rotated_matrix = [col[::-1] for col in zip(*matrix[::-1])]
rotated_matrix = zip(*matrix)

for row in rotated_matrix:
    print(row)