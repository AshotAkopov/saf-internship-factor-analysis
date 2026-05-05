import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant


# My functions

def corr_over_threshold(df, threshold=0.95, method: str = "pearson"):
    """
    Identifies pairs of columns in a DataFrame whose absolute correlation
    exceeds a given threshold.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        threshold (float): Absolute correlation threshold.
        method (str): Correlation method ('pearson', 'spearman', 'kendall').

    Returns:
        pd.Series: Column pairs and their correlation coefficients.
    """
    corr_matrix = df.corr(method=method).abs()

    mask = np.triu(np.ones(corr_matrix.shape, dtype=bool), k=1)
    upper_triangle = corr_matrix.where(mask)

    correlations = (
        upper_triangle.stack()
        .rename("correlation")
        .sort_values(ascending=False)
    )

    return correlations[correlations > threshold]


def pca_results(pca, X_pca, X_original, individual_index=None):
    """
    Computes the main indicators associated with a fitted sklearn PCA.

    Parameters
    ----------
    pca : sklearn.decomposition.PCA
        Fitted PCA object.
    X_pca : np.ndarray
        Coordinates of the individuals in the principal component space.
    X_original : pd.DataFrame
        Original data used for PCA.
    individual_index : array-like, optional
        Index of the individuals. If None, a RangeIndex is used.

    Returns
    -------
    dict of pd.DataFrame
        Dictionary containing eigenvalues, explained variance ratio,
        individual coordinates, cos², contributions, eigenvectors,
        variable coordinates, cos² and contributions.
    """
    if individual_index is None:
        individual_index = range(X_pca.shape[0])

    eigenvalues = pd.DataFrame(
        pca.explained_variance_,
        columns=["Eigenvalue"],
        index=[f"PC{i+1}" for i in range(len(pca.explained_variance_))]
    )

    explained_variance_ratio = pd.DataFrame(
        pca.explained_variance_ratio_,
        columns=["Explained_variance_ratio"],
        index=[f"PC{i+1}" for i in range(len(pca.explained_variance_ratio_))]
    )

    individual_coordinates = pd.DataFrame(
        X_pca,
        index=individual_index,
        columns=[f"PC{i+1}" for i in range(X_pca.shape[1])]
    )

    individual_cos2 = individual_coordinates ** 2

    n = X_pca.shape[0]
    individual_contributions = (individual_coordinates ** 2) / (
        n * pca.explained_variance_
    )

    eigenvectors = pd.DataFrame(
        pca.components_,
        columns=X_original.columns,
        index=[f"PC{i+1}" for i in range(len(pca.components_))]
    )

    variable_coordinates = pd.DataFrame(
        pca.components_.T * np.sqrt(pca.explained_variance_),
        columns=[f"PC{i+1}" for i in range(len(pca.explained_variance_))],
        index=X_original.columns
    )

    variable_cos2 = variable_coordinates ** 2

    variable_contributions = (variable_coordinates ** 2) / pca.explained_variance_

    return {
        "eigenvalues": eigenvalues,
        "explained_variance_ratio": explained_variance_ratio,
        "individual_coordinates": individual_coordinates,
        "individual_cos2": individual_cos2,
        "individual_contributions": individual_contributions,
        "eigenvectors": eigenvectors,
        "variable_coordinates": variable_coordinates,
        "variable_cos2": variable_cos2,
        "variable_contributions": variable_contributions
    }


def double_axis_plot(explained_variance):
    """
    Plots explained variance and cumulative explained variance.

    Parameters
    ----------
    explained_variance : array-like
        Explained variance ratio for each principal component.
    """
    plt.bar(range(1, len(explained_variance) + 1), explained_variance)
    plt.ylabel("Explained variance")
    plt.xlabel("Components")

    plt.plot(
        range(1, len(explained_variance) + 1),
        np.cumsum(explained_variance),
        color="red",
        label="Cumulative explained variance",
        marker="o"
    )

    plt.legend(loc="upper left")
    plt.show()


