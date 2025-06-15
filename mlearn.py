# Langkah 1: Input Data
# Data X: Jumlah kasus positif (Konfirmasi Positif)
X = [876, 8926, 7437, 9480, 3146, 5648, 3704, 5557, 5377, 5188, 3869, 4304, 
     4642, 7467, 2538, 8462, 3939, 6774, 8347, 8410, 4402, 5618, 3483, 3377, 
     4362, 2603, 5113, 2378, 2253, 8175, 3107]
# Data Y: Jumlah sembuh (Konfirmasi sembuh)
Y = Y = [120, 119, 88, 189, 39, 71, 44, 63, 50, 50, 38, 39, 56, 99, 41, 65, 
     56, 85, 87, 94, 59, 61, 44, 37, 51, 51, 65, 40, 39, 139, 33]


# Langkah 2: Hitung nilai-nilai yang diperlukan
n = len(X)                  # Jumlah data poin
sum_X = sum(X)              # Total nilai X
sum_Y = sum(Y)              # Total nilai Y
sum_XY = sum([x * y for x, y in zip(X, Y)])  # Total perkalian X dan Y
sum_X2 = sum([x**2 for x in X])              # Total kuadrat X

# Langkah 3: Hitung koefisien kemiringan (m)
numerator_m = n * sum_XY - sum_X * sum_Y
denominator_m = n * sum_X2 - sum_X**2
m = numerator_m / denominator_m

# Langkah 4: Hitung konstanta (c)
c = (sum_Y - m * sum_X) / n

# Langkah 5: Tampilkan persamaan regresi linear
print(f"Persamaan Regresi Linear: Y = {m:.6f}X + {c:.2f}")