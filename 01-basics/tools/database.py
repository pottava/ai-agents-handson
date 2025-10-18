import psycopg2
import psycopg2.extras
from langchain_core.tools import tool
from libs.config import settings


@tool
def get_appointments(customer_name="", status=""):
    """
    ペットストアへの来店予約を顧客名（部分一致）およびステータスで検索

    Args:
        customer_name: 検索する顧客名。空白でも可。
        status: 絞り込むステータス ('scheduled', 'completed', 'canceled')。空白でも可。

    Returns:
        list[dict] | None: 検索結果のリスト（各行は辞書）。エラー時は None を返します
    """
    query = "SELECT * FROM visit_appointments"
    conditions = []
    params = []

    # customer_name が空白文字以外で指定されている場合
    if customer_name and customer_name.strip():
        conditions.append("customer_name ILIKE %s")
        params.append(f"%{customer_name.strip()}%")

    # status が空白文字以外で指定されている場合
    if status and status.strip():
        conditions.append("status = %s")
        params.append(status.strip())

    # 1 つ以上の条件がある場合、WHERE 句をクエリに追加
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY appointment_datetime DESC;"

    results = None
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        with conn, conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            print(f"実行クエリ: {cur.mogrify(query, tuple(params)).decode('utf-8')}")
            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            results = [dict(row) for row in rows]

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"クエリ実行中にエラーが発生しました: {error}")
    return results


def get_db_connection():
    """データベース接続を取得します"""
    try:
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            dbname=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"データベースに接続できませんでした: {e}")
        return None