def kaiser_plot(eigenvalues):
    """
    Displays a scree plot with Kaiser's criterion and prints how many
    eigenvalues are greater than 1.

    Parameters
    ----------
    eigenvalues : array-like
        Ordered eigenvalues.
    """
    k = int(np.sum(eigenvalues > 1.0))
    print(f"{k} eigenvalue(s) are greater than 1 according to Kaiser's criterion.")

    plt.plot(eigenvalues, marker="o")
    plt.axhline(y=1.0, linestyle="--", color="red")
    plt.title("Scree plot with Kaiser's criterion")
    plt.xlabel("Principal component")
    plt.ylabel("Eigenvalue")
    plt.grid(True, linestyle=":", linewidth=0.5)
    plt.show()


def parallel_analysis(X, n_iter=500, quantile=0.95, random_state=None):
    """
    Performs Horn's parallel analysis for PCA.

    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        Input data. The data do not need to be standardized beforehand.
    n_iter : int, default=500
        Number of random datasets to simulate.
    quantile : float, default=0.95
        Quantile used as the simulated threshold.
        0.95 corresponds to Glorfeld's conservative approach.
        0.50 corresponds to Horn's original approach.
    random_state : int or None, default=None
        Random seed for reproducibility.

    Returns
    -------
    k : int
        Number of components to retain.
    observed_eigenvalues : np.ndarray
        Eigenvalues computed from the observed data.
    simulated_thresholds : np.ndarray
        Simulated eigenvalue thresholds.
    """
    rng = np.random.default_rng(random_state)
    X = np.asarray(X, dtype=float)

    n, p = X.shape

    # Standardize the data.
    X_std = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)

    # Compute the correlation matrix and observed eigenvalues.
    corr_matrix = np.corrcoef(X_std, rowvar=False)
    observed_eigenvalues = np.linalg.eigvalsh(corr_matrix)[::-1]

    # Simulate random datasets and store their eigenvalues.
    simulated_eigenvalues = np.empty((n_iter, p))

    for i in range(n_iter):
        Z = rng.normal(size=(n, p))
        Z = (Z - Z.mean(axis=0)) / Z.std(axis=0, ddof=1)

        simulated_corr_matrix = np.corrcoef(Z, rowvar=False)
        simulated_eigenvalues[i] = np.linalg.eigvalsh(simulated_corr_matrix)[::-1]

    # Compute simulated thresholds.
    simulated_thresholds = np.quantile(simulated_eigenvalues, quantile, axis=0)

    # Retain components whose observed eigenvalue is greater than the threshold.
    k = int(np.sum(observed_eigenvalues > simulated_thresholds))
    print(f"Number of retained components: {k}")

    plt.plot(
        range(1, p + 1),
        observed_eigenvalues,
        marker="o",
        label="Observed eigenvalues"
    )

    plt.plot(
        range(1, p + 1),
        simulated_thresholds,
        marker="x",
        label=f"Simulated {quantile * 100:.0f}% threshold"
    )

    plt.axvline(
        k,
        color="red",
        linestyle="--",
        label=f"{k} retained components"
    )

    plt.xlabel("Principal component")
    plt.ylabel("Eigenvalue")
    plt.title("Horn's parallel analysis")
    plt.legend()
    plt.show()

    return k, observed_eigenvalues, simulated_thresholds


def average_squared_off_diagonals(R):
    """
    Computes the average squared off-diagonal correlations.

    Parameters
    ----------
    R : np.ndarray
        Correlation matrix.

    Returns
    -------
    float
        Mean of the squared off-diagonal values.
    """
    p = R.shape[0]
    mask = ~np.eye(p, dtype=bool)

    off_diagonal_values = R[mask]
    squared_values = off_diagonal_values ** 2

    return np.mean(squared_values)


