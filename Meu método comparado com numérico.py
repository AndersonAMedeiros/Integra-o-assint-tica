import sympy as sp
from scipy.integrate import quad
import numpy as np

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
    num_terms = int(input("Digite o número de termos para a série (recomendado 5-15): "))

    x = sp.symbols('x')
    n, k = sp.symbols('n k', integer=True)

    # Calcula a parte racional (série)
    term = (sp.Product((k - (m1 + 1)/m2), (k, 1, n)) * x**((m1 + 1) - m2*(n + 1)))/(m2)
    serie = sp.Sum(term, (n, 0, num_terms - 1)).doit()
    
    # Mostra a fórmula
    print("\nResultado 1 do Método Assintótico de Ravi")
    print("e^(x^", m2, ") * [", sep="")
    sp.pprint(serie)
    print("]")

    try:
        # Calcula a parte racional nos pontos
        serie_x1 = serie.subs(x, x1).evalf()
        serie_x2 = serie.subs(x, x2).evalf()
        
        # Calcula as exponenciais
        exp_x1 = sp.exp(x1**m2)
        exp_x2 = sp.exp(x2**m2)
        
        print(f"\nPara x1 = {x1}:")
        print("Parte racional:", serie_x1)
        print("e^(x1^m2) =", exp_x1)
        print("Valor total:", serie_x1 * exp_x1)
        
        print(f"\nPara x2 = {x2}:")
        print("Parte racional:", serie_x2)
        print("e^(x2^m2) =", exp_x2)
        print("Valor total:", serie_x2 * exp_x2)
        
        # Calcula a diferença
        integral_assintotica = (serie_x2 * exp_x2) - (serie_x1 * exp_x1)
        print("\nDiferença (integral definida aproximada pelo método assintótico de Ravi):", integral_assintotica)
        
        # Cálculo numérico usando scipy.integrate.quad
        def integrando(x):
            return (x**m1) * np.exp(x**m2)
        
        integral_numerica, erro = quad(integrando, x1, x2)
        
        print("\nResultado 2 - Método Numérico (scipy.integrate.quad):")
        print("Integral numérica:", integral_numerica)
        print("Erro estimado:", erro)
        
        # Comparação dos métodos
        if integral_numerica != 0:
            variacao_relativa = abs((integral_assintotica - integral_numerica)/integral_numerica) * 100
            print("\nComparação:")
            print(f"Variação relativa entre os métodos: {variacao_relativa:.10f}%")
        else:
            print("\nComparação:")
            print("A integral numérica é zero, não é possível calcular a variação relativa")
            
    except Exception as e:
        print("\nErro no cálculo:", e)
        print("Provavelmente devido a valores muito grandes")

calcular_integral()
