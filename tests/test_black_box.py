"""
Black Box Testing Suite for Bus Reservation System (STQA Lab C2).

Techniques Demonstrated:
1. Equivalence Class Partitioning (ECP)
2. Boundary Value Analysis (BVA)
3. Decision Table Testing
4. State Transition Testing
5. Error Guessing & Edge Case Testing
"""

import pytest
from BusReservationSystem.bus_service import (
    book_ticket,
    search_bookings,
    cancel_booking,
    get_all_bookings,
    get_available_seats,
    get_booked_seats,
    ValidationError,
    SeatUnavailableError,
    DuplicateBookingError,
    BookingNotFoundError,
    DEFAULT_BUSES
)


# ============================================================================
# 1. EQUIVALENCE CLASS PARTITIONING (ECP)
# ============================================================================

class TestEquivalenceClassPartitioning:
    """
    Equivalence Classes for Booking Inputs:
    EC1 (Valid Name): Non-empty string, alphabetic or alphanumeric with spaces
    EC2 (Invalid Name): Empty string, whitespace only
    EC3 (Valid Bus): Registered bus identifier ('Bus 1', 'Bus 2')
    EC4 (Invalid Bus): Non-existent bus identifier ('Bus 99', 'Express')
    EC5 (Valid Seat): Unoccupied valid seat ID ('A1', 'A2', etc.)
    EC6 (Invalid Seat): Non-existent seat ID or already booked seat
    """

    @pytest.mark.parametrize("valid_name, bus, seat", [
        ("John Doe", "Bus 1", "A1"),
        ("Alice", "Bus 1", "A2"),
        ("Bob Smith", "Bus 2", "B1"),
        ("Ravi Kumar 007", "Bus 2", "B2"),
    ])
    def test_ecp_valid_booking_partitions(self, db_conn, valid_name, bus, seat):
        """TC_BB_001 to 004: Valid name, valid bus, valid available seat."""
        result = book_ticket(db_conn, valid_name, bus, seat)
        assert result["status"] == "SUCCESS", f"Expected SUCCESS for valid passenger '{valid_name}'"
        assert result["name"] == valid_name
        assert result["bus"] == bus
        assert result["seat"] == seat
        assert result["id"] > 0

    @pytest.mark.parametrize("invalid_name", [
        "",
        "   ",
        "\t\n",
        None
    ])
    def test_ecp_invalid_name_partitions(self, db_conn, invalid_name):
        """TC_BB_005: Booking with empty or whitespace-only name must be rejected."""
        with pytest.raises(ValidationError) as exc_info:
            book_ticket(db_conn, invalid_name, "Bus 1", "A1")
        assert "Passenger name cannot be empty" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_bus", [
        "Bus 99",
        "Volvo Luxury",
        "Bus 3",
        ""
    ])
    def test_ecp_invalid_bus_partitions(self, db_conn, invalid_bus):
        """TC_BB_006: Booking with unlisted bus name must be rejected."""
        with pytest.raises(ValidationError) as exc_info:
            book_ticket(db_conn, "Valid User", invalid_bus, "A1")
        assert "not recognized" in str(exc_info.value) or "cannot be empty" in str(exc_info.value)

    @pytest.mark.parametrize("invalid_seat", [
        "Z9",
        "A5",
        "X1",
        "No seats"
    ])
    def test_ecp_invalid_seat_partitions(self, db_conn, invalid_seat):
        """TC_BB_007: Booking with non-existent or invalid seat identifier."""
        with pytest.raises((ValidationError, SeatUnavailableError)):
            book_ticket(db_conn, "Valid User", "Bus 1", invalid_seat)


# ============================================================================
# 2. BOUNDARY VALUE ANALYSIS (BVA)
# ============================================================================

