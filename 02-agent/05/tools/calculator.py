def add(a: int, b: int) -> dict:
    """2 つの数値を足し算します。"""
    return {"status": "success", "result": f"{a + b}"}


def subtract(a: int, b: int) -> dict:
    """2 つの数値を引き算します。"""
    return {"status": "success", "result": f"{a - b}"}


def multiply(a: int, b: int) -> dict:
    """2 つの数値を掛け算します。"""
    return {"status": "success", "result": f"{a * b}"}


def divide(a: int, b: int) -> dict:
    """数値 a を数値 b で割り算します。ゼロ除算の場合はエラーを返します。"""
    if b == 0:
        return {"status": "エラー: ゼロでは割り算できません"}
    return {"status": "success", "result": f"{a / b}"}
