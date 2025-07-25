import numpy as np
import pandas as pd


def simulate_daily_returns(mean_returns, cov_matrix, weights, size=252):
    """
    Simulate portfolio daily return samples using a multivariate normal distribution.

    Parameters:
        mean_returns (array-like): Mean daily returns for each asset.
        cov_matrix (2D array-like): Covariance matrix of asset returns.
        weights (array-like): Portfolio weights for each asset.
        size (int): Number of random samples to generate (default: 252).

    Returns:
        np.ndarray: Array of simulated portfolio daily returns, shape (size,).
    """
    samples = np.random.multivariate_normal(mean_returns, cov_matrix, size)
    portfolio_returns = np.dot(samples, weights)

    return portfolio_returns


def simulate_portfolio_paths(
    mean_returns,
    cov_matrix,
    weights,
    initial_value=10000,
    num_simulations=1000,
):
    """
    Simulate multiple portfolio value paths over time using Monte Carlo simulation.

    Parameters:
        mean_returns (array-like): Mean daily returns for each asset.
        cov_matrix (2D array-like): Covariance matrix of asset returns.
        weights (array-like): Portfolio weights for each asset.
        initial_value (float): Starting portfolio value (default: 10000).
        num_simulations (int): Number of simulation paths to generate (default: 1000).

    Returns:
        list: List of portfolio value paths, where each path is a list of daily values.
              Each simulation path starts with initial_value and shows portfolio value
              evolution over 252 trading days.
    """

    portfolio_paths = []
    for _ in range(num_simulations):
        simulated_daily_returns = simulate_daily_returns(
            mean_returns, cov_matrix, weights
        )

        portfolio_path = [initial_value]
        for day in range(len(simulated_daily_returns)):
            new_value = portfolio_path[-1] * (1 + simulated_daily_returns[day] / 100)
            portfolio_path.append(new_value)

        portfolio_paths.append(portfolio_path)

    return portfolio_paths


def calculate_risk_metrics(portfolio_paths):
    """
    Calculate professional risk metrics from Monte Carlo simulation results.

    Parameters:
        portfolio_paths (list): List of portfolio value paths.
        initial_value (float): Initial portfolio value for percentage calculations.

    Returns:
        dict: Dictionary containing risk metrics with euro amounts and percentages.
    """

    final_values = [path[-1] for path in portfolio_paths]

    # Value at Risk
    var_95 = np.percentile(final_values, 5)
    var_99 = np.percentile(final_values, 1)

    # Conditional Value at Risk
    cvar_95 = np.mean([v for v in final_values if v <= var_95])
    cvar_99 = np.mean([v for v in final_values if v <= var_99])

    initial_value = portfolio_paths[0][0]
    var_95_pct = ((var_95 / initial_value) - 1) * 100
    var_99_pct = ((var_99 / initial_value) - 1) * 100
    cvar_95_pct = ((cvar_95 / initial_value) - 1) * 100
    cvar_99_pct = ((cvar_99 / initial_value) - 1) * 100

    return {
        "var_95": var_95,
        "var_99": var_99,
        "cvar_95": cvar_95,
        "cvar_99": cvar_99,
        "var_95_pct": var_95_pct,
        "var_99_pct": var_99_pct,
        "cvar_95_pct": cvar_95_pct,
        "cvar_99_pct": cvar_99_pct,
    }


