import matplotlib.pyplot as plt
import numpy as np

# Zakres osi
x = np.linspace(-2, 4, 400)
y = np.linspace(-2, 4, 400)
X, Y = np.meshgrid(x, y)

fig, ax = plt.subplots(figsize=(6,6))

# Zielony obszar: x >= 0
ax.fill_betweenx(y, 0, 4, color='green', alpha=0.5, label='$x \\geq 0$')

# Czerwony obszar: y >= 0
ax.fill_between(x, 0, 4, color='red', alpha=0.5, label='$y \\geq 0$')

# Osie
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

# Ustawienia wykresu
ax.set_xlim(-2, 4)
ax.set_ylim(-2, 4)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_title('Interpretacja układu nierówności $x \\geq 0$, $y \\geq 0$')
ax.legend(loc='upper right')

plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()
