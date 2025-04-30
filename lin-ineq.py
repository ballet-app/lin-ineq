import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import re

st.title("Wizualizacja dwóch nierówności liniowych")

# Funkcja pomocnicza do parsowania nierówności
import re

def improved_parse_inequality(ineq_str):
    ineq_str = ineq_str.replace(' ', '')

    # Szukamy operatora nierówności
    op_match = re.search(r'(<=|>=|<|>)', ineq_str)
    if not op_match:
        return None
    op = op_match.group(0)
    left, right = ineq_str.split(op, 1)

    # Inicjalizacja współczynników
    a = 0.0  # x
    b = 0.0  # y

    # Szukamy wyrazów z x i y w lewej stronie
    for var, coeff in [('x', 'a'), ('y', 'b')]:
        # znajdź wszystkie wyrazy z daną zmienną
        var_matches = re.findall(r'([+-]?\d*\.?\d*)'+var, left)
        if var_matches:
            val = sum([
                float(m) if m not in ['', '+', '-'] else float(m+'1') if m else 1.0
                for m in var_matches
            ])
            if var == 'x':
                a = val
            else:
                b = val

    # Stała po prawej stronie
    try:
        c = float(right)
    except ValueError:
        return None

    return a, b, op, c

# Pola tekstowe dla użytkownika
default_ineq1 = "x>=0"
default_ineq2 = "y>0"
ineq1 = st.text_input("Podaj pierwszą nierówność liniową (np. 2x+3y<=6, x>0):", value=default_ineq1)
ineq2 = st.text_input("Podaj drugą nierówność liniową (np. -x+y>=2, y<3):", value=default_ineq2)

parsed1 = improved_parse_inequality(ineq1)
parsed2 = improved_parse_inequality(ineq2)

if not parsed1 or not parsed2:
    st.error("Nieprawidłowy format nierówności. Użyj np. 2x+3y<=6, x>0, y<=3, x<5 itp.")
else:
    # Zakres wykresu
    x = np.linspace(-10, 10, 400)
    y = np.linspace(-10, 10, 400)
    X, Y = np.meshgrid(x, y)

    fig, ax = plt.subplots(figsize=(6, 6))

    # Funkcja do rysowania półpłaszczyzny i linii pomocniczej
    def plot_halfplane(a, b, op, c, color, label):
        # Określenie czy nierówność jest ostra
        is_strict = op in ['<', '>']
        if b != 0:
            # Wyznacz y z równania ax + by = c => y = (c - a*x)/b
            Y_line = (c - a * x) / b
            if op in ['>=', '>']:
                ax.fill_between(x, Y_line, 10, color=color, alpha=0.5, label=label)
            else:
                ax.fill_between(x, Y_line, -10, color=color, alpha=0.5, label=label)
            ax.plot(x, Y_line, color=color, linewidth=2, linestyle='--' if is_strict else '-')
        else:
            # x = c/a
            X_line = np.full_like(y, c / a)
            if op in ['>=', '>']:
                ax.fill_betweenx(y, c / a, 10, color=color, alpha=0.5, label=label)
            else:
                ax.fill_betweenx(y, -10, c / a, color=color, alpha=0.5, label=label)
            ax.plot(X_line, y, color=color, linewidth=2, linestyle='--' if is_strict else '-')

    plot_halfplane(*parsed1, color='yellow', label=ineq1)
    plot_halfplane(*parsed2, color='red', label=ineq2)

    # Osie
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.set_title('Wizualizacja układu nierówności')
    ax.legend(loc='upper right')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    st.pyplot(fig)
