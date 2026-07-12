import os
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import main


class TestPostgresConnection(TestCase):
    @patch("main.psycopg.connect")
    def test_get_connection(self, mock_connect):
        config = main.PostgresConfig(
            host="db.local",
            port=5433,
            dbname="inventory_db",
            user="admin",
            password="secret",
            sslmode="require",
        )

        main.get_connection(config)

        mock_connect.assert_called_once_with(
            host="db.local",
            port=5433,
            dbname="inventory_db",
            user="admin",
            password="secret",
            sslmode="require",
        )

    def test_fetch_inventory_returns_rows(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {"id": 1, "make": "Toyota", "model": "Corolla", "year": 2020, "price": 15999.99}
        ]

        rows = main.fetch_inventory(mock_conn)

        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "SELECT id, make, model, year, price FROM inventory ORDER BY id"
        )
        self.assertEqual(rows, [
            {"id": 1, "make": "Toyota", "model": "Corolla", "year": 2020, "price": 15999.99}
        ])

    def test_insert_inventory_item_commits_and_returns_id(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [42]

        inserted_id = main.insert_inventory_item(
            mock_conn,
            make="Honda",
            model="Civic",
            year=2021,
            price=19999.99,
        )

        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO inventory (make, model, year, price) VALUES (%s, %s, %s, %s) RETURNING id",
            ("Honda", "Civic", 2021, 19999.99),
        )
        mock_conn.commit.assert_called_once()
        self.assertEqual(inserted_id, 42)
