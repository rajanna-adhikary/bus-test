"""
Demonstration of Pytest with 'assert' Statements (STQA Lab C2).

This module demonstrates why Pytest's native `assert` statement is vastly
superior to legacy xUnit/unittest assertions (`self.assertEqual`, `self.assertTrue`).

Key Features Highlighted:
1. AST Introspection: Pytest re-writes Python bytecode to provide rich failure details
2. Dictionary, List, and Set introspection
3. Custom explanation messages in `assert condition, "explanation"`
4. Testing exceptions with `pytest.raises` and subsequent attribute assertions
5. Parametrized assertions with isolated fixtures
6. Sequential state verification
"""

import pytest
from BusReservationSystem.bus_service import (
    book_ticket,
    search_bookings,
    cancel_booking,
    get_available_seats,
    get_booked_seats,
    ValidationError,
    SeatUnavailableError
)


class TestPytestAssertDemonstration:
    """Pedagogical demonstration suite for Pytest assert capabilities."""

    def test_demo_1_basic_equality_and_membership_assert(self, db_conn):
        """
        DEMO 1: Native equality and membership assertions.
        Notice we do not use self.assertEqual() or self.assertIn().
        Plain Python operators == and `in` give rich diffs automatically.
        """
        result = book_ticket(db_conn, "Samantha", "Bus 1", "A1")

        # Pytest asserts
        assert result["name"] == "Samantha"
        assert result["seat"] == "A1"
        assert result["status"] == "SUCCESS"

        # Membership testing using native `in` keyword
        available = get_available_seats(db_conn, "Bus 1")
        assert "A1" not in available, "Booked seat A1 must NOT be in available seats"
        assert "A2" in available, "Unbooked seat A2 MUST be in available seats"

    def test_demo_2_dictionary_and_collection_diff(self, db_conn):
        """
        DEMO 2: Collection and Dictionary comparison introspection.
        When comparing dictionaries, pytest reports missing keys, extra keys,
        and differing values in a color-coded structural diff.
        """
        result = book_ticket(db_conn, "Raj", "Bus 2", "B1")

        expected_subset = {
            "name": "Raj",
            "bus": "Bus 2",
            "seat": "B1",
            "status": "SUCCESS"
        }

        # Compare dictionaries directly
        actual_subset = {k: result[k] for k in expected_subset}
        assert actual_subset == expected_subset, "Actual booking dictionary must match expected schema"

        # Compare sets directly with set operations
        all_bus2_seats = {"B1", "B2", "B3", "B4"}
        available_seats = set(get_available_seats(db_conn, "Bus 2"))
        booked_seats = set(get_booked_seats(db_conn, "Bus 2"))

        # Assert set partition: Available | Booked == All, Available & Booked == Empty
        assert available_seats.union(booked_seats) == all_bus2_seats
        assert available_seats.intersection(booked_seats) == set()

    def test_demo_3_custom_failure_messages(self, db_conn):
        """
        DEMO 3: Custom explanatory messages in assert.
        Format: `assert <expression>, <failure_message>`
        """
        bus_name = "Bus 1"
        initial_count = len(get_available_seats(db_conn, bus_name))

        book_ticket(db_conn, "Michael", bus_name, "A3")
        new_count = len(get_available_seats(db_conn, bus_name))

        # Informative assert message
        assert new_count == initial_count - 1, (
            f"Expected available seat count to decrement from {initial_count} "
            f"to {initial_count - 1}, but got {new_count}."
        )

    def test_demo_4_exception_assertion_with_pytest_raises(self, db_conn):
        """
        DEMO 4: Exception verification using `pytest.raises`.
        Captures the exception context and allows asserting on exception attributes
        and message text.
        """
        with pytest.raises(ValidationError) as exc_info:
            book_ticket(db_conn, "", "Bus 1", "A1")

        # Assert on the exception type and string representation
        assert exc_info.type is ValidationError
        assert "Passenger name cannot be empty" in str(exc_info.value)

    @pytest.mark.parametrize("passenger, bus, seat", [
        ("User A", "Bus 1", "A1"),
        ("User B", "Bus 1", "A2"),
        ("User C", "Bus 2", "B1"),
    ])
    def test_demo_5_parametrized_isolated_booking_assertions(self, db_conn, passenger, bus, seat):
        """
        DEMO 5: Parametrization with assert.
        Each test parameter runs with a freshly created in-memory db fixture.
        One seat booked out of 4 leaves exactly 3 available seats.
        """
        res = book_ticket(db_conn, passenger, bus, seat)
        assert res["status"] == "SUCCESS"
        assert res["seat"] == seat
        assert len(get_available_seats(db_conn, bus)) == 3

    def test_demo_6_sequential_progressive_state_verification(self, db_conn):
        """
        DEMO 6: Sequential verification of system state across operations.
        Asserts seat decrement step by step: 4 -> 3 -> 2 -> 1 -> 0
        """
        bus = "Bus 1"
        assert len(get_available_seats(db_conn, bus)) == 4

        book_ticket(db_conn, "P1", bus, "A1")
        assert len(get_available_seats(db_conn, bus)) == 3

        book_ticket(db_conn, "P2", bus, "A2")
        assert len(get_available_seats(db_conn, bus)) == 2

        book_ticket(db_conn, "P3", bus, "A3")
        assert len(get_available_seats(db_conn, bus)) == 1

        book_ticket(db_conn, "P4", bus, "A4")
        assert len(get_available_seats(db_conn, bus)) == 0
        assert get_available_seats(db_conn, bus) == []
