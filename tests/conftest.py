"""
Pytest Fixtures for Bus Reservation System Testing (STQA Lab C2).
Provides isolated in-memory databases and pre-seeded environments.
"""

import sys
import os
import pytest
import sqlite3

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from BusReservationSystem.bus_service import init_db, book_ticket, DEFAULT_BUSES


@pytest.fixture
def db_conn():
    """
    Yields a fresh, isolated in-memory SQLite database connection
    with schema initialized. Automatically closes after test.
    """
    conn = init_db(":memory:")
    yield conn
    conn.close()


@pytest.fixture
def seeded_db():
    """
    Yields an in-memory database pre-seeded with known baseline data:
    - Alice on Bus 1, seat A1
    - Bob on Bus 1, seat A2
    - Charlie on Bus 2, seat B1
    """
    conn = init_db(":memory:")
    book_ticket(conn, "Alice", "Bus 1", "A1")
    book_ticket(conn, "Bob", "Bus 1", "A2")
    book_ticket(conn, "Charlie", "Bus 2", "B1")
    yield conn
    conn.close()


@pytest.fixture
def full_bus_db():
    """
    Yields a database where Bus 1 has all 4 seats booked (A1, A2, A3, A4).
    Useful for boundary condition and seat exhaustion testing.
    """
    conn = init_db(":memory:")
    passengers = [("User1", "A1"), ("User2", "A2"), ("User3", "A3"), ("User4", "A4")]
    for name, seat in passengers:
        book_ticket(conn, name, "Bus 1", seat)
    yield conn
    conn.close()
