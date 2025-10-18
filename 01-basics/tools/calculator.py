from langchain_core.tools import tool


@tool
def add(a: int, b: int) -> int:
    """2 つの数値を足し算します。"""
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """2 つの数値を引き算します。"""
    return a - b


@tool
def multiply(a: int, b: int) -> int:
    """2 つの数値を掛け算します。"""
    return a * b


@tool
def divide(a: int, b: int) -> float:
    """数値 a を数値 b で割り算します。ゼロ除算の場合はエラーを返します。"""
    if b == 0:
        return "エラー: ゼロでは割り算できません。"
    return a / b