def calculate_simulation_statistics(portfolio_paths):
    """
    Calculate comprehensive statistics and metrics from Monte Carlo simulation results.

    This function extracts all the calculations currently done in the visualization
    function, making the code more modular and testable.

    Parameters:
        portfolio_paths (list): List of portfolio value paths.

    Returns:
        dict: Dictionary containing all simulation statistics including:
            - percentiles: 5th, 10th, 25th, 50th, 75th, 90th, 95th percentiles
            - path_indices: indices of median, best, and worst paths
            - final_values: final portfolio values for all paths
            - performance_stats: mean, median, best, worst final values and returns
    """
    portfolio_paths = np.array(portfolio_paths)

    # Calculate percentiles across all paths for each time step
    percentiles = np.percentile(portfolio_paths, [5, 10, 25, 50, 75, 90, 95], axis=0)

    # Get final values and find key paths
    final_values = [path[-1] for path in portfolio_paths]
    median_final = np.median(final_values)
    best_final = np.max(final_values)
    worst_final = np.min(final_values)

    # Find indices of key paths
    median_path_idx = np.argmin(
        [abs(path[-1] - median_final) for path in portfolio_paths]
    )
    best_path_idx = np.argmax(final_values)
    worst_path_idx = np.argmin(final_values)

    # Calculate performance statistics
    initial_value = portfolio_paths[0][0]
    mean_final = np.mean(final_values)

    mean_return_pct = ((mean_final / initial_value) - 1) * 100
    best_return_pct = ((best_final / initial_value) - 1) * 100
    worst_return_pct = ((worst_final / initial_value) - 1) * 100
    median_return_pct = ((median_final / initial_value) - 1) * 100

    return {
        "percentiles": percentiles,
        "path_indices": {
            "median": median_path_idx,
            "best": best_path_idx,
            "worst": worst_path_idx,
        },
        "final_values": final_values,
        "performance_stats": {
            "initial_value": initial_value,
            "mean_final": mean_final,
            "median_final": median_final,
            "best_final": best_final,
            "worst_final": worst_final,
            "mean_return_pct": mean_return_pct,
            "median_return_pct": median_return_pct,
            "best_return_pct": best_return_pct,
            "worst_return_pct": worst_return_pct,
        },
    }


def modify_portfolio_for_regime(mean_returns, cov_matrix, regime_asset_factors):
    """
    Modify mean returns and covariance matrix based on macroeconomic regime factors.

    Args:
        mean_returns: Historical mean returns for each asset
        cov_matrix: Historical covariance matrix of asset returns
        regime_asset_factors: Dictionary of factors for each asset with 'mean_factor' and 'vol_factor' keys, and a global key 'correlation_move_pct' (e.g., {"AAPL": {"mean_factor": 1.1, "vol_factor": 1.2}, ..., "correlation_move_pct": -0.15})

    Returns:
        tuple:
            - pd.Series: Modified mean returns for the regime
            - pd.DataFrame: Modified covariance matrix for the regime
    """
    modified_mean_returns = mean_returns.copy()
    modified_cov_matrix = cov_matrix.copy()

    for ticker_i in cov_matrix.columns:
        if ticker_i not in regime_asset_factors:
            return modified_mean_returns, modified_cov_matrix
        # Modify mean returns
        # Use loc for position-based assignment to avoid FutureWarning
        modified_mean_returns.loc[ticker_i] *= regime_asset_factors[ticker_i][
            "mean_factor"
        ]

        # --- Covariance Matrix Regime Adjustment ---
        # - Diagonal elements (i == j): variance is scaled by (vol_factor)^2, so volatility is scaled by vol_factor.
        # - Off-diagonal elements (i != j): covariance is scaled by both assets' vol_factors, reflecting how joint risk changes.
        #   This preserves the correlation structure (correlations are unchanged), but increases or decreases the overall risk.
        for ticker_j in cov_matrix.columns:

            vi = regime_asset_factors[ticker_i]["vol_factor"]
            vj = regime_asset_factors[ticker_j]["vol_factor"]

            #   modified_cov[ticker_i, ticker_j] = original_cov[i, j] * vol_factor_i * vol_factor_j
            modified_cov_matrix.loc[ticker_i, ticker_j] *= vi * vj

    modified_cov_matrix_analysis = analyze_portfolio_correlation(modified_cov_matrix)

    corr_matrix = modified_cov_matrix_analysis["correlation_matrix"]
    stdev_outer_product = modified_cov_matrix_analysis["stdev_outer_product"]

    # Adjust all off-diagonal correlations by the regime's correlation_move_pct, then rebuild the covariance matrix.
    for ticker_i in cov_matrix.columns:
        for ticker_j in cov_matrix.columns:
            if ticker_i != ticker_j:
                new_corr = (
                    corr_matrix.loc[ticker_i, ticker_j]
                    + corr_matrix.loc[ticker_i, ticker_j]
                    * regime_asset_factors["correlation_move_pct"]
                )
                corr_matrix.loc[ticker_i, ticker_j] = np.clip(new_corr, -1, 1)
    new_cov = corr_matrix.values * stdev_outer_product
    modified_cov_matrix = pd.DataFrame(
        new_cov, index=cov_matrix.columns, columns=cov_matrix.columns
    )

    return modified_mean_returns, modified_cov_matrix


