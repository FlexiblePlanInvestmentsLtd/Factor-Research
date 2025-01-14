#type: ignore
import pandas as pd
import numpy as np

def RETURN(DATA):
    n = DATA.shape[0]
    roC = 1
    for i in range(n):
        roC *= 1 + DATA[i]
    return roC - 1


def CAGR(DATA, DAYS):
    n = DATA.shape[0]
    oneOverYears = DAYS / n
    return (RETURN(DATA) + 1) ** oneOverYears - 1


def RISK(DATA, DAYS):
    return np.std(DATA) * DAYS**0.5


def SHARPE(DATA, RISK_FREE_RATE, DAYS):
    return (CAGR(DATA, DAYS) - RISK_FREE_RATE) / RISK(DATA, DAYS)

def MAXDD(DATA):
    n = DATA.shape[0]

    roC = 1
    maxDD = 0
    maxRoC = roC

    for i in range(n):
        roC *= 1 + DATA[i]
        if maxRoC < roC:
            maxRoC = roC
        dD = 1 - (roC / maxRoC)
        if dD > maxDD:
            maxDD = dD

    return maxDD


def MAR(DATA, DAYS):
    return CAGR(DATA, DAYS) / MAXDD(DATA)

def get_data_frame_mpt_statistics(
    df_rors: pd.DataFrame, frequency_per_year: int = 252
) -> pd.DataFrame:
    """This method will output data frame MPT statistics with yearly returns.

    Args:
        df_rors (pd.DataFrame): Pandas data frame with historical rate of returns. The row index should be the trade days and the columns should be the fund symbols.
        frequency_per_year (int, optional): Historical data frequency. Use 252 for daily, 63 for quarterly, 12 for monthly and 1 for yearly. Defaults to 252.

    Returns:
        pd.DataFrame: Fund start and end days, historical MPT statistics (Return|CAGR|Risk|Sharpe|MaxDD|MAR) and yearly returns for each fund.
    """
    data = df_rors.dropna(axis=1, how="all").copy()
    r = len(data.index)
    c = len(data.columns)
    days = pd.to_datetime(data.index)

    row_indices = ["Return", "CAGR", "Risk", "Sharpe", "MaxDD", "MAR"]
    year_end_indices = []
    for i_day in range(1, r):
        if days[i_day].year != days[i_day - 1].year:
            year_end_indices.append(i_day - 1)
            row_indices.append(str(days[i_day - 1].year))
    year_end_indices.append(r - 1)
    row_indices.append(str(days[r - 1]))

    # Indices: 0-Return | 1 - CAGR | 2 - Risk | 3 - Sharpe | 4 - MaxDD | 5 - MAR | 6 and Up - Yearly Returns
    np_mpt_statistics = np.full(
        (c, 6 + len(year_end_indices)), np.nan, dtype=np.float64
    )

    np_data = data.to_numpy()
    for i_col in range(c):
        rors = np_data[:, i_col]
        rors = rors[~np.isnan(rors)]
        if rors.shape[0] > 1:
            np_mpt_statistics[i_col, 0] = RETURN(rors)
            np_mpt_statistics[i_col, 1] = CAGR(
                rors, frequency_per_year
            )
            np_mpt_statistics[i_col, 2] = RISK(
                rors, frequency_per_year
            )
            np_mpt_statistics[i_col, 3] = SHARPE(
                rors, 0.0, frequency_per_year
            )
            np_mpt_statistics[i_col, 4] = MAXDD(rors)
            np_mpt_statistics[i_col, 5] = MAR(
                rors, frequency_per_year
            )
            st_year_end_index = 0
            for i, i_idx_year_end in enumerate(year_end_indices):
                rors_sub = np_data[st_year_end_index : i_idx_year_end + 1, i_col]
                rors_sub = rors_sub[~np.isnan(rors_sub)]
                if rors_sub.shape[0] > 1:
                    np_mpt_statistics[i_col, 6 + i] = RETURN(
                        rors_sub
                    )
                st_year_end_index = i_idx_year_end + 1

    df_mpt_statistics = pd.DataFrame(
        np_mpt_statistics.T, columns=data.columns, index=row_indices
    )
    df_mpt_statistics = df_mpt_statistics.T
    df_mpt_statistics.insert(0, "ED Date", data.apply(pd.Series.last_valid_index))
    df_mpt_statistics.insert(0, "ST Date", data.apply(pd.Series.first_valid_index))

    return df_mpt_statistics.T
