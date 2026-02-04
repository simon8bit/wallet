import sqlite3
from typing import Optional, List, Dict, Any


class DBService:
    DB_NAME = "wallet.db"

    @classmethod
    def _connect(cls) -> sqlite3.Connection:
        """每次操作创建新连接（更安全）"""
        conn = sqlite3.connect(cls.DB_NAME)
        conn.row_factory = sqlite3.Row  # 查询返回 dict 风格
        return conn

    @classmethod
    def create_table(cls) -> None:
        """创建表"""
        create_sql = """
                     CREATE TABLE IF NOT EXISTS wallet
                     (
                         id          INTEGER PRIMARY KEY AUTOINCREMENT,
                         address     TEXT NOT NULL UNIQUE,
                         private_key TEXT NOT NULL UNIQUE,
                         remark      TEXT DEFAULT '',
                         created_at  TEXT DEFAULT (datetime('now', 'localtime'))
                     ); \
                     """
        conn = cls._connect()
        conn.execute(create_sql)
        conn.commit()
        conn.close()

    @classmethod
    def create_wallet(cls, address: str, private_key: str, remark: str = "") -> int:
        sql = """ INSERT INTO wallet (address, private_key, remark)VALUES (?, ?, ?); """
        conn = cls._connect()
        try:
            cur = conn.execute(sql, (address, private_key, remark))
            conn.commit()
            return cur.lastrowid
        finally:
            conn.close()

    @classmethod
    def get_wallet_by_address(cls, address: str) -> Optional[Dict[str, Any]]:
        """按地址查询钱包"""
        sql = "SELECT * FROM wallet WHERE address = ? LIMIT 1;"
        conn = cls._connect()
        try:
            cur = conn.execute(sql, (address,))
            row = cur.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    @classmethod
    def list_wallets(cls) -> List[Dict[str, Any]]:
        """查询全部钱包"""
        sql = "SELECT * FROM wallet ORDER BY id DESC;"
        conn = cls._connect()
        try:
            cur = conn.execute(sql)
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    @classmethod
    def update_remark(cls, wallet_id: int, remark: str) -> bool:
        """更新备注"""
        sql = "UPDATE wallet SET remark = ? WHERE id = ?;"
        conn = cls._connect()
        try:
            cur = conn.execute(sql, (remark, wallet_id))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    @classmethod
    def delete_wallet(cls, wallet_id: int) -> bool:
        """删除钱包"""
        sql = "DELETE FROM wallet WHERE id = ?;"
        conn = cls._connect()
        try:
            cur = conn.execute(sql, (wallet_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()
