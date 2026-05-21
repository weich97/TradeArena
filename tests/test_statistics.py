from tradearena.evaluation.statistics import paired_bootstrap_difference, sample_std, summarize_metric


def test_summarize_metric_reports_mean_std_and_ci():
    summary = summarize_metric([0.01, 0.02, 0.03], prefix="return")

    assert summary["return_mean"] == 0.02
    assert round(float(summary["return_std"]), 6) == 0.01
    assert summary["return_ci_low"] is not None
    assert summary["return_ci_high"] is not None


def test_paired_bootstrap_difference_uses_matched_keys():
    result = paired_bootstrap_difference(
        {("calm", 1): 0.04, ("calm", 2): 0.03, ("other", 1): 0.01},
        {("calm", 1): 0.01, ("calm", 2): 0.02},
    )

    assert result["paired_n"] == 2
    assert round(float(result["mean_delta"]), 6) == 0.02
    assert result["p_value"] is not None


def test_sample_std_singleton_is_zero():
    assert sample_std([0.1]) == 0.0
