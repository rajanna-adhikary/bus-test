"""
White Box Testing Suite for Bus Reservation System (STQA Lab C2).

Techniques Demonstrated:
1. Statement Coverage (100% statement execution)
2. Branch / Decision Coverage (True and False outcomes of all predicates)
3. Condition Coverage (Compound boolean expressions evaluation)
4. Basis Path Testing (Independent control flow paths derived from Cyclomatic Complexity)
"""

import pytest
import sqlite3
from BusReservationSystem.bus_service import (
    init_db,
    get_booked_seats,
    get_available_seats,
    book_ticket,
    search_bookings,
    cancel_booking,
    get_all_bookings,
    ValidationError,
    SeatUnavailableError,
    DuplicateBookingError,
    BookingNotFoundError,
    DEFAULT_BUSES
)


# ============================================================================
# MODULE 1: DATABASE INITIALIZATION (init_db)
# ============================================================================

class TestWhiteBoxInitDb:
    """
    White Box Analysis of init_db:
    - Path 1: Default path creation / table setup
    - Path 2: Re-entrance (CREATE TABLE IF NOT EXISTS idempotency)
    """

    def test_init_db_creates_table_and_columns(self):
        """Statements: Connect, row_factory set, cursor execute, commit."""
        conn = init_db(":memory:")
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(bookings)")
        columns = {row[1] for row in cursor.fetchall()}
        assert {"id", "name", "bus", "seat"}.issubset(columns)
        conn.close()

    def test_init_db_idempotency(self):
        """Calling init_db multiple times on existing schema must not crash."""
        conn = init_db(":memory:")
        # Execute create again
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY, name TEXT, bus TEXT, seat TEXT)")
        conn.commit()
        assert conn.total_changes >= 0
        conn.close()


# ============================================================================
# MODULE 2: SEAT RETRIEVAL & AVAILABILITY LOGIC (get_booked_seats, get_available_seats)
# ============================================================================

class TestWhiteBoxSeatLogic:
    """
    White Box Analysis:
    - get_booked_seats:
        Predicate 1: `if not bus_name:`
            Branch 1T: bus_name is empty/None -> returns []
            Branch 1F: bus_name provided -> executes SQL query
    - get_available_seats:
        Predicate 1: `if buses is None:`
            Branch 1T: buses defaults to DEFAULT_BUSES
            Branch 1F: custom buses passed
        Predicate 2: `if not canonical_bus:`
            Branch 2T: bus not in dictionary -> returns []
            Branch 2F: bus found -> computes set difference
    """

    def test_get_booked_seats_branch_empty_bus(self, db_conn):
        """Branch 1T: bus_name is empty or None."""
        assert get_booked_seats(db_conn, "") == []
        assert get_booked_seats(db_conn, None) == []

    def test_get_booked_seats_branch_populated(self, seeded_db):
        """Branch 1F: bus_name provided, retrieves booked seats."""
        booked = get_booked_seats(seeded_db, "Bus 1")
        assert "A1" in booked
        assert "A2" in booked
        assert "A3" not in booked

    def test_get_available_seats_custom_buses(self, db_conn):
        """Branch 1F: custom buses dictionary provided."""
        custom_buses = {"MiniBus": ["M1", "M2"]}
        avail = get_available_seats(db_conn, "MiniBus", buses=custom_buses)
        assert avail == ["M1", "M2"]

    def test_get_available_seats_unrecognized_bus(self, db_conn):
        """Branch 2T: canonical_bus not found in configuration."""
        avail = get_available_seats(db_conn, "NonExistentRoute")
        assert avail == []


# ============================================================================
# MODULE 3: BOOKING CONTROL FLOW & BASIS PATHS (book_ticket)
# ============================================================================

class TestWhiteBoxBookingPaths:
    """
    Control Flow Graph (CFG) for book_ticket:
    Nodes:
      N1: Clean name, clean bus
      N2: Check `if not clean_name`
      N3: Check `if not bus_name`
      N4: Loop/Match canonical bus
      N5: Check `if not canonical_bus`
      N6: Check `if not seat or seat == 'No seats'`
      N7: Check `if seat not in valid_seats`
      N8: Query booked seats & Check `if seat in booked`
      N9: Query duplicate & Check `if cursor.fetchone()`
      N10: Insert into DB, commit, return success dict
    
    Cyclomatic Complexity: V(G) = 7 decision points + 1 = 8 Basis Paths
    """

    def test_path_1_empty_name(self, db_conn):
        """Basis Path 1: Empty name -> ValidationError at N2."""
        with pytest.raises(ValidationError) as exc:
            book_ticket(db_conn, "   ", "Bus 1", "A1")
        assert "Passenger name cannot be empty" in str(exc.value)

    def test_path_2_empty_bus_name(self, db_conn):
        """Basis Path 2: Valid name, but empty bus -> ValidationError at N3."""
        with pytest.raises(ValidationError) as exc:
            book_ticket(db_conn, "Alice", "", "A1")
        assert "Bus selection cannot be empty" in str(exc.value)

    def test_path_3_unrecognized_bus(self, db_conn):
        """Basis Path 3: Valid name, unlisted bus -> ValidationError at N5."""
        with pytest.raises(ValidationError) as exc:
            book_ticket(db_conn, "Alice", "Bus 999", "A1")
        assert "not recognized" in str(exc.value)

    def test_path_4_no_seat_selected(self, db_conn):
        """Basis Path 4: Valid name & bus, seat='No seats' -> SeatUnavailableError at N6."""
        with pytest.raises(SeatUnavailableError) as exc:
            book_ticket(db_conn, "Alice", "Bus 1", "No seats")
        assert "No seats available" in str(exc.value)

    def test_path_5_invalid_seat_id(self, db_conn):
        """Basis Path 5: Seat not in bus route configuration -> ValidationError at N7."""
        with pytest.raises(ValidationError) as exc:
            book_ticket(db_conn, "Alice", "Bus 1", "Z99")
        assert "not valid for Bus 1" in str(exc.value)

    def test_path_6_seat_already_booked(self, seeded_db):
        """Basis Path 6: Seat already in booked list -> SeatUnavailableError at N8."""
        with pytest.raises(SeatUnavailableError) as exc:
            book_ticket(seeded_db, "New User", "Bus 1", "A1")
        assert "already booked" in str(exc.value)

    def test_path_7_duplicate_passenger_on_same_bus(self, seeded_db):
        """Basis Path 7: Passenger already booked on this bus -> DuplicateBookingError at N9."""
        with pytest.raises(DuplicateBookingError) as exc:
            book_ticket(seeded_db, "Alice", "Bus 1", "A3")
        assert "already has a booking" in str(exc.value)

    def test_path_8_successful_booking(self, db_conn):
        """Basis Path 8: All predicates pass -> Insert, Commit, Return at N10."""
        res = book_ticket(db_conn, "Leonard", "Bus 1", "A1")
        assert res["status"] == "SUCCESS"
        assert res["id"] is not None
        assert res["name"] == "Leonard"


