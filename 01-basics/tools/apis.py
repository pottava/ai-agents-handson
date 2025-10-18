from langchain_core.tools import tool
import requests


@tool
def get_users():
    """
    ペットストアの全ユーザーのリストを取得します

    Returns:
      list or None: ユーザー情報のリスト (list)。エラーが発生した場合は None を返します
    """
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        response.raise_for_status()  # HTTPエラーがあれば例外を発生
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")
        return None


@tool
def get_user_by_id(user_id):
    """
    指定された ID のペットストア ユーザー情報を取得します

    Args:
      user_id (int): 取得したいユーザーの ID

    Returns:
      dict or None: ユーザー情報 (dict)。エラーが発生した場合は None を返します
    """
    if not isinstance(user_id, int):
        raise ValueError("user_id は整数である必要があります")
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")
        return None
