# QF623 ETF Portfolio Management Project

This project implements an ETF portfolio strategy that aims to **maximize the Sharpe Ratio** under a **minimum volatility constraint**, using historical price and volume data from Yahoo Finance.

---

## 🔍 Objective

- Select a universe of ETFs (excluding leveraged/inverse funds)
- Generate alpha signals using a **trend-following strategy**
- Construct a long-only or long-short portfolio with:
  - Annualized risk ≥ 3%
  - Absolute sum of weights ≤ 100%
- Simulate portfolio execution with **T+1 rebalancing**
- Evaluate performance metrics and **explain factor exposures**

---

## ⚙️ Methodology

### 1. ETF Universe Construction
- Filter ETFs by keywords like `3x`, `inverse`, `ultra` and volume threshold
- See: `data/etf_universe.py`

### 2. Alpha Signal: Trend Following
- Calculate short (20-day) and long (100-day) moving averages
- Signal = short_MA - long_MA (positive = bullish)

### 3. Portfolio Optimization
- Objective: maximize Sharpe ratio
- Constraints:
  - Annualized volatility ≥ 3%
  - L1 norm (∑|weights|) ≤ 1
- Solver: `scipy.optimize.minimize` with SLSQP

### 4. T+1 Execution Logic
- Signal generated at time T
- Portfolio rebalanced at T+1 close
- Returns measured from T+1 to T+2

### 5. Performance Attribution
- Compute:
  - Annualized return, volatility, Sharpe ratio
  - Beta exposures to macro/equity factors (optional)
  - Hedging impact (optional)

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Or if using poetry
poetry install
```

```bash
# Run the strategy
python main.py
```

---

## 📈 Example Output

**Cumulative Portfolio Returns (T+1 Execution):**

![Cumulative Returns](./cumulative_returns.png)

---

## 📁 Project Structure

```
QF623_Final_Project/
├── config/
├── data/
├── signals/
├── portfolio/
├── execution/
├── attribution/
├── utils/
├── main.py
└── cumulative_returns.png
```

---

## 📜 License

MIT License