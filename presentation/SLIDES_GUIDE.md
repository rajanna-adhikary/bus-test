# Presentation Slide Deck & Speaker Notes
## STQA Lab C2: Software Testing & Quality Assurance
**Topic:** Comprehensive Test Suite & IEEE 829 Validation for Bus Reservation System  
**Presentation File:** [`STQA_Lab_C2_Presentation.pptx`](file:///c:/Users/Rajanna%20Adhikary/STQA/bus-reservation-system/presentation/STQA_Lab_C2_Presentation.pptx)  

---

### Slide 1: Title Slide
- **Title:** STQA Lab C2: Software Testing & Quality Assurance
- **Subtitle:** Comprehensive Test Plan & Automated Verification
- **Details:** Bus Reservation System • Black Box • White Box • Pytest with Assert • IEEE 829
- **Speaker Notes:**
  > "Good morning/afternoon, evaluators and colleagues. Today, we present the comprehensive Software Testing and Quality Assurance verification for the Bus Reservation System project. Our testing adheres strictly to the IEEE 829-2008 standard and employs both black box and white box methodologies, backed by automated Pytest suites and defect discovery profiling."

---

### Slide 2: Executive Summary & Testing Scope
- **Key Cards:**
  1. *System Under Test (SUT):* Python desktop bus booking application with Tkinter GUI and SQLite3 database.
  2. *Testing Methodologies:* IEEE 829 standard, Equivalence Class Partitioning (ECP), Boundary Value Analysis (BVA), Decision Tables, 100% Statement/Branch White Box Coverage, Cyclomatic Complexity basis paths.
  3. *Key Metrics:* 68 automated Pytest test cases, 64 passing, 4 isolated defect failure demonstrations, sub-second execution (~0.67s).
- **Speaker Notes:**
  > "The Bus Reservation System manages route inventory for multiple buses with 4 seats each. Our objective was to establish an automated, repeatable quality assurance pipeline that guarantees database integrity, validates user inputs, and measures code coverage."

---

### Slide 3: IEEE 829-2008 Test Plan Structure
- **Key Cards:**
  1. *Identification & References:* Standard document `STQA-C2-BTRS-TP-2026-V1.0`.
  2. *Test Items:* 6 core modules decomposed for isolated verification.
  3. *Pass/Fail Criteria & Quality Gates:* Strict boolean assertions and 100% pass criteria on regression suite.
  4. *Environment & Deliverables:* Python 3.13, Pytest 9.2, in-memory SQLite fixtures, automated reporting.
- **Speaker Notes:**
  > "Following IEEE 829-2008, we structured an 18-section formal test plan. This ensures complete traceability from risk identification to test item decomposition, pass/fail thresholds, and delivery milestones."

---

### Slide 4: Black Box Testing Strategy
- **Key Cards:**
  1. *Equivalence Class Partitioning (ECP):* Dividing name, route, seat, and search query domains into valid and invalid classes.
  2. *Boundary Value Analysis (BVA):* Testing bus capacity boundaries ($N=0, 1, 2, 3, 4, 5$) and string length extremes.
  3. *Decision Tables & State Transitions:* Matrix verification of business logic and seat state lifecycle ([Available] $\to$ [Booked] $\to$ [Available]).
- **Speaker Notes:**
  > "Our black box testing does not look at the internal code. Instead, we use ECP to reduce test bloat, BVA to verify capacity limits, and Decision Tables to validate compound business rules such as duplicate prevention."

---

### Slide 5: Black Box Test Execution Matrix
- **Key Content:**
  - Tabular execution summary: `TC_BB_001` through `TC_BB_020`.
  - Sample test scenarios: valid bookings, empty name rejection, unrecognized bus rejection, boundary seat exhaustion, duplicate booking detection, case-insensitive search.
- **Speaker Notes:**
  > "Here is our execution summary table. Every single functional requirement has a corresponding test case with defined inputs, expected outputs, and actual outcomes. All 20 black box test cases pass with 100% compliance."

---

### Slide 6: White Box Testing: Architectural Decomposition
- **Key Cards:**
  1. *Module 1 (init_db):* Schema creation, idempotency, $V(G)=1$.
  2. *Module 2 (Inventory Engine):* Seat availability set arithmetic, $V(G)=2$ and $V(G)=5$.
  3. *Module 3 & 4 (Booking & Search):* 7 decision predicates in booking ($V(G)=8$), compound SQL conditions.
  4. *Module 5 & 6 (Cancellation & Roster):* Parameter checks, deletion verification, audit queries.
- **Speaker Notes:**
  > "Moving to white box testing, we decoupled the business engine from the GUI into `bus_service.py`. This allowed us to calculate McCabe's Cyclomatic Complexity for every function and establish basis path coverage."

---

### Slide 7: Control Flow Graph & Cyclomatic Complexity: `book_ticket()`
- **Key Cards:**
  1. *Complexity Formulas:* $V(G) = E - N + 2P$ and $V(G) = P + 1 = 7 + 1 = 8$.
  2. *8 Linearly Independent Basis Paths:* Empty name, empty bus, unrecognized bus, no seats selected, invalid seat ID, seat already booked, duplicate booking, and successful insertion.
- **Speaker Notes:**
  > "For `book_ticket()`, there are 7 decision nodes. By McCabe's theorem, $V(G) = P + 1 = 8$. This proves mathematically that exactly 8 linearly independent basis paths exist. Our white box test suite explicitly exercises all 8 paths."

---

### Slide 8: Coverage Metrics & Condition Truth Table
- **Key Cards:**
  1. *Code Coverage:* 100% Statement Coverage ($C_0$), 100% Branch Coverage ($C_1$), 100% Basis Path Coverage.
  2. *Search Condition Truth Table:* Full evaluation of `LOWER(name)=? OR LOWER(bus)=?` across all True/False combinations ($C_1 \land \neg C_2$, $\neg C_1 \land C_2$, $\neg C_1 \land \neg C_2$).
- **Speaker Notes:**
  > "We achieved 100% statement and branch coverage. Additionally, for the compound SQL OR condition in search, we validated the full truth table to ensure passengers and buses are matched appropriately without false positives."

---

### Slide 9: Pytest Automation & Native `assert` Introspection
- **Key Cards:**
  1. *AST Bytecode Rewriting:* Eliminates legacy `unittest` methods (`self.assertEqual`) in favor of plain Python `assert`.
  2. *Deep Collection Introspection:* Dictionaries, lists, and sets produce color-coded diffs on mismatch.
  3. *In-Memory Fixtures:* `@pytest.fixture` creates clean `:memory:` databases per test, enabling 68 tests to run in just 0.67 seconds.
- **Speaker Notes:**
  > "Pytest re-writes Python bytecode during test execution. When an `assert` fails, it introspects local variables and shows the exact operands. Combined with in-memory SQLite fixtures, our test suite is completely isolated and lightning fast."

---

### Slide 10: Defect Discovery & Demonstrated Failed Test Cases
- **Key Cards:**
  1. *Bug 1 (Logic Flaw):* Same passenger booking 2 seats on the same bus is blocked with 'Already booked'.
  2. *Bug 2 (Assertion Diff Demo):* Pytest operand mismatch display (`assert 4 == 5`).
  3. *Bug 3 (Data Hazard):* Cancelling by name without seat ID deletes arbitrary booking when duplicates exist.
  4. *Bug 4 (Search Limitation):* Strict string equality fails on substring queries like 'Ali' for 'Alice'.
- **Speaker Notes:**
  > "A robust QA suite must not just pass green tests; it must uncover real defects. We isolated 4 latent bugs in the original codebase, decorated them with `@pytest.mark.xfail`, and demonstrated their stack traces and assertion diffs."

---

### Slide 11: Defect Resolution & System Improvements
- **Key Cards:**
  1. *Architectural Fixes:* Replace passenger constraint with `UNIQUE(bus, seat)` composite constraint; require Seat ID on cancellation; use SQL `LIKE` wildcard matching.
  2. *Defensive Programming:* Parameterized queries for SQL injection prevention, custom exception hierarchy, whitespace normalization.
- **Speaker Notes:**
  > "To resolve these bugs, we recommended replacing the restrictive passenger-level constraint with a composite `UNIQUE(bus, seat)` constraint. This allows lead bookers to buy multiple tickets while preventing duplicate bookings on the same physical seat."

---

### Slide 12: Interactive Project Demonstration Workflow
- **Key Cards:**
  1. *CLI Demo Runner:* `python run_demo.py` provides an interactive menu for running passing tests, running failure demos, viewing matrices, or launching the GUI.
  2. *Batch Shortcut:* `run_demo.bat` for Windows one-click execution.
- **Speaker Notes:**
  > "To facilitate live evaluation during lab defense, we built an interactive runner `run_demo.py`. Evaluators can run the full suite, view CFG complexities, inspect failure reports, or launch the Tkinter GUI directly."

---

### Slide 13: Conclusion & Final Deliverables
- **Key Cards:**
  1. *Documentation:* IEEE 829 Test Plan, Black Box Spec, White Box Spec, Draft Report.
  2. *Code Artifacts:* `bus_service.py`, 4 Pytest suites, PPTX generator, interactive runner.
  3. *Takeaways:* Decoupled architecture, mathematical coverage verification, AST assert diagnostics.
- **Speaker Notes:**
  > "In conclusion, this project fulfills all STQA Lab C2 requirements with academic rigor and production-grade software testing standards. Thank you, and we welcome your questions."
