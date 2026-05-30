from chemloop_studio.experiment import FEATURE_COLUMNS, load_experiments, recommend_next_experiment


def test_recommend_next_experiment_returns_candidate():
    frame = load_experiments()
    recommendation = recommend_next_experiment(frame)
    assert recommendation.experiment_id.startswith("CAND-")
    assert recommendation.predicted_score >= 0
    assert set(recommendation.variables) == set(FEATURE_COLUMNS)