def velicer_map(
    X,
    max_components=None,
    plot=True,
    show_values=True,
    return_avg_sqrs=False,
    return_k_map=False
):
    """
    Performs Velicer's MAP test.

    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        Input data.
    max_components : int or None, default=None
        Maximum number of components to test. If None, p - 1 is used.
    plot : bool, default=True
        If True, displays the MAP curve.
    show_values : bool, default=True
        If True, displays numerical values on the plot.
    return_avg_sqrs : bool, default=False
        If True, returns the average squared correlations for each step.
    return_k_map : bool, default=False
        If True, returns the optimal number of components.

    Returns
    -------
    list, int or None
        Depending on the return parameters.
    """
    X = np.asarray(X, dtype=float)
    _, p = X.shape

    if max_components is None:
        max_components = p - 1

    # Standardize the data.
    X_std = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)

    # Step 0: correlation matrix of the standardized data.
    corr_matrix = np.corrcoef(X_std, rowvar=False)
    avg_sqrs = [average_squared_off_diagonals(corr_matrix)]

    # Subsequent steps: remove k principal components and compute residual correlations.
    for k in range(1, max_components + 1):
        pca = PCA(n_components=k)
        scores = pca.fit_transform(X_std)

        reconstructed_X = pca.inverse_transform(scores)
        residuals = X_std - reconstructed_X

        residual_corr_matrix = np.corrcoef(residuals, rowvar=False)
        avg_sqrs.append(average_squared_off_diagonals(residual_corr_matrix))

    k_map = int(np.argmin(avg_sqrs))

    if plot:
        steps = np.arange(len(avg_sqrs))

        plt.figure()
        plt.plot(steps, avg_sqrs, marker="o")
        plt.axvline(
            k_map,
            linestyle="--",
            color="red",
            label=f"Minimum at step {k_map}"
        )

        if show_values:
            for i, value in enumerate(avg_sqrs):
                plt.text(
                    i,
                    value,
                    f"{value:.3f}",
                    ha="center",
                    va="bottom",
                    fontsize=8
                )

        plt.xlabel("Step (k removed components)")
        plt.ylabel("Average squared off-diagonal correlations")
        plt.title("Velicer's MAP test")
        plt.legend()
        plt.show()

    if return_avg_sqrs and return_k_map:
        return k_map, avg_sqrs

    if return_avg_sqrs:
        return avg_sqrs

    if return_k_map:
        return k_map

    return None


def pca_top(results: dict, indicator="variable_coordinates", dim="PC1", top=10, *, return_frames=False):
    """
    Displays the top and bottom values for a given PCA indicator and dimension.

    Values are ranked by absolute value, but displayed with their original sign.
    The two associated indicators are also displayed.

    Parameters
    ----------
    results : dict
        Dictionary returned by pca_results(...).
    indicator : str, default="variable_coordinates"
        Indicator to analyze. Possible values are:
        'variable_coordinates', 'variable_cos2', 'variable_contributions',
        'individual_coordinates', 'individual_cos2', 'individual_contributions'.
    dim : str, default="PC1"
        Principal component to analyze.
    top : int, default=10
        Number of values to display.
    return_frames : bool, default=False
        If True, returns the two displayed DataFrames.

    Returns
    -------
    None or tuple(pd.DataFrame, pd.DataFrame)
    """
    variable_indicators_names = [
        "variable_coordinates",
        "variable_cos2",
        "variable_contributions"
    ]

    individual_indicators_names = [
        "individual_coordinates",
        "individual_cos2",
        "individual_contributions"
    ]

    variable_indicators = {
        "variable_coordinates": results["variable_coordinates"],
        "variable_cos2": results["variable_cos2"],
        "variable_contributions": results["variable_contributions"]
    }

    individual_indicators = {
        "individual_coordinates": results["individual_coordinates"],
        "individual_cos2": results["individual_cos2"],
        "individual_contributions": results["individual_contributions"]
    }

    if indicator in variable_indicators:
        df = variable_indicators[indicator]
        associated_indicators = variable_indicators.copy()
        del associated_indicators[indicator]
        indicator_group = variable_indicators_names
        label = "Variable"

    elif indicator in individual_indicators:
        df = individual_indicators[indicator]
        associated_indicators = individual_indicators.copy()
        del associated_indicators[indicator]
        indicator_group = individual_indicators_names
        label = "Observation"

    else:
        raise ValueError(
            "Invalid indicator. Please use one of the keys returned by pca_results()."
        )

    sorted_index = df[dim].abs().sort_values(ascending=False).index

    top_values = df.loc[sorted_index].head(top)[dim]
    bottom_values = df.loc[sorted_index].tail(top)[dim]

    associated_names = [name for name in indicator_group if name != indicator]

    associated_1_top = associated_indicators[associated_names[0]].loc[top_values.index, dim]
    associated_2_top = associated_indicators[associated_names[1]].loc[top_values.index, dim]

    associated_1_bottom = associated_indicators[associated_names[0]].loc[bottom_values.index, dim]
    associated_2_bottom = associated_indicators[associated_names[1]].loc[bottom_values.index, dim]

    top_df = pd.concat([top_values, associated_1_top, associated_2_top], axis=1)
    top_df.columns = [indicator, associated_names[0], associated_names[1]]

    bottom_df = pd.concat([bottom_values, associated_1_bottom, associated_2_bottom], axis=1)
    bottom_df.columns = [indicator, associated_names[0], associated_names[1]]

    top_df = top_df.reset_index()
    top_df.rename(columns={top_df.columns[0]: label}, inplace=True)

    bottom_df = bottom_df.reset_index()
    bottom_df.rename(columns={bottom_df.columns[0]: label}, inplace=True)

    print(f"Top {top} values for indicator '{indicator}' on dimension '{dim}':")
    print(top_df)
    print()
    print(f"Bottom {top} values for indicator '{indicator}' on dimension '{dim}':")
    print(bottom_df)

    return (top_df, bottom_df) if return_frames else None