class TestBoundaryValueAnalysis:
    """
    BVA focuses on values at the extremes of input domains and capacity limits.
    Bus 1 has capacity = 4 (Seats: A1, A2, A3, A4).
    - Minimum capacity: 0 booked (All 4 available)
    - Boundary 1: Booking 1st seat (Transition from 0 to 1)
    - Boundary 2: Booking 3rd seat (1 seat remaining)
    - Boundary 3: Booking 4th seat (Bus becomes full, 0 seats remaining)
    - Boundary 4: Attempting to book 5th seat on full bus (Capacity exceeded)
    """

    def test_bva_bus_capacity_limits(self, db_conn):
        """TC_BB_008: Progressive booking up to full bus capacity and overflow."""
        # Initial Boundary: 4 seats available
        available = get_available_seats(db_conn, "Bus 1")
        assert len(available) == 4, "Initial available seats should equal total capacity 4"

        # Boundary: 1st seat booked
        r1 = book_ticket(db_conn, "Passenger 1", "Bus 1", "A1")
        assert r1["seat"] == "A1"
        assert len(get_available_seats(db_conn, "Bus 1")) == 3

        # Booking intermediate seats
        book_ticket(db_conn, "Passenger 2", "Bus 1", "A2")
        book_ticket(db_conn, "Passenger 3", "Bus 1", "A3")
        assert len(get_available_seats(db_conn, "Bus 1")) == 1

        # Upper Boundary: 4th seat booked (bus reaches maximum capacity)
        r4 = book_ticket(db_conn, "Passenger 4", "Bus 1", "A4")
        assert r4["seat"] == "A4"
        available_after_full = get_available_seats(db_conn, "Bus 1")
        assert len(available_after_full) == 0, "No seats should remain when full"

        # Boundary Exceeded: 5th booking attempted on full bus
        with pytest.raises(SeatUnavailableError):
            book_ticket(db_conn, "Passenger 5", "Bus 1", "No seats")

    @pytest.mark.parametrize("name_length, name", [
        (1, "A"),                       # Min boundary: single-char valid name
        (2, "Al"),                      # Min boundary + 1
        (50, "A" * 50),                 # Typical upper boundary string
    ])
    def test_bva_name_string_length(self, db_conn, name_length, name):
        """TC_BB_009: Passenger name boundary testing from 1 character to large strings."""
        result = book_ticket(db_conn, name, "Bus 2", f"B1")
        assert result["status"] == "SUCCESS"
        assert len(result["name"]) == name_length


# ============================================================================
# 3. DECISION TABLE TESTING
# ============================================================================

class TestDecisionTableTesting:
    """
    Decision Table: Booking Rules
    ---------------------------------------------------------------------------------
    Rule # | Name Valid? | Bus Valid? | Seat Available? | Duplicate? | Expected Result
    ---------------------------------------------------------------------------------
    R1     | Yes         | Yes        | Yes             | No         | Booking Confirmed
    R2     | No          | Yes        | Yes             | No         | ValidationError
    R3     | Yes         | No         | Yes             | No         | ValidationError
    R4     | Yes         | Yes        | No              | No         | SeatUnavailableError
    R5     | Yes         | Yes        | Yes             | Yes        | DuplicateBookingError
    ---------------------------------------------------------------------------------
    """

    def test_decision_rule_1_success(self, db_conn):
        """Rule 1: All valid conditions met -> Success."""
        res = book_ticket(db_conn, "David", "Bus 1", "A1")
        assert res["status"] == "SUCCESS"

    def test_decision_rule_2_invalid_name(self, db_conn):
        """Rule 2: Name invalid -> ValidationError."""
        with pytest.raises(ValidationError):
            book_ticket(db_conn, "", "Bus 1", "A1")

    def test_decision_rule_3_invalid_bus(self, db_conn):
        """Rule 3: Bus invalid -> ValidationError."""
        with pytest.raises(ValidationError):
            book_ticket(db_conn, "David", "Bus Unknown", "A1")

    def test_decision_rule_4_seat_unavailable(self, seeded_db):
        """Rule 4: Seat already booked -> SeatUnavailableError."""
        # Alice already booked A1 in seeded_db
        with pytest.raises(SeatUnavailableError):
            book_ticket(seeded_db, "David", "Bus 1", "A1")

    def test_decision_rule_5_duplicate_passenger(self, seeded_db):
        """Rule 5: Passenger already has a ticket on this bus -> DuplicateBookingError."""
        # Alice already booked on Bus 1 in seeded_db
        with pytest.raises(DuplicateBookingError):
            book_ticket(seeded_db, "Alice", "Bus 1", "A3")


# ============================================================================
# 4. STATE TRANSITION TESTING
# ============================================================================

