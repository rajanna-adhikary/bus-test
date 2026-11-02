"""
Failed Test Cases Demonstration Suite (STQA Lab C2).

This module contains test cases designed to FAIL, demonstrating:
1. Defect discovery in the Bus Reservation System logic.
2. How Pytest displays failed assertions with bytecode introspection, diffs, and stack traces.
3. Common software testing failure patterns:
   - Defect A: Inability for a passenger to book multiple seats on the same bus (Overly restrictive duplicate constraint).
   - Defect B: Ambiguous cancellation deleting wrong seat when name/bus is non-unique.
   - Defect C: Capacity assertion mismatch (Demonstrating Pytest equality diff).
   - Defect D: Case-sensitivity & whitespace anomaly in naive query logic.

NOTE: Tests are marked with `@pytest.mark.xfail` so the test suite can be run either:
- As expected failures: `pytest tests/test_failures_demo.py` (marked as XFAIL)
- Or in strict failure mode: `pytest tests/test_failures_demo.py --runxfail` (shows red FAILED reports)
"""

import pytest
from BusReservationSystem.bus_service import (
    book_ticket,
    search_bookings,
    cancel_booking,
    get_available_seats,
    get_all_bookings,
    DuplicateBookingError,
    BookingNotFoundError
)


class TestDemonstratedFailuresAndBugs:
    """
    Demonstrating real bugs found during STQA testing of the Bus Reservation System.
    """

    @pytest.mark.xfail(reason="BUG #1: System forbids same passenger booking multiple distinct seats on the same bus.", strict=False)
    def test_fail_bug1_multi_seat_booking_by_same_passenger(self, db_conn):
        """
        DEFECT 1 (Logic Flaw):
        A user 'John Doe' wants to book seat A1 and seat A2 for his travel companion.
        Expected Behavior: John Doe should be allowed to book two different seats (A1 and A2).
        Actual Behavior in current design: Attempting to book seat A2 raises DuplicateBookingError
        because the system checks `WHERE LOWER(name)=? AND LOWER(bus)=?` without considering the seat.
        """
        # First seat booking succeeds
        r1 = book_ticket(db_conn, "John Doe", "Bus 1", "A1")
        assert r1["seat"] == "A1"

        # Second seat booking should succeed in an ideal reservation system
        # In current system, this triggers DuplicateBookingError!
        r2 = book_ticket(db_conn, "John Doe", "Bus 1", "A2")
        assert r2["seat"] == "A2", "Passenger should be permitted to reserve seat A2 as well"

    @pytest.mark.xfail(reason="BUG #2: Over-capacity assertion failure demonstration.", strict=False)
    def test_fail_bug2_capacity_assertion_mismatch(self, db_conn):
        """
        DEMO TEST FAILURE (Intentional Assertion Diff):
        Demonstrates Pytest's AST failure reporting when an expected value doesn't match actual.
        Suppose an analyst incorrectly assumes Bus 1 has 5 seats instead of 4.
        """
        available = get_available_seats(db_conn, "Bus 1")
        # Pytest will clearly output: assert 4 == 5
        assert len(available) == 5, f"Expected 5 seats on Bus 1, but system configured with {len(available)}"

    @pytest.mark.xfail(reason="BUG #3: Ambiguous cancellation deletes arbitrary seat when passenger has multiple bookings.", strict=False)
    def test_fail_bug3_ambiguous_cancellation_by_name_only(self, db_conn):
        """
        DEFECT 3 (Data Integrity Issue):
        If database contains two bookings for 'Robert' (e.g. booked via external source or edge case),
        cancelling without specifying the seat deletes whichever row SQLite happens to return first.
        """
        # Insert two manual bookings under same name on same bus
        cursor = db_conn.cursor()
        cursor.execute("INSERT INTO bookings (name, bus, seat) VALUES ('Robert', 'Bus 1', 'A1')")
        cursor.execute("INSERT INTO bookings (name, bus, seat) VALUES ('Robert', 'Bus 1', 'A2')")
        db_conn.commit()

        # User wants to cancel ONLY seat A2, but cancel_ui() only takes name and bus!
        # Calling cancel without seat parameter deletes A1 instead of A2!
        cancel_booking(db_conn, "Robert", "Bus 1")

        remaining = search_bookings(db_conn, "Robert")
        # Asserting that A1 is still intact fails because A1 was prematurely deleted!
        assert any(b["seat"] == "A1" for b in remaining), "Seat A1 should not have been cancelled!"

    @pytest.mark.xfail(reason="BUG #4: Strict string match failure on un-sanitized special characters.", strict=False)
    def test_fail_bug4_special_characters_sql_like_search(self, db_conn):
        """
        DEFECT 4: Searching with wildcard characters like '%' or '_'
        Current code uses '=': `WHERE LOWER(name)=? OR LOWER(bus)=?`.
        A partial search for 'Ali' does not find 'Alice'.
        """
        book_ticket(db_conn, "Alice", "Bus 1", "A1")
        # In a user-friendly system, searching for prefix 'Ali' should match 'Alice'
        results = search_bookings(db_conn, "Ali")
        assert len(results) > 0, "Partial search for 'Ali' should return 'Alice'"
