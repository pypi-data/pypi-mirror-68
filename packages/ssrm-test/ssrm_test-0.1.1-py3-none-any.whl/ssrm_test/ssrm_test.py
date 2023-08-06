import warnings
from typing import List

import numpy as np
from scipy.special import gammaln, loggamma, xlogy
from toolz.itertoolz import accumulate


def update_posterior(n: np.ndarray, alpha: np.ndarray) -> np.ndarray:
    """
    Updates posterior distribution.

    Parameters
    ----------
    n : np.ndarray
        Amount to update posterior distribution parameter by.
    alpha : np.ndarray
        Posterior distribution parameter.

    Returns
    -------
    np.ndarray
        Updated alpha parameter, which defines the posterior.
    """
    return n + alpha


def log_posterior_predictive(n: np.ndarray, alpha: np.ndarray) -> float:
    """
    Log posterior predictive density resulting from marginalizing a
    multinomial likelihood with a dirichlet(alpha) prior, evaluated at n.

    Parameters
    ----------
    n : np.ndarray
        A new data point.
    alpha : np.ndarray
        Parameter defining the dirichlet distribution.

    Returns
    -------
    float
        log posterior predictive density evaluated at n.
    """

    return (
        loggamma(n.sum() + 1)
        - loggamma(n + 1).sum()
        + loggamma(alpha.sum())
        - loggamma(alpha).sum()
        + loggamma(alpha + n).sum()
        - loggamma((alpha + n).sum())
    )


def accumulator(acc: dict, new_data_point: np.ndarray) -> dict:
    """
    Binary operator for accumulating statistical quantities across a stream of data.

    Parameters
    ----------
    acc : dict
        Contains posterior parameters and log marginal likelihoods at previous data point.
    new_data_point : np.ndarray
        Number of counts in each variation.

    Returns
    -------
    dict
        A dictionary storing accumulated values with the same keys as in acc.
    """
    out = {
        "log_marginal_likelihood_M1": acc["log_marginal_likelihood_M1"]
        + log_posterior_predictive(new_data_point, acc["posterior_M1"]),
        "log_marginal_likelihood_M0": acc["log_marginal_likelihood_M0"]
        + multinomiallogpmf(new_data_point, new_data_point.sum(), acc["posterior_M0"])
        if new_data_point.sum() > 0
        else acc["log_marginal_likelihood_M0"],
        "posterior_M1": acc["posterior_M1"] + new_data_point,
        "posterior_M0": acc["posterior_M0"],
    }
    return out


def posterior_probability(bayes_factor: float) -> float:
    """
    Computes the posterior probability given a Bayes Factor.

    Parameters
    ----------
    bayes_factor : float
        Bayes factor of a SRM.

    Returns
    -------
    float
        The posterior probability of a sample ratio mismatch.
    """
    if bayes_factor == np.Inf:
        return 1
    elif bayes_factor == -np.Inf:
        return 0
    else:
        return bayes_factor / (1.0 + bayes_factor)


