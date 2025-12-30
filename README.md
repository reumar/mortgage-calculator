# Fixed Rate Mortgage Calculator

Mortgage information for a given loan principal, annual fixed interest rate and number of years.

The payment schedule follows the **French amortization system**, in which the monthly payment $M$ is given by

$$
M = P \cdot \dfrac{i(1+i)^{n}}{(1+i)^{n}-1}
$$

where:
- $P$ is the loan principal,
- $i$ is the monthly interest rate,
- $n$ is the total number of monthly payments.

## Install dependencies

```bash
uv sync
```

## Run the notebook

```bash
uv run marimo run main.py
```

## Edit the notebook

```bash
uv run marimo edit main.py
```