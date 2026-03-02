import numpy as np
from mds.bo import fit_gp, suggest_next


def test_suggest_next_within_bounds():
    rng = np.random.default_rng(0)
    bounds = np.array([[0.0, 1.0], [0.0, 2.0]])
    X = rng.uniform(bounds[:,0], bounds[:,1], size=(12, 2))
    y = (X[:,0] - 0.3)**2 + (X[:,1] - 1.2)**2 + rng.normal(0, 0.01, size=12)

    gp = fit_gp(X, y)
    x_next, meta = suggest_next(bounds, gp, y_best=float(np.min(y)), n_candidates=500, xi=0.01, random_state=1)

    assert x_next.shape == (2,)
    assert bounds[0,0] <= x_next[0] <= bounds[0,1]
    assert bounds[1,0] <= x_next[1] <= bounds[1,1]
    assert "predicted_mean" in meta and "predicted_std" in meta