def bayes_factor(posterior: dict) -> float:
    """
    Returns the Bayes Factor (BF) of an SRM.
    The BF can be np.Inf (numerically), which occurs when the data is
    overwhelmingly in favour of a SRM, but that is not an issue and is
    handled correctly by other functions.

    Parameters
    ----------
    posterior : dict
        Posterior distribution parameters.

    Returns
    -------
    float
        Bayes factor of a SRM.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        bf = np.exp(
            posterior["log_marginal_likelihood_M1"]
            - posterior["log_marginal_likelihood_M0"]
        )
    return bf


def total_n(posterior: dict) -> float:
    """
    Returns the total number of datapoints in the posterior.

    Parameters
    ----------
    posterior : dict
        Posterior distribution parameters.

    Returns
    -------
    float
        Total number of datapoints in the posterior.
    """
    return np.sum(posterior["posterior_M1"] - posterior["posterior_M0"])


def sequential_posteriors(
    data: np.ndarray, null_probabilities: np.ndarray, dirichlet_alpha=None
) -> List[dict]:
    """
    Accumulates the posteriors and marginal likelihoods for each datapoint.

    Parameters
    ----------
    data : List[tuple]
        Data.
    null_probabilities : np.ndarray
        The expected traffic allocation probability, where the values must sum to 1.
    dirichlet_alpha : float
        The parameter defining the dirichlet prior.

    Returns
    -------
    List[dict]
        Posterior distribution and marginal likelihoods at every datapoint.

    Examples
    --------
    For unit-level data, we can use sequential_posteriors like so:
    >>> data = np.array([[1, 0, 0], [0, 1, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    >>> null_probabilities = [0.4, 0.4, 0.2]
    >>> list_dict = sequential_posteriors(data, null_probabilities)

    For time-aggregated data, we can pass in tuples that represent the
    aggregated count during that time:
    >>> data = np.array([[20, 17, 9], [18, 21, 8], [4, 6, 4], [18, 19, 11]])
    >>> null_probabilities = [0.4, 0.4, 0.2]
    >>> list_dict = sequential_posteriors(data, null_probabilities)
    """
    if dirichlet_alpha is None:
        dirichlet_alpha = np.array([1] * len(null_probabilities))
    acc = {
        "log_marginal_likelihood_M1": 0,
        "log_marginal_likelihood_M0": 0,
        "posterior_M1": dirichlet_alpha,
        "posterior_M0": null_probabilities,
    }
    return list(accumulate(accumulator, data, acc))[1:]


def sequential_p_values(bayes_factors: List[float]) -> List[float]:
    """
    Computes a sequentially valid p-value from Bayes factors.

    Parameters
    ----------
    bayes_factors : List[float]
        List of Bayes factors.

    Returns
    -------
    List[float]
        Sequentially valid p-values.
    """
    inverse_bayes_factors = [1 / bf for bf in bayes_factors]
    return list(accumulate(min, inverse_bayes_factors, 1))


def srm_test(data: np.ndarray, null_probabilities: np.ndarray) -> float:
    """
    Creates a Sample Ratio Mismatch (SRM) test to validate whether an
    experiment follows a predefined distribution of data amongst its
    variations.

    Parameters
    ----------
    data : np.ndarray
        Data.
    null_probabilities : np.ndarray
        The expected traffic allocation probability, where the values must sum to 1.

    Returns
    -------
    float
        Final posterior probability of a sample ratio mismatch.

    Examples
    --------
    For unit-level data, we can use sequential_posteriors like so:
    >>> data = np.array([[1, 0, 0], [0, 1, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    >>> null_probabilities = [0.4, 0.4, 0.2]
    >>> prob = srm_test(data, null_probabilities)

    For time-aggregated data, we can pass in tuples that represent the
    aggregated count during that time:
    >>> data = np.array([[20, 17, 9], [18, 21, 8], [4, 6, 4], [18, 19, 11]])
    >>> null_probabilities = [0.4, 0.4, 0.2]
    >>> prob = srm_test(data, null_probabilities)
    """
    final_posterior = sequential_posteriors(data, null_probabilities)[-1]
    final_bf = bayes_factor(final_posterior)
    post_prob = posterior_probability(final_bf)
    return post_prob


def get_bayes_factor_threshold(
    y: List[int], dirichlet_alpha: np.ndarray, alpha: float
) -> float:
    """
    Computes a constant which defines a constraint in the convex
    optimization program for finding confidence intervals over
    individual parameters.

    Parameters
    ----------
    y : List[int]
        Cumulative counts of visitors assigned to each arm.
    dirichlet_alpha : np.ndarray
        Concentration parameter of dirichlet distribution.
    alpha : float
        Frequentist type 1 error probability.

    Returns
    -------
    float
        Value which defines the feasible set i.e. returns the c in c <= sum y_i log p_i.
    """
    return (
        log_posterior_predictive(y, np.array(dirichlet_alpha))
        + np.log(alpha)
        - loggamma(y.sum() + 1)
        + loggamma(y + 1).sum()
    )


def multinomiallogpmf(x: List[int], n: int, p: List[float]):
    """
    Alternative implementation of multinomial.logpmf from scipy.stats.
    This is about 5x faster.

    Parameters
    ----------
    x : List[int]
        A list of observations e.g. [10,21,33].
    n : int
        The number of trials (equal to sum(x)).
    p : List[float]
        A list of probabilities which should sum to 1 e.g. [0.2, 0.4, 0.4].

    Returns
    -------
    float
        Probability mass function of a multinomial(n,p) pmf evaluated at x.
    """
    x = np.array(x)
    p = np.array(p)
    return gammaln(n + 1) + np.sum(xlogy(x, p) - gammaln(x + 1), axis=-1)
