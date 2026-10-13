import pathlib

# ex 1: Parsing the System of Equation

def get_coef(s):
    if s == "" or s == "+":
        return 1.0
    if s == "-":
        return -1.0
    return float(s)

def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A = []
    B = []
    
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            line = line.replace(" ", "")
            
            left, right = line.split('=')
            B.append(float(right))
            
            idx_x = left.find('x')
            idx_y = left.find('y')
            idx_z = left.find('z')
            
            str_x = left[:idx_x]
            str_y = left[idx_x + 1 : idx_y]
            str_z = left[idx_y + 1 : idx_z]

            coef_x = get_coef(str_x)
            coef_y = get_coef(str_y)
            coef_z = get_coef(str_z)

            A.append([coef_x, coef_y, coef_z])
            
    return A, B

# ex 2:Matrix and Vector Operations

def determinant_3x3(matrix: list[list[float]]) -> float:
    return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) - 
            matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
            matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))

def trace(matrix: list[list[float]]) -> float:
    sum = 0
    for i in range(3):
        sum += matrix[i][i]
    return sum

def norm(vector: list[float]) -> float:
    sum = 0
    for i in range(3):
        sum += vector[i] ** 2
    return sum ** 0.5

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    aux = []
    for i in range(3):
        aux.append([])
        for j in range(3):
            aux[i].append(matrix[j][i])
    return aux

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    aux = []
    for i in range(3):
        aux.append(0)
        for j in range(3):
            aux[i] += matrix[i][j] * vector[j]
    return aux

# ex 3: Solving using Cramer’s Rule

def replace_column(matrix, column_index, new_column):
    aux = []
    for i in range(3):
        aux.append([])
        for j in range(3):
            if j == column_index:
                aux[i].append(new_column[i])
            else:
                aux[i].append(matrix[i][j])
    return aux

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det = determinant_3x3(matrix)
    if det == 0:
        raise ValueError("The system has no unique solution.")
    
    x_matrix = replace_column(matrix, 0, vector)
    y_matrix = replace_column(matrix, 1, vector)
    z_matrix = replace_column(matrix, 2, vector)
    
    x = determinant_3x3(x_matrix) / det
    y = determinant_3x3(y_matrix) / det
    z = determinant_3x3(z_matrix) / det
    
    return [x, y, z]

# ex 4: Solving using Inversion

def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    aux = []
    aux_row = 0
    for row in range(3):
        if row == i:
            continue
        aux.append([])
        for col in range(3):
            if col == j:
                continue
            aux[aux_row].append(matrix[row][col])
        aux_row += 1
    return aux

def determinant_2x2(matrix: list[list[float]]) -> float:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    aux = []
    for i in range(3):
        aux.append([])
        for j in range(3):
            minor_matrix = minor(matrix, i, j)
            aux[i].append(((-1) ** (i + j)) * determinant_2x2(minor_matrix))
    return aux

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    return transpose(cofactor(matrix))

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det = determinant_3x3(matrix)
    if det == 0:
        raise ValueError("The system has no unique solution.")
    
    adj = adjoint(matrix)
    for i in range(3):
        for j in range(3):
            adj[i][j] = adj[i][j] / det
    
    return multiply(adj, vector)

A, B = load_system(pathlib.Path("matrix.txt"))
print(f"{A=} {B=}")
print(f"{determinant_3x3(A)=}")
print(f"{trace(A)=}")
print(f"{norm(B)=}")
print(f"{transpose(A)=}")
print(f"{multiply(A, B)=}")
print(f"{solve_cramer(A, B)=}")
print(f"{solve(A, B)=}")
