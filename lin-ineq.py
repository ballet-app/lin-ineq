import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import re

st.title("Wizualizacja dwóch nierówności liniowych")

# Funkcja pomocnicza do parsowania nierówności
def parse_inequality(ineq_str):
    # Usuwamy spacje
    ineq_str = ineq_str.replace(' ', '')
    # Wzorzec: ax+by>=c, ax+by<=c, ax+by>c, ax+by<c
    pattern = r'([+-]?\d*\.?\d*)x([+-]\d*\.?\d*)y([<>]=?|>=|<=)([+-]?\d*\.?\d*)'
    match = re.match(pattern, ineq_str)
    if match:
        a = match.group(1)
        b = match.group(2)
        op = match.group(3)
        c = match.group(4)
        a = float(a) if a not in ['', '+', '-'] else float(a+'1') if a else 1.0
        b = float(b) if b not in ['', '+', '-'] else float(b+'1') if b else 1.0
        c = float(c)
        return a, b, op, c
    # Specjalne przypadki: x>=c, x>c, y<=c, y<c itd.
    pattern_x = r'x([<>]=?|>=|<=)([+-]?\d*\.?\d*)'
    pattern_y = r'y([<>]=?|>=|<=)([+-]?\d*\.?\d*)'
    match_x = re.match(pattern_x, ineq_str)
    match_y = re.match(pattern_y, ineq_str)
    if match_x:
        a, b, op, c = 1.0, 0.0, match_x.group(1), float(match_x.group(2))
        return a, b, op, c
    if match_y:
        a, b, op, c = 0.0, 1.0, match_y.group(1), float(match_y.group(2))
        return a, b, op, c
    return None

# Pola tekstowe dla użytkownika
default_ineq1 = "x>=0"
default_ineq2 = "y>0"
ineq1 = st.text_input("Podaj pierwszą nierówność liniową (np. 2x+3y<=6, x>0):", value=default_ineq1)
ineq2 = st.text_input("Podaj drugą nierówność liniową (np. -x+y>=2, y<3):", value=default_ineq2)

parsed1 = parse_inequality(ineq1)
parsed2 = parse_inequality(ineq2)

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
