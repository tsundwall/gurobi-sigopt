## Sigmoidal Programming Wrapper for Gurobipy Python Package

### Provides quick setup for modeling 'sum of sigmoid' problems in the Gurobi interface

Typically, this problem is modeled as:

$$\underset{x}{max} \; f_i(x_i)$$

$$s.t. \; Ax = b$$
$$\;\;\;\;\;\; Cx \leq d$$

Where we parameterize each $f_i$ as a continuouos sigmoidal function:

$$f_i =\frac{\mu_i}{1+e^{\lambda_i-\theta_ix_i}}$$

In Gurobi, several of these operations cannot be traditionally implemented, but we can reformulate this as an epigraph problem:
```math
$$\underset{t_1,...,t_n \in t}{max} \; t$$

$$ \; x^n_i = -\theta_i x_i + \lambda_i \; \forall i$$
$$\; x^e_i = \hat{e}^{x^n_i} \; \forall i$$
$$\; t_i \leq \mu_i z_i \; \forall i$$
$$ \; z_i(1+x^e_i) = 1 \;  $$
```

$$\; Ax = b$$
$$\; Cx \leq d$$

$\hat{e}$ indicates the piecewise linear bound approximation of the natural exponent.

Note that as $n$ increases, it becomes apparent that Gurobi's general non-convex solver performs poorly on sigmoidal programming problems compared to the specific methods proposed by Boyd (Python and Julia implementations of their method are implemented).
