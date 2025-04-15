import sympy as sp
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt

from sympy import init_printing, latex
init_printing(use_unicode=True)

def exibir_formula_como_imagem(expr, m2):
    expr_latex = latex(sp.exp(x**m2) * expr)
    plt.figure(figsize=(10, 2))
    plt.axis('off')
    plt.text(0.5, 0.5, f"$f(x) \\approx {expr_latex}$", fontsize=16, ha='center', va='center')
    plt.title("Método Assintótico de Ravi", fontsize=14)
    plt.tight_layout()
    plt.show()

def calcular_integral():
    print("Este código calcula a integral aproximada de x^m1 * e^(x^m2) dx")
    print("usando uma expansão em série com n termos, denominada de Método Assintótico de Ravi.")
    print("A fórmula utilizada é:")
    print(r"∫x^m1 * e^(x^m2) dx ≈ e^(x^m2) * (1/m2) * Σ [Produto(k=1 até n) (k - (m1+1)/m2)] * x^[(m1+1) - m2(n+1)]")

    # Entradas do usuário
    m1 = float(input("\nDigite o valor de m1: "))
    m2 = float(input("Digite o valor de m2: "))
    x1 = float(input("Digite o valor de x1 (Limite Inferior): "))
    x2 = float(input("Digite o valor de x2 (Limite Superior): "))

    global x  # usado na função de imagem
    x = sp.symbols('x')
    n, k = sp.symbols('n k', integer=True)

    # Método numérico de referência
    def integrando(x):
        return (x**m1) * np.exp(x**m2)
    
    integral_numerica, erro = quad(integrando, x1, x2)
    print("\nResultado do Método Numérico (scipy.integrate.quad):")
    print("Integral numérica:", integral_numerica)
    print("Erro estimado:", erro)

    # Busca pelo melhor n
    melhor_n = None
    menor_diferenca = float('inf')
    melhor_serie = None
    melhor_integral_assintotica = 0
    max_n = 50

    for num_terms in range(1, max_n + 1):
        try:
            termo = (sp.Product((k - (m1 + 1)/m2), (k, 1, n)) * x**((m1 + 1) - m2*(n + 1)))/(m2)
            serie = sp.Sum(termo, (n, 0, num_terms - 1)).doit()
            serie_x1 = serie.subs(x, x1).evalf()
            serie_x2 = serie.subs(x, x2).evalf()
            exp_x1 = sp.exp(x1**m2)
            exp_x2 = sp.exp(x2**m2)
            integral_assintotica = (serie_x2 * exp_x2) - (serie_x1 * exp_x1)
            diferenca = abs(integral_assintotica - integral_numerica)

            if diferenca < menor_diferenca:
                menor_diferenca = diferenca
                melhor_n = num_terms
                melhor_serie = serie
                melhor_integral_assintotica = integral_assintotica
        except:
            pass

    if melhor_n is None:
        print("\n⚠️ Não foi possível determinar o melhor n. Usando n = 5 como padrão.")
        melhor_n = 5
        termo = (sp.Product((k - (m1 + 1)/m2), (k, 1, n)) * x**((m1 + 1) - m2*(n + 1)))/(m2)
        melhor_serie = sp.Sum(termo, (n, 0, melhor_n - 1)).doit()
        serie_x1 = melhor_serie.subs(x, x1).evalf()
        serie_x2 = melhor_serie.subs(x, x2).evalf()
        exp_x1 = sp.exp(x1**m2)
        exp_x2 = sp.exp(x2**m2)
        melhor_integral_assintotica = (serie_x2 * exp_x2) - (serie_x1 * exp_x1)
        menor_diferenca = abs(melhor_integral_assintotica - integral_numerica)

    # Exibe detalhes do melhor n
    print(f"\nMelhor número de termos (n): {melhor_n}")
    print("Integral aproximada pelo método de Ravi:", melhor_integral_assintotica)
    print("Menor diferença absoluta:", menor_diferenca)

    # Mostra a expressão
    print("\nExpressão completa do Método Assintótico de Ravi para n =", melhor_n)
    print(f"f(x) ≈ e^(x^{m2}) * [racional(x)] onde:")
    sp.pprint(melhor_serie)

    # Mostrar imagem com fórmula renderizada
    exibir_formula_como_imagem(melhor_serie, m2)

    # Comparação
    if integral_numerica != 0:
        variacao_relativa = abs((melhor_integral_assintotica - integral_numerica)/integral_numerica) * 100
        print("\nComparação:")
        print(f"Variação relativa entre os métodos: {variacao_relativa:.10f}%")
    else:
        print("\nA integral numérica é zero, não é possível calcular a variação relativa.")

calcular_integral()


