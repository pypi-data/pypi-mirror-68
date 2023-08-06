import warnings
from functools import reduce

import numpy as np
from pytest import approx
from scipy.stats import multinomial

from .ssrm_test import (
    bayes_factor,
    log_posterior_predictive,
    multinomiallogpmf,
    posterior_probability,
    sequential_posteriors,
    srm_test
)


def test_accumulator():
    """
    Tests that the posterior probability computed sequentially
    via accumulation is equal to the posterior probability
    computed in a batch manner.
    """
    theta = np.array([1 / 3, 1 / 3, 1 / 3])
    alpha = np.array([1, 3, 2])
    sample_size = 40
    observations = multinomial.rvs(1, theta, size=sample_size)
    observations_sum = reduce(lambda x, y: x + y, observations)
    final_posterior = sequential_posteriors(observations, theta, alpha)[-1]
    final_bf = bayes_factor(final_posterior)
    post_prob = posterior_probability(final_bf)
    log_marginal_likelihood_M1 = log_posterior_predictive(observations_sum, alpha)
    log_marginal_likelihood_M0 = multinomial.logpmf(
        observations_sum, observations_sum.sum(), theta
    )
    log_odds = log_marginal_likelihood_M1 - log_marginal_likelihood_M0
    odds = np.exp(log_odds)
    assert post_prob == approx(odds / (1 + odds))


def test_overflow():
    posterior = {
        "log_marginal_likelihood_M1": -23.585991739528254,
        "log_marginal_likelihood_M0": -76546.65811250894,
        "posterior_M1": [88519.5, 12540.25, 13002.25],
        "posterior_M0": [0.75, 0.125, 0.125],
    }
    # Assert there are no warnings in code exec
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        bf = bayes_factor(posterior)
        assert np.isinf(bf)
        assert posterior_probability(bf) == approx(1)
        assert len(w) == 0


def test_multinomiallogpmf():
    xs = [[10, 20, 30], [1, 1, 1], [0, 0, 1], [12, 30, 8]]
    ns = [sum(x) for x in xs]
    ps = [[0.2, 0.4, 0.4], [1 / 3, 1 / 3, 1 / 3], [0.3, 0.4, 0.3], [0, 0, 1]]
    for x, n, p in zip(xs, ns, ps):
        assert multinomial.logpmf(x, n, p) == approx(multinomiallogpmf(x, n, p))


def test_sequential_posteriors():
    # Testing unit-level data, where the counts across all variations are represented as one-hot vectors.
    expected_posteriors_dict = [
        {
            "log_marginal_likelihood_M1": -1.0986122886681096,
            "log_marginal_likelihood_M0": -0.916290731874155,
            "posterior_M1": np.array([2, 1, 1]),
            "posterior_M0": np.array([0.4, 0.4, 0.2]),
        },
        {
            "log_marginal_likelihood_M1": -2.4849066497880004,
            "log_marginal_likelihood_M0": -1.83258146374831,
            "posterior_M1": np.array([2, 2, 1]),
            "posterior_M0": np.array([0.4, 0.4, 0.2]),
        },
        {
            "log_marginal_likelihood_M1": -3.401197381662155,
            "log_marginal_likelihood_M0": -2.748872195622465,
            "posterior_M1": np.array([3, 2, 1]),
            "posterior_M0": np.array([0.4, 0.4, 0.2]),
        },
        {
            "log_marginal_likelihood_M1": -4.499809670330265,
            "log_marginal_likelihood_M0": -3.66516292749662,
            "posterior_M1": np.array([3, 3, 1]),
            "posterior_M0": np.array([0.4, 0.4, 0.2]),
        },
        {
            "log_marginal_likelihood_M1": -6.4457198193855785,
            "log_marginal_likelihood_M0": -5.27460083993072,
            "posterior_M1": np.array([3, 3, 2]),
            "posterior_M0": np.array([0.4, 0.4, 0.2]),
        },
    ]
    datapoints = np.array([[1, 0, 0], [0, 1, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    null_probabilities = np.array([0.4, 0.4, 0.2])
    posteriors_dict = sequential_posteriors(datapoints, null_probabilities)
    assert len(posteriors_dict) == len(datapoints)
    for acc_dict, expected_acc_dict in zip(posteriors_dict, expected_posteriors_dict):
        assert acc_dict["log_marginal_likelihood_M1"] == approx(
            expected_acc_dict["log_marginal_likelihood_M1"]
        )
        assert acc_dict["log_marginal_likelihood_M0"] == approx(
            expected_acc_dict["log_marginal_likelihood_M0"]
        )
        assert acc_dict["posterior_M1"] == approx(expected_acc_dict["posterior_M1"])
        assert acc_dict["posterior_M0"] == approx(expected_acc_dict["posterior_M0"])

    # Testing time-aggregated data, where each entry represents an aggregate count across all variations for that time.
    datapoints = np.array([[20, 17, 9], [18, 21, 8], [4, 6, 4], [18, 19, 11]])
    null_probabilities = np.array([0.4, 0.4, 0.2])
    posteriors_dict = sequential_posteriors(datapoints, null_probabilities)
    expected_posteriors_dict = [
        {
            "log_marginal_likelihood_M1": -7.028201432058012,
            "log_marginal_likelihood_M0": -4.0776406466061985,
            "posterior_M1": np.array([21, 18, 10]),
            "posterior_M0": np.array([0.4, 0.4, 0.2]),
        },
        {
            "log_marginal_likelihood_M1": -11.947847738358888,
            "log_marginal_likelihood_M0": -8.265946861099877,
            "posterior_M1": np.array([39, 39, 18]),
            "posterior_M0": np.array([0.4, 0.4, 0.2]),
        },
        {
            "log_marginal_likelihood_M1": -15.471401950257842,
            "log_marginal_likelihood_M0": -11.610743519545139,
            "posterior_M1": np.array([43, 45, 22]),
            "posterior_M0": np.array([0.4, 0.4, 0.2]),
        },
        {
            "log_marginal_likelihood_M1": -19.96484521090386,
            "log_marginal_likelihood_M0": -15.781031228536165,
            "posterior_M1": np.array([61, 64, 33]),
            "posterior_M0": np.array([0.4, 0.4, 0.2]),
        },
    ]
    assert len(posteriors_dict) == len(datapoints)
    for acc_dict, expected_acc_dict in zip(posteriors_dict, expected_posteriors_dict):
        assert acc_dict["log_marginal_likelihood_M1"] == approx(
            expected_acc_dict["log_marginal_likelihood_M1"]
        )
        assert acc_dict["log_marginal_likelihood_M0"] == approx(
            expected_acc_dict["log_marginal_likelihood_M0"]
        )
        assert acc_dict["posterior_M1"] == approx(expected_acc_dict["posterior_M1"])
        assert acc_dict["posterior_M0"] == approx(expected_acc_dict["posterior_M0"])


def test_srm_test():
    # Testing unit-level data, where the counts across all variations are represented as one-hot vectors.
    datapoints = np.array([[1, 0, 0], [0, 1, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    null_probabilities = np.array([0.4, 0.4, 0.2])
    mismatch_prob = srm_test(datapoints, null_probabilities)
    assert mismatch_prob >= 0 and mismatch_prob <= 1

    # Testing time-aggregated data, where each entry represents an aggregate count across all variations for that time.
    datapoints = np.array([[20, 17, 9], [18, 21, 8], [4, 6, 4], [18, 19, 11]])
    null_probabilities = np.array([0.4, 0.4, 0.2])
    mismatch_prob = srm_test(datapoints, null_probabilities)
    assert mismatch_prob >= 0 and mismatch_prob <= 1
