import asyncpg

from ..libs.config import settings


async def get_appointments(customer_name: str = "", status: str = "") -> dict:
    """
    ペットストアへの来店予約を顧客名（部分一致）およびステータスで検索
    （この関数は並列実行に最適化されています）

    Args:
        customer_name: 検索する顧客名。空白でも可。
        status: 絞り込むステータス ('scheduled', 'completed', 'canceled')。空白でも可。

    Returns:
        検索結果のリスト（各行は辞書）
    """
    query = "SELECT * FROM visit_appointments"
    conditions = []
    params = []
    i = 1

    # customer_name が空白文字以外で指定されている場合
    if customer_name and customer_name.strip():
        conditions.append(f"customer_name ILIKE ${i}")
        params.append(f"%{customer_name.strip()}%")
        i += 1

    # status が空白文字以外で指定されている場合
    if status and status.strip():
        conditions.append(f"status = ${i}")
        params.append(status.strip())

    # 1 つ以上の条件がある場合、WHERE 句をクエリに追加
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY appointment_datetime DESC;"

    pool = await asyncpg.create_pool(get_dsn())
    records = []
    try:
        print(f"Executing Query: {query}, Params: {params}")
        async with pool.acquire() as conn:
            records = await conn.fetch(query, *params)
            records = [dict(r) for r in records]
        return {"status": "success", "appointments": records}

    except Exception as e:
        return {"status": f"エラーが発生しました: {e}"}
    finally:
        await pool.close()


def get_dsn() -> str:
    return f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
