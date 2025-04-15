import sympy as sp
from scipy.integrate import quad
import numpy as np

from sympy import init_printing
init_printing(use_latex=True)

def calcular_comparacao():
    print("Este código calcula a variação relativa entre o método numérico e o método assintótico")
    print("para a integral de x^m1 * e^(x^m2) dx em intervalos fixos.")
    
    # Solicita os valores
    m1 = float(input("\nDigite o valor de m1: "))
    m2 = float(input("Digite o valor de m2: "))

    # Intervalos fixos
    intervalos = [(0.1, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
    
    x = sp.symbols('x')
    n, k = sp.symbols('n k', integer=True)
    max_n = 50  # Número máximo de termos a testar

    print("\n{:^10} | {:^25} | {:^10}".format("Intervalo", "Variação Relativa (%)", "Termos"))
    print("-" * 50)

    for x1, x2 in intervalos:
        # Cálculo numérico
        def integrando(x):
            return (x**m1) * np.exp(x**m2)
        
        try:
            integral_numerica, _ = quad(integrando, x1, x2)
        except:
            print("{:^10} | {:^25} | {:^10}".format(f"({x1},{x2})", "Divergente", "-"))
            continue

        # Encontrar o melhor n
        melhor_n = 0
        menor_diferenca = float('inf')
        melhor_integral_assintotica = 0

        for num_terms in range(1, max_n + 1):
            try:
                term = (sp.Product((k - (m1 + 1)/m2), (k, 1, n)) * x**((m1 + 1) - m2*(n + 1)))/(m2)
                serie = sp.Sum(term, (n, 0, num_terms - 1)).doit()
                
                serie_x1 = serie.subs(x, x1).evalf()
                serie_x2 = serie.subs(x, x2).evalf()
                
                exp_x1 = sp.exp(x1**m2)
                exp_x2 = sp.exp(x2**m2)
                
                integral_assintotica = (serie_x2 * exp_x2) - (serie_x1 * exp_x1)
                
                diferenca = abs(integral_assintotica - integral_numerica)
                
                if diferenca < menor_diferenca:
                    menor_diferenca = diferenca
                    melhor_n = num_terms
                    melhor_integral_assintotica = integral_assintotica
            except:
                continue

        # Calcula variação relativa
        if integral_numerica != 0:
            variacao_relativa = abs((melhor_integral_assintotica - integral_numerica)/integral_numerica) * 100
            print("{:^10} | {:^25.10f} | {:^10}".format(f"({x1},{x2})", variacao_relativa, melhor_n))
        else:
            print("{:^10} | {:^25} | {:^10}".format(f"({x1},{x2})", "Indeterminado (div/0)", melhor_n))

calcular_comparacao()
