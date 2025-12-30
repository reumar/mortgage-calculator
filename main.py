import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    # Imports
    import pandas as pd
    import numpy as np
    import altair as alt

    return alt, pd


@app.cell
def _(pd):
    # Functions
    def mortgage_schedule(loan: int, annual_rate: float, years: int) -> pd.DataFrame:
        monthly_rate = annual_rate / (12 * 100)
        n = years * 12
        payment = (
            loan
            * (monthly_rate * (1 + monthly_rate) ** n)
            / ((1 + monthly_rate) ** n - 1)
        )
        payment = round(payment, 2)

        balance = round(loan, 2)
        schedule = []

        for month in range(1, n + 1):
            interest = round(balance * monthly_rate, 2)
            principal = round(payment - interest, 2)

            # Last month adjustment
            if month == n:
                principal = balance
                payment = round(principal + interest, 2)

            balance = round(balance - principal, 2)

            schedule.append(
                {
                    "Month": month,
                    "Payment": payment,
                    "Interest": interest,
                    "Principal": principal,
                    "Remaining Balance": balance,
                }
            )

        return pd.DataFrame(schedule)

    return (mortgage_schedule,)


@app.cell
def _(mo):
    mo.md(r"""
    # Fixed Rate Mortgage Calculator
    """)
    return


@app.cell
def _(mo):
    data = mo.md("<br>{loan} {interest} {years}<br>").batch(
        loan=mo.ui.number(
            start=80000, stop=1000000, step=1000, label="**Loan Amount**:\t"
        ),
        years=mo.ui.number(start=15, stop=30, step=1, label="**Years**:\t"),
        interest=mo.ui.number(
            start=0.01,
            stop=20,
            step=0.01,
            label="**Annual Interest Rate**:\t",
            value=2.0,
        ),
    )
    data
    return (data,)


@app.cell
def _(mo):
    mo.md(r"""
    ## General statistics
    """)
    return


@app.cell
def _(df, mo):
    mo.hstack(
        [
            mo.stat(
                label="Amount to pay back",
                value="{:,.2f}€".format(df["Payment"].sum()),
                bordered=True,
            ),
            mo.stat(
                label="Interest to pay back",
                value="{:,.2f}€".format(df["Interest"].sum()),
                bordered=True,
            ),
        ],
        widths="equal",
        gap=1,
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Amortization Schedule

    The schedule follows the **French amortization system**, in which the monthly payment $M$ is given by

    $$
    M = P \cdot \dfrac{i(1+i)^{n}}{(1+i)^{n}-1}
    $$

    where:
    - $P$ is the loan principal,
    - $i$ is the monthly interest rate,
    - $n$ is the total number of monthly payments.
    """)
    return


@app.cell
def _(data, mo, mortgage_schedule):
    df = mortgage_schedule(
        annual_rate=data.value["interest"],
        loan=data.value["loan"],
        years=data.value["years"],
    )

    mo.ui.table(
        df,
        page_size=12,
        show_column_summaries=False,
        show_data_types=False,
        selection=None,
        freeze_columns_left=["Month"],
    )
    return (df,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Interest and Principal paid over time
    """)
    return


@app.cell
def _(alt, data, df, mo):
    _chart1 = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X(
                "Month:Q",
                axis=alt.Axis(title="Month", titleFontSize=16, labelFontSize=13),
                scale=alt.Scale(domain=[0, data.value["years"] * 12]),
            ),
            y=alt.Y(
                "Interest:Q",
                axis=alt.Axis(
                    title="Interest (€)",
                    titleColor="#1f77b4",
                    titleFontSize=16,
                    labelFontSize=13,
                ),
            ),
            color=alt.value("#1f77b4"),
        )
    )
    _chart2 = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("Month:Q", scale=alt.Scale(domain=[0, data.value["years"] * 12])),
            y=alt.Y(
                "Principal:Q",
                axis=alt.Axis(
                    title="Principal (€)",
                    titleColor="#ff7f0e",
                    labelFontSize=13,
                    titleFontSize=16,
                ),
            ),
            color=alt.value("#ff7f0e"),
        )
    )

    _chart = alt.layer(_chart1, _chart2).resolve_scale(y="independent")
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Cumulative Interest and Principal paid over time
    """)
    return


@app.cell
def _(alt, data, df, mo, pd):
    _tmp = df.loc[:, ["Month", "Principal", "Interest"]].assign(
        Principal=lambda _: _["Principal"].cumsum(),
        Interest=lambda _: _["Interest"].cumsum(),
    )
    _tmp = pd.melt(_tmp, id_vars="Month")

    _chart = (
        alt.Chart(_tmp)
        .mark_line()
        .encode(
            x=alt.X(
                "Month:Q",
                axis=alt.Axis(title="Month", titleFontSize=16, labelFontSize=13),
                scale=alt.Scale(domain=[0, data.value["years"] * 12]),
            ),
            y=alt.Y(
                "value:Q",
                axis=alt.Axis(
                    title="€",
                    titleFontSize=16,
                    labelFontSize=13,
                    titleAngle=0,
                    titleX=-70,
                ),
            ),
            color=alt.Color(
                "variable:N",
                title="",
                legend=alt.Legend(labelFontSize=13),
                scale=alt.Scale(
                    domain=["Principal", "Interest"], range=["#ff7f0e", "#1f77b4"]
                ),
            ),
        )
    )

    mo.ui.altair_chart(_chart)
    return


if __name__ == "__main__":
    app.run()