class TestStateTransitionTesting:
    """
    State Transitions of a Seat:
    [Available] --(Book Seat)--> [Booked]
    [Booked]    --(Cancel)-----> [Available]
    [Booked]    --(Book Again)-> [Error / Rejected]
    """

    def test_seat_lifecycle_state_transitions(self, db_conn):
        """TC_BB_010: Complete lifecycle transitions for Seat A1 on Bus 1."""
        # State 1: Seat is initially Available
        initial_available = get_available_seats(db_conn, "Bus 1")
        assert "A1" in initial_available, "State 1: A1 should be available initially"

        # Transition 1 -> State 2: Book Seat -> Status: Booked
        booking = book_ticket(db_conn, "Emma Watson", "Bus 1", "A1")
        assert booking["status"] == "SUCCESS"
        assert "A1" not in get_available_seats(db_conn, "Bus 1")
        assert "A1" in get_booked_seats(db_conn, "Bus 1")

        # Attempt invalid transition from State 2: Booked -> Booked (Should fail)
        with pytest.raises(SeatUnavailableError):
            book_ticket(db_conn, "Other Person", "Bus 1", "A1")

        # Transition 2 -> State 1: Cancel Booking -> Status: Available again
        cancelled = cancel_booking(db_conn, "Emma Watson", "Bus 1", "A1")
        assert cancelled["status"] == "CANCELLED"
        assert "A1" in get_available_seats(db_conn, "Bus 1"), "A1 must return to Available state"
        assert "A1" not in get_booked_seats(db_conn, "Bus 1")

        # Transition 3 -> Re-booking freed seat
        rebooking = book_ticket(db_conn, "New Passenger", "Bus 1", "A1")
        assert rebooking["status"] == "SUCCESS"
        assert "A1" in get_booked_seats(db_conn, "Bus 1")


# ============================================================================
# 5. ERROR GUESSING & EDGE CASES
# ============================================================================

class TestErrorGuessing:
    """
    Error guessing based on common user faults, string edge cases, and search anomalies:
    - Whitespace trimming around passenger name ("  Alice  ")
    - Case-insensitivity in search ("ALICE", "alice", "Alice")
    - Case-insensitivity in bus name ("bus 1" vs "Bus 1")
    - Searching for non-existent record
    - Cancelling a non-existent booking
    """

    def test_whitespace_handling_in_booking(self, db_conn):
        """TC_BB_011: Leading/trailing whitespace should be stripped from passenger names."""
        result = book_ticket(db_conn, "   Robert Downey   ", "Bus 1", "A1")
        assert result["name"] == "Robert Downey"

    def test_case_insensitive_search(self, seeded_db):
        """TC_BB_012: Search should match regardless of uppercase/lowercase input."""
        # 'Alice' was booked in seeded_db
        res_upper = search_bookings(seeded_db, "ALICE")
        res_lower = search_bookings(seeded_db, "alice")
        res_mixed = search_bookings(seeded_db, "AlIcE")

        assert len(res_upper) == 1
        assert len(res_lower) == 1
        assert len(res_mixed) == 1
        assert res_upper[0]["name"] == "Alice"

    def test_search_by_bus_name(self, seeded_db):
        """TC_BB_013: Searching by bus name returns all passengers on that bus."""
        res_bus1 = search_bookings(seeded_db, "Bus 1")
        # Alice and Bob are on Bus 1
        assert len(res_bus1) == 2
        names = {r["name"] for r in res_bus1}
        assert names == {"Alice", "Bob"}

    def test_search_empty_or_non_existent(self, seeded_db):
        """TC_BB_014: Searching for non-existent record or blank string returns empty list."""
        assert search_bookings(seeded_db, "Ghost Rider") == []
        assert search_bookings(seeded_db, "") == []
        assert search_bookings(seeded_db, "   ") == []

    def test_cancellation_non_existent_booking(self, seeded_db):
        """TC_BB_015: Cancelling non-existent booking raises BookingNotFoundError."""
        with pytest.raises(BookingNotFoundError):
            cancel_booking(seeded_db, "NonExistentUser", "Bus 1")

    def test_view_all_bookings_integrity(self, seeded_db):
        """TC_BB_016: View all retrieves all active bookings in correct format."""
        all_bookings = get_all_bookings(seeded_db)
        assert len(all_bookings) == 3
        # Verify schema elements
        for b in all_bookings:
            assert "id" in b
            assert "name" in b
            assert "bus" in b
            assert "seat" in b
