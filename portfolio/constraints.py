import numpy as np
from typing import Callable

def build_constraints(cov_matrix: np.ndarray, min_vol: float = 0.03, l1_limit: float = 1.0):
    """
    Generate constraint list for optimizer.

    Args:
        cov_matrix (np.ndarray): Covariance matrix of daily returns.
        min_vol (float): Minimum annualized portfolio volatility.
        l1_limit (float): Maximum L1 norm (sum of absolute weights).

    Returns:
        List[dict]: Constraints to be passed into scipy.optimize.minimize
    """
    def port_vol(w):
        var = np.dot(w.T, np.dot(cov_matrix, w))
        return np.sqrt(var) * np.sqrt(252)

    constraints = [
        {'type': 'ineq', 'fun': lambda w: port_vol(w) - min_vol},         # min vol constraint
        {'type': 'ineq', 'fun': lambda w: l1_limit - np.sum(np.abs(w))}   # L1 norm constraint
    ]
    return constraints
