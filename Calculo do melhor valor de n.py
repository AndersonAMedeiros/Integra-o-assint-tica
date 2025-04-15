import sympy as sp
from scipy.integrate import quad
import numpy as np

from sympy import init_printing
init_printing(use_latex=True)

def calcular_integral():
    print("Este código calcula a integral aproximada de x^m1 * e^(x^m2) dx")
    print("usando uma expansão em série com n termos, denominada de Método Assintótico de Ravi.")
    print("A fórmula utilizada é:")
    print(r"∫x^m1 * e^(x^m2) dx ≈ e^(x^m2) * (1/m2) * Σ [Produto(k=1 até n) (k - (m1+1)/m2)] * x^[(m1+1) - m2(n+1)]")

    # Solicita os valores
    m1 = float(input("\nDigite o valor de m1: "))
    m2 = float(input("Digite o valor de m2: "))
    x1 = float(input("Digite o valor de x1 (Limite Inferior): "))
    x2 = float(input("Digite o valor de x2 (Limite Superior): "))

    x = sp.symbols('x')
    n, k = sp.symbols('n k', integer=True)

    # Cálculo numérico usando scipy.integrate.quad
    def integrando(x):
        return (x**m1) * np.exp(x**m2)
    
    integral_numerica, erro = quad(integrando, x1, x2)
    print("\nResultado do Método Numérico (scipy.integrate.quad):")
    print("Integral numérica:", integral_numerica)
    print("Erro estimado:", erro)

    # Encontrar o melhor n
    melhor_n = 0
    menor_diferenca = float('inf')
    melhor_integral_assintotica = 0
    max_n = 50  # Número máximo de termos a testar

    for num_terms in range(1, max_n + 1):
        try:
            # Calcula a parte racional (série)
            term = (sp.Product((k - (m1 + 1)/m2), (k, 1, n)) * x**((m1 + 1) - m2*(n + 1)))/(m2)
            serie = sp.Sum(term, (n, 0, num_terms - 1)).doit()
            
            # Calcula a parte racional nos pontos
            serie_x1 = serie.subs(x, x1).evalf()
            serie_x2 = serie.subs(x, x2).evalf()
            
            # Calcula as exponenciais
            exp_x1 = sp.exp(x1**m2)
            exp_x2 = sp.exp(x2**m2)
            
            # Calcula a diferença
            integral_assintotica = (serie_x2 * exp_x2) - (serie_x1 * exp_x1)
            
            # Calcula a diferença absoluta em relação ao método numérico
            diferenca = abs(integral_assintotica - integral_numerica)
            
            # Verifica se esta é a menor diferença encontrada até agora
            if diferenca < menor_diferenca:
                menor_diferenca = diferenca
                melhor_n = num_terms
                melhor_integral_assintotica = integral_assintotica
        except:
            # Ignora erros (pode acontecer para alguns valores de n)
            pass

    print(f"\nMelhor número de termos (n): {melhor_n}")
    print("Menor diferença absoluta encontrada:", menor_diferenca)
    print("Integral aproximada pelo método de Ravi com n =", melhor_n, ":", melhor_integral_assintotica)

    # Mostra a fórmula para o melhor n
    term = (sp.Product((k - (m1 + 1)/m2), (k, 1, n)) * x**((m1 + 1) - m2*(n + 1)))/(m2)
    serie = sp.Sum(term, (n, 0, melhor_n - 1)).doit()
    print("\nResultado do Método Assintótico de Ravi para n =", melhor_n)
    print("e^(x^", m2, ") * [", sep="")
    sp.pprint(serie)
    print("]")

    # Comparação dos métodos
    if integral_numerica != 0:
        variacao_relativa = abs((melhor_integral_assintotica - integral_numerica)/integral_numerica) * 100
        print("\nComparação:")
        print(f"Variação relativa entre os métodos: {variacao_relativa:.10f}%")
    else:
        print("\nComparação:")
        print("A integral numérica é zero, não é possível calcular a variação relativa")

calcular_integral()
