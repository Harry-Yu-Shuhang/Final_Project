import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_cumulative_returns(returns: pd.Series, output_path: str = "cumulative_returns.png"):
    cumulative = (1 + returns).cumprod()
    plt.figure(figsize=(10, 5))
    plt.plot(cumulative, label='Portfolio')
    plt.title("Cumulative Returns")
    plt.xlabel("Date")
    plt.ylabel("Net Value")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_weights_heatmap(weights_df: pd.DataFrame, output_path: str = "weights_heatmap.png"):
    import seaborn as sns
    plt.figure(figsize=(12, 6))
    sns.heatmap(weights_df.T, cmap="coolwarm", center=0, cbar_kws={'label': 'Weight'})
    plt.title("Portfolio Weights Over Time")
    plt.xlabel("Date")
    plt.ylabel("ETFs")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
