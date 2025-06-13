# filepath: h:\Meu Drive\Ciencia de Dados\Python\O tutorial do Python\6 - Módulos\fibo.py
def fib(n):
    """Print a Fibonacci series up to n."""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()