def plot_correlation_circle(
    coord_var,
    feature_names,
    ax1=1,
    ax2=2,
    threshold=None,
    figsize=(6, 6),
    show_unselected=False,
    unselected_color="#bbbbbb",
    unselected_alpha=0.4,
    use_cos2=False
):
    """
    Plots the correlation circle of a PCA.

    Each variable is represented by a vector starting from the origin and
    pointing to its coordinates on two principal components.

    Parameters
    ----------
    coord_var : pd.DataFrame or np.ndarray
        Variable coordinates in the factor space.
    feature_names : list of str
        Names of the variables to display.
    ax1 : int, default=1
        First principal component to plot. Numbering starts at 1.
    ax2 : int, default=2
        Second principal component to plot. Numbering starts at 1.
    threshold : None, float or tuple(float, float), default=None
        Filtering threshold.
        If None, all variables are displayed.
        If float, the same threshold is applied to both axes.
        If tuple, different thresholds are applied to each axis.
    figsize : tuple, default=(6, 6)
        Figure size.
    show_unselected : bool, default=False
        If True, also displays variables not selected by the threshold.
    unselected_color : str, default="#bbbbbb"
        Color of unselected vectors.
    unselected_alpha : float, default=0.4
        Transparency of unselected vectors.
    use_cos2 : bool, default=False
        If False, filtering is based on absolute coordinates.
        If True, filtering is based on cos².

    Returns
    -------
    matplotlib.axes.Axes
        Matplotlib Axes object.
    """
    ax1 -= 1
    ax2 -= 1

    coord_array = coord_var.values if hasattr(coord_var, "values") else np.asarray(coord_var)

    mode = "no_filter"
    sx = sy = None

    if threshold is None:
        mode = "no_filter"

    elif np.isscalar(threshold):
        if float(threshold) <= 0:
            mode = "no_filter"
        else:
            sx = sy = float(threshold)
            mode = "both_nonzero"

    else:
        threshold_values = list(threshold)

        if len(threshold_values) != 2:
            raise ValueError(
                "`threshold` must be None, a scalar, or a tuple (threshold_PC1, threshold_PC2)."
            )

        sx, sy = float(threshold_values[0]), float(threshold_values[1])
        nonzero_x, nonzero_y = sx > 0, sy > 0

        if nonzero_x and nonzero_y:
            mode = "both_nonzero"
        elif nonzero_x or nonzero_y:
            mode = "one_nonzero"
        else:
            mode = "no_filter"

    fig, ax = plt.subplots(figsize=figsize)
    handles, labels = [], []

    for i in range(len(feature_names)):
        x, y = coord_array[i, ax1], coord_array[i, ax2]

        if mode == "no_filter":
            color = "blue"
            ax.arrow(
                0, 0, x, y,
                head_width=0.03,
                head_length=0.03,
                fc=color,
                ec=color,
                alpha=0.8
            )
            ax.text(
                x * 1.1,
                y * 1.1,
                feature_names[i],
                color=color,
                ha="center",
                va="center"
            )
            continue

        if use_cos2:
            cx, cy = x * x, y * y
            cond_x = sx is not None and sx > 0 and cx > sx
            cond_y = sy is not None and sy > 0 and cy > sy
        else:
            cond_x = sx is not None and sx > 0 and abs(x) > sx
            cond_y = sy is not None and sy > 0 and abs(y) > sy

        if cond_x or cond_y:
            if cond_x and cond_y:
                color = "purple"
                label_text = (
                    f"cos² > ({sx:.3g}, {sy:.3g}) on PC{ax1+1} and PC{ax2+1}"
                    if use_cos2 else
                    f"|coord| > ({sx:.3g}, {sy:.3g}) on PC{ax1+1} and PC{ax2+1}"
                )

            elif cond_x:
                color = "red"

                if mode == "one_nonzero" and not (sy and sy > 0):
                    label_text = (
                        f"cos² > {sx:.3g} on PC{ax1+1} "
                        f"(no filter on PC{ax2+1})"
                        if use_cos2 else
                        f"|coord| > {sx:.3g} on PC{ax1+1} "
                        f"(no filter on PC{ax2+1})"
                    )
                else:
                    label_text = (
                        f"cos² > {sx:.3g} on PC{ax1+1}"
                        if use_cos2 else
                        f"|coord| > {sx:.3g} on PC{ax1+1}"
                    )

            else:
                color = "green"

                if mode == "one_nonzero" and not (sx and sx > 0):
                    label_text = (
                        f"cos² > {sy:.3g} on PC{ax2+1} "
                        f"(no filter on PC{ax1+1})"
                        if use_cos2 else
                        f"|coord| > {sy:.3g} on PC{ax2+1} "
                        f"(no filter on PC{ax1+1})"
                    )
                else:
                    label_text = (
                        f"cos² > {sy:.3g} on PC{ax2+1}"
                        if use_cos2 else
                        f"|coord| > {sy:.3g} on PC{ax2+1}"
                    )

            ax.arrow(
                0, 0, x, y,
                head_width=0.03,
                head_length=0.03,
                fc=color,
                ec=color,
                alpha=0.8
            )

            ax.text(
                x * 1.1,
                y * 1.1,
                feature_names[i],
                color=color,
                ha="center",
                va="center"
            )

            if label_text not in labels:
                handles.append(plt.Line2D([0], [0], color=color, lw=2))
                labels.append(label_text)

        elif show_unselected:
            ax.arrow(
                0, 0, x, y,
                head_width=0.03,
                head_length=0.03,
                fc=unselected_color,
                ec=unselected_color,
                alpha=unselected_alpha
            )

            ax.text(
                x * 1.1,
                y * 1.1,
                feature_names[i],
                color=unselected_color,
                alpha=unselected_alpha,
                ha="center",
                va="center"
            )

    ax.add_patch(
        plt.Circle(
            (0, 0),
            1,
            facecolor="none",
            edgecolor="gray",
            linestyle="--"
        )
    )

    ax.axhline(0, color="black", lw=1)
    ax.axvline(0, color="black", lw=1)

    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect("equal", "box")

    ax.set_xlabel(f"PC{ax1+1}")
    ax.set_ylabel(f"PC{ax2+1}")

    if mode == "no_filter":
        ax.set_title("Correlation circle")
    else:
        s1 = f"{sx:.3g}" if sx is not None and sx > 0 else "none"
        s2 = f"{sy:.3g}" if sy is not None and sy > 0 else "none"
        metric_label = "cos²" if use_cos2 else "|coord|"

        ax.set_title(
            f"Correlation circle "
            f"({metric_label} thresholds: PC{ax1+1}={s1}, PC{ax2+1}={s2})"
        )

        if handles:
            ax.legend(handles, labels, loc="lower left")

    return ax


def calculate_vif(X, order_by_vif=True):
    """
    Computes the Variance Inflation Factor (VIF) for each variable.

    Parameters
    ----------
    X : pd.DataFrame
        DataFrame containing the explanatory variables.
    order_by_vif : bool, default=True
        If True, sorts the output by decreasing VIF.

    Returns
    -------
    pd.DataFrame
        DataFrame containing variables and their corresponding VIF values.
    """
    X_with_const = add_constant(X)

    vif_data = pd.DataFrame()
    vif_data["Variable"] = X_with_const.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X_with_const.values, i)
        for i in range(X_with_const.shape[1])
    ]

    if order_by_vif:
        vif_data = vif_data.sort_values(
            by="VIF",
            ascending=False
        ).reset_index(drop=True)

    return vif_data
