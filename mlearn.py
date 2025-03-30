# Langkah 1: Input Data
# Data X dan Y dimasukkan dalam bentuk list
X = [x1, x2, x3, ..., xn]  # Ganti dengan data X yang sebenarnya
Y = [y1, y2, y3, ..., yn]  # Ganti dengan data Y yang sebenarnya

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