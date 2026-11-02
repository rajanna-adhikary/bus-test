"""
Script to generate the STQA Lab C2 PowerPoint Presentation (.pptx)
Using python-pptx with a polished, modern design theme.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    PRIMARY = RGBColor(10, 37, 64)       # Deep Navy
    SECONDARY = RGBColor(0, 122, 255)   # Tech Blue
    ACCENT = RGBColor(230, 81, 0)       # Amber / Alert
    BG_LIGHT = RGBColor(248, 250, 252)  # Soft gray/white
    TEXT_DARK = RGBColor(30, 41, 59)    # Slate 800
    TEXT_MUTED = RGBColor(100, 116, 139)# Slate 500
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(241, 245, 249)   # Slate 100
    SUCCESS_BG = RGBColor(236, 253, 245)# Emerald light
    SUCCESS_TXT = RGBColor(6, 95, 70)

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        background = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
        )
        background.fill.solid()
        background.fill.fore_color.rgb = BG_LIGHT
        background.line.color.rgb = BG_LIGHT
        return background

    def add_header(slide, title_text, category="STQA LAB C2 • SOFTWARE TESTING & QUALITY ASSURANCE"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = SECONDARY

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = PRIMARY
        p_title.space_before = Pt(4)

    def add_card(slide, left, top, width, height, title, items, card_bg=CARD_BG, title_color=PRIMARY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = card_bg
        card.line.color.rgb = RGBColor(226, 232, 240)
        card.line.width = Pt(1)

        tx_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_head = tf.paragraphs[0]
        p_head.text = title
        p_head.font.size = Pt(14)
        p_head.font.bold = True
        p_head.font.color.rgb = title_color

        for item in items:
            p = tf.add_paragraph()
            p.text = f"•  {item}"
            p.font.size = Pt(11.5)
            p.font.color.rgb = TEXT_DARK
            p.space_before = Pt(6)

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = PRIMARY
    bg1.line.color.rgb = PRIMARY

    title_box = s1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(3.5))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "STQA LAB C2: SOFTWARE TESTING & QUALITY ASSURANCE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = SECONDARY

    p2 = tf1.add_paragraph()
    p2.text = "Comprehensive Test Plan & Automated Verification"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(10)

    p3 = tf1.add_paragraph()
    p3.text = "Bus Reservation System • Black Box • White Box • Pytest with Assert • IEEE 829"
    p3.font.size = Pt(18)
    p3.font.color.rgb = RGBColor(203, 213, 225)
    p3.space_before = Pt(12)

    meta_box = s1.shapes.add_textbox(Inches(1.0), Inches(5.8), Inches(11.3), Inches(1.0))
    tf_meta = meta_box.text_frame
    p_meta = tf_meta.paragraphs[0]
    p_meta.text = "STQA Lab Batch: C2  |  Technology: Python 3.13, Pytest 9.2, SQLite3, Tkinter  |  November 2026"
    p_meta.font.size = Pt(12)
    p_meta.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: EXECUTIVE SUMMARY
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Executive Summary & Testing Scope")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "🎯 System Under Test (SUT)", [
                 "Python Tkinter desktop bus booking application.",
                 "SQLite3 relational database backend.",
                 "Features: Search routes, inspect seats, book tickets, cancel reservations, view roster.",
                 "Configured for Bus 1 (A1-A4) and Bus 2 (B1-B4)."
             ])

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "🧪 Testing Methodologies", [
                 "IEEE 829-2008 Standard Test Plan compliance.",
                 "Black Box: ECP, BVA, Decision Tables, State Transitions, Error Guessing.",
                 "White Box: Statement (100%), Branch (100%), Condition, McCabe Cyclomatic Complexity.",
                 "Automated Pytest regression suite with isolated in-memory SQLite fixtures."
             ])

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "📊 Key Accomplishments", [
                 "68 Total Pytest automated test scenarios.",
                 "64 Passing tests verifying valid & edge cases.",
                 "4 XFAIL defect tests demonstrating subtle bugs.",
                 "Sub-second execution (~0.67s) with zero external state corruption.",
                 "Complete reproducible CLI/GUI demonstration suite."
             ])

    # =========================================================================
    # SLIDE 3: IEEE 829 TEST PLAN FRAMEWORK
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "IEEE 829-2008 Standard Test Plan Structure")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.4),
             "1. Core Identification & References", [
                 "Identifier: STQA-C2-BTRS-TP-2026-V1.0",
                 "References: IEEE Std 829-2008, ISO/IEC/IEEE 29119",
                 "Purpose: Verify booking integrity, seat concurrency, and input validation"
             ])

    add_card(s3, Inches(6.8), Inches(1.8), Inches(5.7), Inches(2.4),
             "2. Test Items & Architectural Scope", [
                 "Modules: DB Init, Inventory Engine, Booking Engine, Search Engine, Cancellation Engine, View All",
                 "Out of Scope: Payment gateways, distributed cloud sync"
             ])

    add_card(s3, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
             "3. Quality Gates & Pass/Fail Criteria", [
                 "Item Pass: 100% assertion adherence on functional rules",
                 "Item Fail: Unexpected exception, data corruption, duplicate seat assignment",
                 "Exit Gate: 100% pass on core regression suite, zero open Critical bugs"
             ])

    add_card(s3, Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.4),
             "4. Environment & Deliverables", [
                 "Environment: Python 3.13, Pytest 9.2, SQLite3 In-Memory",
                 "Deliverables: Test Plan, Black/White Box specs, Pytest test suites, PPTX, Draft Report, Interactive Demo"
             ])

    # =========================================================================
    # SLIDE 4: BLACK BOX TESTING STRATEGY
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Black Box Testing: Techniques & Equivalence Partitions")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "📦 Equivalence Class Partitioning", [
                 "Valid Name: Alphabetic or alphanumeric with spaces ('Alice', 'John Doe 2nd').",
                 "Invalid Name: Empty (''), whitespace only ('   '), None.",
                 "Valid Bus: 'Bus 1', 'Bus 2' (case-insensitive).",
                 "Invalid Bus: 'Bus 99', 'Volvo', empty string.",
                 "Valid Seat: Available seat IDs ('A1'..'A4', 'B1'..'B4').",
                 "Invalid Seat: 'Z9', 'No seats', already booked seat."
             ])

    add_card(s4, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "📏 Boundary Value Analysis (BVA)", [
                 "Capacity Boundary (Bus 1, Max=4):",
                 "• Initial: 4 available (0 booked).",
                 "• Progressive: 3, 2, 1 seats remaining.",
                 "• Upper Boundary: 4th seat booked (0 remaining).",
                 "• Beyond Boundary: 5th booking triggers SeatUnavailableError.",
                 "String Boundaries: Length 1 ('A') to Length 50+ tested."
             ])

    add_card(s4, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "🔄 State Transitions & Error Guessing", [
                 "Seat Lifecycle: [Available] -> [Booked] -> [Available].",
                 "Illegal State Transition: [Booked] -> [Booked] rejected.",
                 "Decision Table: 5-rule matrix testing Name x Bus x Seat x Duplicate.",
                 "Error Guessing: Whitespace stripping ('  Alice  '), mixed case ('ALICE'), non-existent cancel."
             ])

    # =========================================================================
    # SLIDE 5: BLACK BOX TEST EXECUTION MATRIX
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Black Box Test Execution Summary (Sample Cases)")

    # Table of test cases
    rows = 7
    cols = 5
    table_shape = s5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(1.4)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(3.2)
    table.columns[3].width = Inches(3.7)
    table.columns[4].width = Inches(1.2)

    headers = ["Test ID", "Component", "Input Vector", "Expected Outcome", "Status"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = WHITE

    data = [
        ("TC_BB_001", "Booking Engine", "Name: 'John Doe', Bus: 'Bus 1', Seat: 'A1'", "SUCCESS: Seat A1 reserved, ID assigned", "PASS"),
        ("TC_BB_005", "Input Validation", "Name: '   ' (Whitespace only), Bus 1", "ValidationError: 'Passenger name cannot be empty'", "PASS"),
        ("TC_BB_007", "Route Validation", "Name: 'Alice', Bus: 'Bus 99', Seat: 'A1'", "ValidationError: 'Bus not recognized'", "PASS"),
        ("TC_BB_009", "BVA Capacity", "Progressive booking of A1, A2, A3, A4", "Available seats decrement: 4 -> 3 -> 2 -> 1 -> 0", "PASS"),
        ("TC_BB_012", "Duplicate Check", "Alice books A1, then attempts A2 on Bus 1", "DuplicateBookingError: 'Already has a booking'", "PASS"),
        ("TC_BB_015", "Search Engine", "Query: 'ALICE' / 'alice' / 'AlIcE'", "Case-insensitive exact match returned", "PASS"),
    ]

    for r_idx, row in enumerate(data, start=1):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if r_idx % 2 == 0 else WHITE
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                if c_idx == 4:
                    p.font.bold = True
                    p.font.color.rgb = SUCCESS_TXT
                else:
                    p.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 6: WHITE BOX TESTING & ARCHITECTURE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "White Box Testing: Module Decomposition")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.4),
             "Module 1: Database Initialization (init_db)", [
                 "Control Flow: Sequential execution (N=3, E=2).",
                 "Cyclomatic Complexity: V(G) = E - N + 2P = 2 - 3 + 2 = 1.",
                 "Idempotency: Tested repeated CREATE TABLE IF NOT EXISTS execution."
             ])

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.7), Inches(2.4),
             "Module 2: Inventory Engine (get_booked / get_available)", [
                 "Predicates: Empty bus check, loop match, canonical bus validation.",
                 "Cyclomatic Complexity: get_booked V(G)=2; get_available V(G)=5.",
                 "Branches: Traversed both valid route & non-existent route paths."
             ])

    add_card(s6, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
             "Module 3 & 4: Booking & Search Engines", [
                 "book_ticket(): 7 predicate decisions -> V(G) = 8 Basis Paths.",
                 "search_bookings(): Evaluates compound condition LOWER(name)=? OR LOWER(bus)=?.",
                 "Multiple Condition Coverage evaluated with full truth table."
             ])

    add_card(s6, Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.4),
             "Module 5 & 6: Cancellation & Roster Roster", [
                 "cancel_booking(): Evaluates input presence, seat filter, row existence.",
                 "Cyclomatic Complexity: V(G) = 3 + 1 = 4 Basis Paths.",
                 "get_all_bookings(): Verifies complete audit query mapping."
             ])

    # =========================================================================
    # SLIDE 7: CONTROL FLOW GRAPH & CYCLOMATIC COMPLEXITY
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Control Flow Graph (CFG) & Basis Paths: book_ticket()")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(4.6), Inches(5.0),
             "📐 Cyclomatic Complexity Formulas", [
                 "Formula 1: V(G) = E - N + 2P",
                 "Formula 2: V(G) = P + 1 (Predicates + 1)",
                 "Formula 3: V(G) = Number of Enclosed Regions + 1",
                 "",
                 "Decision Predicates in book_ticket():",
                 "1. D1: if not clean_name",
                 "2. D2: if not bus_name",
                 "3. D3: if not canonical_bus",
                 "4. D4: if not seat or seat == 'No seats'",
                 "5. D5: if seat not in valid_seats",
                 "6. D6: if seat in booked",
                 "7. D7: if cursor.fetchone() (Duplicate check)",
                 "",
                 "Total Complexity: V(G) = 7 + 1 = 8 Basis Paths"
             ])

    add_card(s7, Inches(5.8), Inches(1.8), Inches(6.7), Inches(5.0),
             "🛤️ 8 Linearly Independent Basis Paths", [
                 "Path 1: Empty name -> raises ValidationError (Name empty).",
                 "Path 2: Valid name, empty bus -> raises ValidationError (Bus empty).",
                 "Path 3: Valid name, unlisted route -> raises ValidationError (Unrecognized).",
                 "Path 4: Valid name & bus, seat='No seats' -> raises SeatUnavailableError.",
                 "Path 5: Out of bounds seat ID ('Z99') -> raises ValidationError (Invalid seat).",
                 "Path 6: Seat already in booked list -> raises SeatUnavailableError.",
                 "Path 7: Passenger already booked on route -> raises DuplicateBookingError.",
                 "Path 8: All predicates pass -> INSERT record, commit DB, return SUCCESS.",
                 "",
                 "All 8 Basis Paths implemented in tests/test_white_box.py with 100% pass."
             ])

    # =========================================================================
    # SLIDE 8: COVERAGE METRICS & CONDITION COVERAGE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "White Box Coverage Metrics & Condition Truth Table")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "📈 Code Coverage Metrics Achieved", [
                 "Statement Coverage (C0): 100%",
                 "• Every executable line in bus_service.py traversed by test suite.",
                 "",
                 "Branch / Decision Coverage (C1): 100%",
                 "• All True and False outcomes of all 17 branching points exercised.",
                 "",
                 "Multiple Condition Coverage: 100%",
                 "• Evaluated compound boolean expressions independently.",
                 "",
                 "Basis Path Coverage: 100%",
                 "• All 8 basis paths of booking logic verified.",
                 "",
                 "Test Execution Speed:",
                 "• 68 tests executed in 0.67s via in-memory SQLite fixtures."
             ])

    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "🔍 Search Condition Truth Table", [
                 "Query SQL: WHERE LOWER(name)=? OR LOWER(bus)=?",
                 "Let C1 = (LOWER(name) == query), C2 = (LOWER(bus) == query)",
                 "",
                 "Case 1: C1 = True, C2 = False",
                 "-> Matches passenger name ('Alice') exclusively. Verified.",
                 "",
                 "Case 2: C1 = False, C2 = True",
                 "-> Matches route name ('Bus 2') exclusively. Verified.",
                 "",
                 "Case 3: C1 = False, C2 = False",
                 "-> Neither matches ('Spaceship') -> returns []. Verified.",
                 "",
                 "Branch: if not clean_query",
                 "-> Blank/whitespace search returns [] immediately. Verified."
             ])

    # =========================================================================
    # SLIDE 9: PYTEST AUTOMATION WITH ASSERT
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Pytest Automation & Native 'assert' Introspection")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "⚡ Why Pytest with assert?", [
                 "AST Bytecode Rewriting:",
                 "Pytest re-writes Python AST to inspect operands upon comparison failure, eliminating tedious self.assertEqual() boilerplate.",
                 "",
                 "Deep Collection Introspection:",
                 "Direct comparison of dictionaries, lists, and sets with color-coded diffs showing missing, extra, or mismatched elements.",
                 "",
                 "Custom Explanatory Failure Messages:",
                 "assert len(seats) == 4, f'Expected 4 seats, got {len(seats)}'",
                 "",
                 "Exception Inspection via pytest.raises:",
                 "with pytest.raises(ValidationError) as exc_info:",
                 "assert 'Passenger name cannot be empty' in str(exc_info.value)"
             ])

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "🛠️ Pytest Fixture Architecture (conftest.py)", [
                 "@pytest.fixture: db_conn",
                 "• Spawns an isolated SQLite in-memory database (:memory:).",
                 "• Zero filesystem residue, instant setup & teardown.",
                 "",
                 "@pytest.fixture: seeded_db",
                 "• Pre-loads Alice (Bus 1, A1), Bob (Bus 1, A2), Charlie (Bus 2, B1).",
                 "• Enables instant testing of search, duplicate, and cancel rules.",
                 "",
                 "@pytest.fixture: full_bus_db",
                 "• Pre-loads all 4 seats on Bus 1 to test capacity exhaustion.",
                 "",
                 "@pytest.mark.parametrize",
                 "• Runs multi-vector boundary and ECP datasets seamlessly."
             ])

    # =========================================================================
    # SLIDE 10: DEFECT DISCOVERY & FAILED TEST CASES
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Defect Discovery & Demonstrated Failed Test Cases")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.4),
             "🐛 Bug #1: Multi-Seat Booking Blocked (Logic Flaw)", [
                 "Defect: A passenger booking 2 seats on Bus 1 (e.g. for family) is blocked with 'Already booked'.",
                 "Root Cause: c.execute('WHERE LOWER(name)=? AND LOWER(bus)=?') ignores seat number.",
                 "Test: test_fail_bug1_multi_seat_booking_by_same_passenger (XFAIL)."
             ], card_bg=RGBColor(254, 242, 242), title_color=RGBColor(153, 27, 27))

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(2.4),
             "🐛 Bug #2: Capacity Assertion Mismatch (Pytest Diff)", [
                 "Defect: Incorrect analyst assumption that route holds 5 seats.",
                 "Pytest Output: assert 4 == 5 | where 4 = len(['A1', 'A2', 'A3', 'A4']).",
                 "Demonstrates Pytest's visual operand diagnosis without manual debuggers.",
                 "Test: test_fail_bug2_capacity_assertion_mismatch (XFAIL)."
             ], card_bg=RGBColor(254, 242, 242), title_color=RGBColor(153, 27, 27))

    add_card(s10, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
             "🐛 Bug #3: Ambiguous Cancellation Hazard", [
                 "Defect: Cancelling with name and bus without seat deletes whichever row SQLite returns first.",
                 "Risk: User intending to cancel seat A2 accidentally loses seat A1.",
                 "Test: test_fail_bug3_ambiguous_cancellation_by_name_only (XFAIL)."
             ], card_bg=RGBColor(254, 242, 242), title_color=RGBColor(153, 27, 27))

    add_card(s10, Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.4),
             "🐛 Bug #4: Substring / Wildcard Search Limitation", [
                 "Defect: Search query uses strict '=' comparison. Searching 'Ali' fails to return 'Alice'.",
                 "Impact: Poor user experience in desktop query workflows.",
                 "Test: test_fail_bug4_special_characters_sql_like_search (XFAIL)."
             ], card_bg=RGBColor(254, 242, 242), title_color=RGBColor(153, 27, 27))

    # =========================================================================
    # SLIDE 11: DEFECT RESOLUTION & REFACTORING RECOMMENDATIONS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Defect Resolution & System Improvements")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "🔧 Architectural & Schema Fixes", [
                 "Composite Unique Constraint:",
                 "Replace passenger-name constraint with UNIQUE(bus, seat) to allow multi-seat reservations per person while preventing double-booking.",
                 "",
                 "Seat-Specific Cancellation:",
                 "Update cancel interface to require Booking ID or Seat identifier, preventing ambiguous deletions.",
                 "",
                 "Pattern-Matching Search:",
                 "Upgrade query to: WHERE LOWER(name) LIKE ? OR LOWER(bus) LIKE ? with query wildcard parameter '%query%'.",
                 "",
                 "Layered Architecture Decoupling:",
                 "Decoupled bus_service.py engine from Tkinter UI, enabling 100% headless testability."
             ])

    add_card(s11, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "🛡️ Defensive Programming Enhancements", [
                 "Parameterized Prepared Statements:",
                 "Guaranteed immunity against SQL injection via parameterized tuples (?, ?).",
                 "",
                 "Whitespace Normalization:",
                 "name.strip() applied across all booking and search vectors.",
                 "",
                 "Explicit Custom Exceptions:",
                 "Created hierarchy: ValidationError, SeatUnavailableError, DuplicateBookingError, BookingNotFoundError.",
                 "",
                 "Automated Continuous Integration:",
                 "Pytest integrated into local workflow to prevent regression on future code changes."
             ])

    # =========================================================================
    # SLIDE 12: PROJECT DEMONSTRATION WORKFLOW
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Interactive Project Demonstration Workflow")

    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0),
             "🖥️ Interactive Demo Runner (run_demo.py)", [
                 "A complete terminal CLI & GUI launcher for evaluators:",
                 "",
                 "[1] Run All Passing Pytest Tests (Verbose)",
                 "Executes 64 tests in 0.67s across Black Box, White Box, and Assert suites.",
                 "",
                 "[2] Run Demonstrated Failed Test Cases",
                 "Runs defect cases with --runxfail showing colorized assertion diffs and bug tracebacks.",
                 "",
                 "[3] View White Box Cyclomatic Complexity & CFG",
                 "Displays mathematical complexity and basis path derivations.",
                 "",
                 "[4] View Black Box Test Cases Matrix",
                 "Displays full tabular verification results.",
                 "",
                 "[5] Launch Desktop GUI Application",
                 "Opens Tkinter app with pre-seeded sample data."
             ])

    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "▶️ One-Click Execution Commands", [
                 "Run full test suite:",
                 "python -m pytest -v tests/",
                 "",
                 "Run defect failure demonstration:",
                 "python -m pytest tests/test_failures_demo.py --runxfail",
                 "",
                 "Run interactive demo runner:",
                 "python run_demo.py",
                 "",
                 "Windows batch shortcut:",
                 "run_demo.bat",
                 "",
                 "Launch GUI directly:",
                 "python BusReservationSystem/bus_reservation.py"
             ])

    # =========================================================================
    # SLIDE 13: CONCLUSION & DELIVERABLES
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Conclusion & Final Deliverables Summary")

    add_card(s13, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "📁 Documentation Deliverables", [
                 "1. IEEE 829 Test Plan (IEEE_829_Test_Plan.md)",
                 "2. Black Box Testing Specification (Black_Box_Testing.md)",
                 "3. White Box Testing & CFG Analysis (White_Box_Testing.md)",
                 "4. STQA Lab C2 Final Draft Report (STQA_Lab_C2_Report.md)"
             ])

    add_card(s13, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "🧪 Testing & Code Deliverables", [
                 "1. Modular Service Engine (bus_service.py)",
                 "2. Pytest Conftest Fixtures (conftest.py)",
                 "3. Black Box Suite (test_black_box.py)",
                 "4. White Box Suite (test_white_box.py)",
                 "5. Pytest Assert Demo (test_pytest_assert_demo.py)",
                 "6. Failed Test Cases Demo (test_failures_demo.py)"
             ])

    add_card(s13, Inches(8.8), Inches(1.8), Inches(3.7), Inches(5.0),
             "🎓 Key Learnings & Takeaways", [
                 "Decoupling UI from core data logic is vital for testability.",
                 "Boundary testing exposes capacity overflow bugs reliably.",
                 "McCabe Cyclomatic Complexity provides mathematical rigor to path coverage.",
                 "Pytest's assert introspection drastically accelerates defect triage."
             ])

    # Save presentation
    os.makedirs("presentation", exist_ok=True)
    out_path = os.path.join("presentation", "STQA_Lab_C2_Presentation.pptx")
    prs.save(out_path)
    print(f"Successfully generated PowerPoint presentation at {out_path}")

if __name__ == "__main__":
    create_presentation()
