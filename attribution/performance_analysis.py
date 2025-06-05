import pandas as pd
import numpy as np
import statsmodels.api as sm
from utils.metrics import annualized_return, annualized_volatility, sharpe_ratio


def compute_basic_metrics(portfolio_returns: pd.Series) -> dict:
    return {
        "annual_return": annualized_return(portfolio_returns),
        "annual_volatility": annualized_volatility(portfolio_returns),
        "sharpe_ratio": sharpe_ratio(portfolio_returns)
    }

def compute_beta_exposure(portfolio_returns: pd.Series, factor_df: pd.DataFrame) -> pd.Series:
    """
    Run regression of portfolio returns on risk factors to compute beta exposure.
    """
    aligned = pd.concat([portfolio_returns, factor_df], axis=1).dropna()
    y = aligned.iloc[:, 0]
    X = aligned.iloc[:, 1:]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    return model.params  # includes intercept (alpha)

def analyze_performance(portfolio_returns: pd.Series, factor_df: pd.DataFrame = None,
                        hedge_returns: pd.Series = None) -> None:
    """
    Main entry for performance attribution analysis.
    Also writes summary to result.md.
    """
    lines = []

    # === Basic performance ===
    basic = compute_basic_metrics(portfolio_returns)
    print("\n✅ Basic Performance Metrics:")
    lines.append("# 📈 Basic Performance Metrics\n")
    for k, v in basic.items():
        print(f"{k}: {v:.4f}")
        lines.append(f"- **{k.replace('_', ' ').title()}**: {v:.4f}")

    # === Factor exposure ===
    if factor_df is not None:
        lines.append("\n---\n\n# 📉 Beta Exposure to Risk Factors\n")
        print("\n📈 Beta Exposures to Risk Factors:")
        betas = compute_beta_exposure(portfolio_returns, factor_df)
        for k, v in betas.items():
            print(f"{k}: {v:.4f}")
            lines.append(f"- **{k}**: {v:.4f}")

    # === Hedge effect ===
    if hedge_returns is not None:
        lines.append("\n---\n\n# 🧩 Effect of Hedging\n")
        print("\n🔍 Evaluating effect of hedging:")
        combined = portfolio_returns + hedge_returns
        hedged_metrics = compute_basic_metrics(combined)
        print("With Hedging:")
        lines.append("## With Hedging:")
        for k, v in hedged_metrics.items():
            print(f"{k}: {v:.4f}")
            lines.append(f"- **{k.replace('_', ' ').title()}**: {v:.4f}")

    # === Save to result.md ===
    result_md = "result.md"
    with open(result_md, "w") as f:
        f.write("\n".join(lines))
        f.write("\n\n---\n\n![Cumulative Returns](./cumulative_returns.png)\n")

    print(f"\n📝 Results saved to {result_md}")

