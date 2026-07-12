from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import psycopg


@dataclass
class PostgresConfig:
    host: str
    port: int
    dbname: str
    user: str
    password: str
    sslmode: str = "prefer"


def get_connection(config: PostgresConfig) -> psycopg.Connection:
    """Create and return a PostgreSQL connection using psycopg."""
    return psycopg.connect(
        host=config.host,
        port=config.port,
        dbname=config.dbname,
        user=config.user,
        password=config.password,
        sslmode=config.sslmode,
    )


def create_inventory_table(conn: psycopg.Connection) -> None:
    """Create a simple inventory table if it does not already exist."""
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS inventory (
                id SERIAL PRIMARY KEY,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                price NUMERIC(12, 2) NOT NULL
            )
            """
        )
    conn.commit()


def fetch_inventory(conn: psycopg.Connection) -> list[dict[str, Any]]:
    """Fetch all inventory rows from the database."""
    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
        cur.execute(
            "SELECT id, make, model, year, price FROM inventory ORDER BY id"
        )
        return [dict(row) for row in cur.fetchall()]


def insert_inventory_item(
    conn: psycopg.Connection,
    make: str,
    model: str,
    year: int,
    price: float,
) -> int:
    """Insert a new inventory item and return the generated row id."""
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO inventory (make, model, year, price) VALUES (%s, %s, %s, %s) RETURNING id",
            (make, model, year, price),
        )
        inserted_id = cur.fetchone()[0]
    conn.commit()
    return inserted_id


def main() -> None:
    """Example main entry point that connects to PostgreSQL."""
    config = PostgresConfig(
        host="localhost",
        port=5432,
        dbname="finecar",
        user="postgres",
        password="postgres",
    )

    conn = get_connection(config)
    create_inventory_table(conn)
    conn.close()


if __name__ == "__main__":
    main()