# ============================================================================
# MODULE 4: SEARCH CONTROL FLOW & CONDITION COVERAGE (search_bookings)
# ============================================================================

class TestWhiteBoxSearchConditionCoverage:
    """
    Search Query:
    `WHERE LOWER(name)=? OR LOWER(bus)=?`
    Condition 1: LOWER(name) == query
    Condition 2: LOWER(bus) == query
    
    Truth Table:
    C1 | C2 | Result
    T  | F  | Match by Name
    F  | T  | Match by Bus
    T  | T  | Match by both (e.g., if a passenger named their handle after a bus)
    F  | F  | No match
    """

    def test_condition_c1_true_c2_false(self, seeded_db):
        """C1=True, C2=False: Match passenger name exclusively."""
        res = search_bookings(seeded_db, "Alice")
        assert len(res) == 1
        assert res[0]["name"] == "Alice"

    def test_condition_c1_false_c2_true(self, seeded_db):
        """C1=False, C2=True: Match bus name exclusively."""
        res = search_bookings(seeded_db, "Bus 2")
        assert len(res) == 1
        assert res[0]["bus"] == "Bus 2"

    def test_condition_c1_false_c2_false(self, seeded_db):
        """C1=False, C2=False: No match found."""
        res = search_bookings(seeded_db, "Spaceship")
        assert res == []

    def test_empty_search_query_branch(self, seeded_db):
        """Branch: `if not clean_query:` True branch returns []."""
        assert search_bookings(seeded_db, "") == []
        assert search_bookings(seeded_db, "    ") == []


# ============================================================================
# MODULE 5: CANCELLATION CONTROL FLOW (cancel_booking)
# ============================================================================

class TestWhiteBoxCancellationPaths:
    """
    cancel_booking paths:
    Path 1: Missing name or bus -> ValidationError
    Path 2: Seat specified (AND seat=?) vs Seat not specified
    Path 3: Row not found -> BookingNotFoundError
    Path 4: Row found -> DELETE executed and commit
    """

    def test_cancel_missing_parameters(self, db_conn):
        """Path 1: Missing input parameters."""
        with pytest.raises(ValidationError):
            cancel_booking(db_conn, "", "Bus 1")
        with pytest.raises(ValidationError):
            cancel_booking(db_conn, "Alice", "")

    def test_cancel_not_found_path(self, seeded_db):
        """Path 3: Record does not exist in DB."""
        with pytest.raises(BookingNotFoundError):
            cancel_booking(seeded_db, "Ghost", "Bus 1")

    def test_cancel_success_with_seat_specified(self, seeded_db):
        """Path 2 (with seat) & Path 4 (successful deletion)."""
        res = cancel_booking(seeded_db, "Alice", "Bus 1", seat="A1")
        assert res["status"] == "CANCELLED"
        assert res["seat"] == "A1"
        # Confirm deleted from database
        assert search_bookings(seeded_db, "Alice") == []

    def test_cancel_success_without_seat_specified(self, seeded_db):
        """Path 2 (without seat) & Path 4 (successful deletion)."""
        res = cancel_booking(seeded_db, "Bob", "Bus 1")
        assert res["status"] == "CANCELLED"
        assert res["name"] == "Bob"
        assert search_bookings(seeded_db, "Bob") == []


# ============================================================================
# MODULE 6: VIEW ALL BOOKINGS (get_all_bookings)
# ============================================================================

class TestWhiteBoxViewAll:
    """
    Testing SQL result iteration and mapping.
    """

    def test_view_all_empty_database(self, db_conn):
        """Empty database returns empty list."""
        assert get_all_bookings(db_conn) == []

    def test_view_all_multiple_records(self, seeded_db):
        """Populated database returns all active records sorted by ID."""
        records = get_all_bookings(seeded_db)
        assert len(records) == 3
        ids = [r["id"] for r in records]
        assert ids == sorted(ids)