def analyze_portfolio_risk_factors(cov_matrix):
    """
    Perform principal component analysis (PCA) on a covariance matrix to identify dominant risk factors in a portfolio.

    This function computes the eigenvalues and eigenvectors of the covariance matrix, sorts them in descending order of variance explained, and identifies the dominant principal components (PCs) with eigenvalues > 1.0. For each dominant PC, it determines the top contributing assets (by absolute loading percentage), selecting either all assets above a 10% threshold or the top 2 contributors.

    Parameters:
        cov_matrix (pd.DataFrame): Covariance matrix of asset returns (assets as both rows and columns).

    Returns:
        dict: Dictionary containing:
            - 'eigenvalues': np.ndarray of sorted eigenvalues (variance explained by each PC)
            - 'dominant_factor_loadings': dict mapping PC index (1-based) to list of top asset contributors (dicts with 'asset' and 'pct')
            - 'explained_variance_dominant': float, total variance explained by dominant PCs (as a percentage)
    """
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix.values)

    # Sort eigenvalues and eigenvectors from largest to smallest
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    dominant_factor_loadings = {}
    threshold = 10  # percent threshold for asset contribution
    explained_variance_dominant = 0

    # Loop through PCs, only considering those with eigenvalue > 1.0 (dominant factors)
    for pc_idx, eigval in enumerate(eigenvalues):
        if eigval < 1.0:
            break

        # Accumulate explained variance for dominant PCs
        explained_variance_dominant += eigenvalues[pc_idx] / sum(eigenvalues) * 100

        pc_vector = eigenvectors[:, pc_idx]

        # Calculate absolute loadings and their percentage contribution
        abs_loadings = [abs(x) for x in pc_vector]
        total = sum(abs_loadings)
        pct_loadings = [(val / total) * 100 for val in abs_loadings]

        # Pair each asset with its loading percentage
        pc_assets = sorted(
            [
                {"asset": cov_matrix.columns[i], "pct": pct_loadings[i]}
                for i in range(len(pct_loadings))
            ],
            key=lambda x: x["pct"],
            reverse=True,
        )

        # Smart selection: Top 2 OR all above threshold
        top_2 = pc_assets[:2]
        eigval_is_small = eigval < 5.0  # Remove clutter from chart
        above_threshold = [i for i in pc_assets if i["pct"] >= threshold]

        selected_assets = (
            above_threshold
            if len(above_threshold) > 2 and not eigval_is_small
            else top_2
        )

        dominant_factor_loadings[pc_idx + 1] = selected_assets

    # Return PCA results and dominant factor analysis
    # Each principal component (PC) is a 6D vector (for 6 assets), showing how much each asset contributes to that risk factor.
    # PC1 is the eigenvector with the highest risk (largest variance explained).
    return {
        "eigenvalues": eigenvalues,
        "dominant_factor_loadings": dominant_factor_loadings,
        "explained_variance_dominant": explained_variance_dominant,
    }


def analyze_portfolio_correlation(cov_matrix):
    """
    Compute eigenvalues, condition number, and correlation matrix from a covariance matrix.

    Args:
        cov_matrix (pd.DataFrame): Covariance matrix of asset returns.

    Returns:
        dict: Condition number, correlation matrix, and stdev outer product.
    """
    eigenvalues, _ = np.linalg.eig(cov_matrix.values)

    condition_number = max(eigenvalues) / min(eigenvalues)

    # Compute correlation matrix
    std_devs = np.sqrt(np.diag(cov_matrix.values))
    stdev_outer_product = np.outer(std_devs, std_devs)
    corr_matrix = cov_matrix.values / stdev_outer_product
    corr_matrix = np.clip(corr_matrix, -1, 1)  # Numerical safety

    corr_matrix_df = pd.DataFrame(
        corr_matrix, index=cov_matrix.columns, columns=cov_matrix.columns
    )

    return {
        "condition_number": condition_number,
        "correlation_matrix": corr_matrix_df,
        "stdev_outer_product": stdev_outer_product,
    }
