"""
Bus Reservation System - Core Business and Data Logic Service
Module for STQA Lab C2 Testing and System Operations.
"""

import sqlite3
from typing import List, Dict, Optional, Tuple

DEFAULT_BUSES = {
    "Bus 1": ["A1", "A2", "A3", "A4"],
    "Bus 2": ["B1", "B2", "B3", "B4"]
}

class BookingError(Exception):
    """Base exception for booking operations."""
    pass

class ValidationError(BookingError):
    """Raised when user input validation fails."""
    pass

class SeatUnavailableError(BookingError):
    """Raised when a selected seat is not available."""
    pass

class DuplicateBookingError(BookingError):
    """Raised when a passenger has already booked on the same bus."""
    pass

class BookingNotFoundError(BookingError):
    """Raised when cancellation or query targets non-existent booking."""
    pass


def init_db(db_path: str = "bus_reservation.db") -> sqlite3.Connection:
    """Initialize database connection and create bookings table if not exists."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bus TEXT NOT NULL,
            seat TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def get_booked_seats(conn: sqlite3.Connection, bus_name: str) -> List[str]:
    """Retrieve list of booked seat identifiers for a specific bus (case-insensitive)."""
    if not bus_name:
        return []
    cursor = conn.cursor()
    cursor.execute(
        "SELECT seat FROM bookings WHERE LOWER(bus)=?",
        (bus_name.strip().lower(),)
    )
    return [row["seat"] for row in cursor.fetchall()]


def get_available_seats(conn: sqlite3.Connection, bus_name: str, buses: Dict[str, List[str]] = None) -> List[str]:
    """Retrieve available seats for a given bus."""
    if buses is None:
        buses = DEFAULT_BUSES
    
    # Locate bus matching case-insensitively
    canonical_bus = None
    for b in buses:
        if b.lower() == bus_name.strip().lower():
            canonical_bus = b
            break
            
    if not canonical_bus:
        return []
        
    all_seats = buses[canonical_bus]
    booked = get_booked_seats(conn, canonical_bus)
    return [seat for seat in all_seats if seat not in booked]


def book_ticket(conn: sqlite3.Connection, name: str, bus_name: str, seat: str,
                buses: Dict[str, List[str]] = None) -> Dict:
    """
    Book a seat on a bus.
    
    Enforces business rules:
    - Name must be non-empty and stripped of leading/trailing spaces
    - Bus must exist in configured routes
    - Seat must be a valid seat for the given bus
    - Seat must not already be booked
    - Passenger cannot have duplicate booking on the same bus (system rule)
    """
    if buses is None:
        buses = DEFAULT_BUSES
        
    clean_name = name.strip() if name else ""
    if not clean_name:
        raise ValidationError("Passenger name cannot be empty.")
        
    if not bus_name:
        raise ValidationError("Bus selection cannot be empty.")
        
    canonical_bus = None
    for b in buses:
        if b.lower() == bus_name.strip().lower():
            canonical_bus = b
            break
            
    if not canonical_bus:
        raise ValidationError(f"Bus '{bus_name}' is not recognized.")
        
    if not seat or seat == "No seats":
        raise SeatUnavailableError("No seats available or invalid seat chosen.")
        
    valid_seats = buses[canonical_bus]
    if seat not in valid_seats:
        raise ValidationError(f"Seat '{seat}' is not valid for {canonical_bus}.")
        
    booked = get_booked_seats(conn, canonical_bus)
    if seat in booked:
        raise SeatUnavailableError(f"Seat '{seat}' on {canonical_bus} is already booked.")
        
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM bookings WHERE LOWER(name)=? AND LOWER(bus)=?",
        (clean_name.lower(), canonical_bus.lower())
    )
    if cursor.fetchone():
        raise DuplicateBookingError(f"Passenger '{clean_name}' already has a booking on {canonical_bus}.")
        
    cursor.execute(
        "INSERT INTO bookings (name, bus, seat) VALUES (?, ?, ?)",
        (clean_name, canonical_bus, seat)
    )
    conn.commit()
    booking_id = cursor.lastrowid
    
    return {
        "id": booking_id,
        "name": clean_name,
        "bus": canonical_bus,
        "seat": seat,
        "status": "SUCCESS"
    }


def search_bookings(conn: sqlite3.Connection, query: str) -> List[Dict]:
    """Search bookings matching either passenger name or bus name (case-insensitive)."""
    clean_query = query.strip().lower() if query else ""
    if not clean_query:
        return []
        
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, bus, seat FROM bookings WHERE LOWER(name)=? OR LOWER(bus)=?",
        (clean_query, clean_query)
    )
    rows = cursor.fetchall()
    return [{"id": r["id"], "name": r["name"], "bus": r["bus"], "seat": r["seat"]} for r in rows]


def cancel_booking(conn: sqlite3.Connection, name: str, bus_name: str, seat: Optional[str] = None) -> Dict:
    """
    Cancel an existing booking by name and bus (and optionally specific seat).
    """
    clean_name = name.strip().lower() if name else ""
    clean_bus = bus_name.strip().lower() if bus_name else ""
    
    if not clean_name or not clean_bus:
        raise ValidationError("Both Name and Bus are required for cancellation.")
        
    cursor = conn.cursor()
    if seat:
        cursor.execute(
            "SELECT id, name, bus, seat FROM bookings WHERE LOWER(name)=? AND LOWER(bus)=? AND seat=?",
            (clean_name, clean_bus, seat)
        )
    else:
        cursor.execute(
            "SELECT id, name, bus, seat FROM bookings WHERE LOWER(name)=? AND LOWER(bus)=?",
            (clean_name, clean_bus)
        )
        
    row = cursor.fetchone()
    if not row:
        raise BookingNotFoundError(f"No booking found for '{name}' on '{bus_name}'.")
        
    booking_id = row["id"]
    cancelled_details = {
        "id": row["id"],
        "name": row["name"],
        "bus": row["bus"],
        "seat": row["seat"],
        "status": "CANCELLED"
    }
    
    cursor.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
    conn.commit()
    return cancelled_details


def get_all_bookings(conn: sqlite3.Connection) -> List[Dict]:
    """Retrieve all confirmed bookings in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, bus, seat FROM bookings ORDER BY id ASC")
    rows = cursor.fetchall()
    return [{"id": r["id"], "name": r["name"], "bus": r["bus"], "seat": r["seat"]} for r in rows]
