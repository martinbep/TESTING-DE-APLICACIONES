"""
Tests automatizados de la calculadora.
Cubren los tres casos pedidos en la consigna: exitoso, error y borde.
"""

import pytest
from app.calculadora import sumar, dividir


def test_sumar_dos_numeros():
    # Caso exitoso
    assert sumar(2, 3) == 5


def test_dividir_por_cero():
    # Caso de error
    with pytest.raises(ValueError):
        dividir(10, 0)


def test_sumar_con_negativos():
    # Caso borde
    assert sumar(-5, 3) == -2
