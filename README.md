# 🚑 AI-Based Emergency Ambulance Dispatch & Hospital Optimization System

An intelligent emergency response system that uses **A\* Search** to route ambulances optimally through a city road network and **Constraint Satisfaction Problem (CSP)** solving to assign the best available hospital — all visualized in a real-time Streamlit dashboard.

## Features

### Emergency Dispatch
- **Nearest Ambulance Selection** — Runs A\* search from every available ambulance to the emergency location and picks the one with the lowest travel cost
- **Optimal Hospital Assignment** — Uses CSP to filter hospitals by bed availability, ICU requirement, doctor count, capacity limit and road reachability, then picks the one with the lowest A* road cost (straight-line distance is only a tie-breaker)
- **Full Route Planning** — Computes two legs: ambulance → emergency, then emergency → hospital, with combined total cost
- **Pre-defined Scenarios** — Four ready-to-run emergency cases (heart attack, car accident, fall injury, stroke) for quick testing

### A\* Search Algorithm
- Classic f(n) = g(n) + h(n) implementation where h(n) is Euclidean distance (admissible heuristic)
- Tracks every node expansion and edge exploration for step-by-step visualization
- Includes a **Dijkstra baseline** (A\* without heuristic) shown in the dashboard for both route legs: costs must match, nodes expanded show the heuristic's savings
- Metrics: nodes expanded, path cost, execution time

### CSP Hospital Optimizer
- Five hard constraints applied in sequence with full domain reduction:
  - **C1** — Available beds > 0
  - **C2** — ICU available (only if required)
  - **C3** — Doctors available > 0
  - **C4** — Occupied beds < capacity limit (limit is below total beds in the sample data, so it is independent of C1)
  - **C5** — Hospital reachable by road from the emergency location
- Remaining hospitals are ordered by A* route cost (same effective weights as routing); Euclidean distance breaks ties
- If no hospital is feasible, the dashboard explains which constraint emptied the domain

### Hospital Management
- Live capacity dashboard with occupancy indicators (🟢 / 🟡 / 🔴)
- Update beds, doctors, and ICU availability per hospital in real time

### System Administration
- **Randomize traffic** — Assigns random traffic multipliers (1.0×–3.0×) to all roads
- **Reset traffic** — Clears all roads back to 1.0×
- **Manual road control** — Adjust traffic factor on individual roads via slider
- Color-coded road map: green (clear), orange (moderate), red (heavy)

### Visualizations
- City road network with hospitals, ambulances, and emergency location highlighted
- A\* exploration map (explored nodes + edges) vs. final optimal path side-by-side
- CSP domain reduction bar chart
- CSP backtracking flowchart with color-coded step statuses
- CSP constraints table
- CSP final assignment table (assigned / valid / rejected per hospital)

---

## Technologies Used

- Streamlit
- NetworkX
- Matplotlib
- NumPy
- Python 3.8+
- A\* Search
- Dijkstra's Algorithm
- Constraint Satisfaction Problem (CSP) with Backtracking + MRV heuristic

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "AI-Based Emergency Ambulance Dispatch & Hospital Optimization System"
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. Open your browser at `http://localhost:8501`

---

## AI-Enhanced Routing Features

### Fuzzy Logic — Traffic Congestion Estimation

**What it does:** Uses Mamdani-style fuzzy inference with centroid defuzzification to estimate a traffic congestion severity score (0–100) from the existing road `traffic_factor` data. This replaces the raw traffic multiplier with a fuzzy-derived cost factor for more nuanced congestion modeling.

**Inputs:**
| Input | Source | Range |
|-------|--------|-------|
| `traffic_factor` | Existing road data from CityGraph edges | 1.0–3.0 |
| `speed_ratio` | **Simulated** — derived as `1.0 / traffic_factor` | 0.0–1.0 |

> **Note:** `speed_ratio` is not from a real data source. The project does not measure actual vehicle speeds. It is derived from the traffic factor as a reasonable proxy.

**Membership Functions (all triangular):**

| Variable | Category | Triangle (a, b, c) |
|----------|----------|---------------------|
| Traffic Density | LOW | (0.5, 1.0, 1.8) |
| Traffic Density | MEDIUM | (1.2, 2.0, 2.8) |
| Traffic Density | HIGH | (2.2, 3.0, 3.5) |
| Speed Ratio | SLOW | (-0.3, 0.0, 0.5) |
| Speed Ratio | MODERATE | (0.2, 0.5, 0.8) |
| Speed Ratio | FAST | (0.5, 1.0, 1.3) |
| Congestion | LOW | (0, 10, 35) |
| Congestion | MEDIUM | (20, 45, 65) |
| Congestion | HIGH | (50, 70, 85) |
| Congestion | VERY_HIGH | (75, 90, 100) |

**Fuzzy Rules:**
1. IF traffic\_density is LOW → congestion is LOW
2. IF traffic\_density is MEDIUM → congestion is MEDIUM
3. IF traffic\_density is HIGH → congestion is HIGH
4. IF traffic\_density is HIGH AND speed is SLOW → congestion is VERY\_HIGH
5. IF traffic\_density is MEDIUM AND speed is SLOW → congestion is HIGH
6. IF traffic\_density is LOW AND speed is FAST → congestion is LOW

**Output:** Congestion score (0–100) → converted to cost factor (1.0–3.0).

---

### Bayesian Reasoning — Road Risk Estimation

**What it does:** Uses a small Bayesian Network with exact enumeration inference to estimate the probability that a road is blocked, given uncertain evidence (weather, accidents, traffic level).

**Bayesian Network Structure:**
```
Rain ──┐
       ├──→ Road_Blocked
Accident ─┤
           │
Traffic_Level ─┘
```

**Evidence Variables:**
| Variable | States | Source |
|----------|--------|--------|
| Rain | True / False | **Simulated** — toggled via UI checkbox |
| Accident | True / False | **Simulated** — toggled via UI checkbox |
| Traffic Level | low / medium / high | Derived from existing `traffic_factor` |

> **Note:** Rain and accident evidence are simulated inputs. The project has no real weather feed or accident reporting system.

**Conditional Probability Tables (manually specified, NOT trained):**

Prior probabilities:
- P(Rain) = 0.20
- P(Accident) = 0.05

P(Traffic\_Level | Rain):

| Rain | P(low) | P(medium) | P(high) |
|------|--------|-----------|---------|
| True | 0.15 | 0.35 | 0.50 |
| False | 0.50 | 0.35 | 0.15 |

P(Road\_Blocked | Rain, Accident, Traffic\_Level): see `algorithms/bayesian_reasoning.py` for full table.

**Output:** Posterior P(blocked | evidence) → converted to risk factor (≥ 1.0).

---

### How Both Models Affect Road Costs

The processing pipeline is:

```
Existing road data → Fuzzy Logic → Bayesian Reasoning → Effective Cost → A* Routing
```

**Cost Formula:**
```
effective_cost = base_distance × congestion_factor × risk_factor
```

Where:
- `base_distance` = Euclidean distance between nodes (unchanged)
- `congestion_factor` = fuzzy-derived (replaces raw `traffic_factor` to avoid double-counting)
- `risk_factor` = `1.0 + penalty_weight × P(blocked | evidence)`

When both features are **disabled**, the formula reduces to the original: `base_distance × traffic_factor`.

---

### How to Enable / Disable

1. Navigate to **⚙️ System Administration**
2. Scroll to **🧠 AI-Enhanced Routing**
3. Expand **⚙️ Fuzzy Logic & Bayesian Reasoning Settings**
4. Toggle checkboxes for each feature
5. When Bayesian is enabled, configure evidence (Rain, Accident) and Risk Penalty Weight
6. Dispatch an ambulance from the **🆘 Emergency Dispatch** tab to see the effect

Both features default to **disabled** — the original routing behavior is preserved until you explicitly enable them.

---

## Running Tests

```bash
# Direct execution
python tests/test_fuzzy_bayesian.py

# Using pytest (if installed)
python -m pytest tests/test_fuzzy_bayesian.py -v
```

Tests cover:
- **Fuzzy Logic**: Low/medium/high traffic → appropriate scores, range validation, determinism, invalid inputs
- **Bayesian Reasoning**: Probability bounds, evidence impact, determinism, missing evidence
- **Cost Integration**: Backward compatibility, feature toggling, non-negative weights
- **System Integration**: A* routing, CSP hospital assignment, feature enable/disable roundtrip

---
