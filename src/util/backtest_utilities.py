#type: ignore
from typing import Tuple

import numpy as np
import numpy.typing as npt
import pandas as pd





def CheckValidReblance(DATA_NP, INDEX, MINDays, MINFunds, delay):
    counter = 0
    cols = DATA_NP.shape[1]
    for iCol in range(cols):
        if not np.isnan(DATA_NP[INDEX - delay, iCol]) and not np.isnan(DATA_NP[INDEX - delay - MINDays + 1, iCol]):
            counter += 1
    if counter >= MINFunds:
        return True
    return False


def GetReblanceIndexes(DATA_NP, DAYS, REBALANCEFrequency, MINDays=252, MINFunds=1, DELAY=1, ISEndMQHY=False):
    rows = DATA_NP.shape[0]
    reblanceIndexes = []

    delay = DELAY
    if ISEndMQHY and REBALANCEFrequency.upper() != "D":
        delay += 1

    for i in range(MINDays - 1 + delay, rows):
        index = i
        if ISEndMQHY:
            index -= 1

        if REBALANCEFrequency.upper() == "D":
            if CheckValidReblance(DATA_NP, i, MINDays, MINFunds, DELAY):
                reblanceIndexes.append(i)

        elif (REBALANCEFrequency.upper() == "W") and (
            pd.to_datetime(DAYS[i - 1]).isocalendar()[1] != pd.to_datetime(DAYS[i]).isocalendar()[1]
        ):
            if CheckValidReblance(DATA_NP, i, MINDays, MINFunds, delay):
                reblanceIndexes.append(index)

        elif (REBALANCEFrequency.upper() == "M") and (
            pd.to_datetime(DAYS[i - 1]).month != pd.to_datetime(DAYS[i]).month
        ):
            if CheckValidReblance(DATA_NP, i, MINDays, MINFunds, delay):
                reblanceIndexes.append(index)

        elif (REBALANCEFrequency.upper() == "Q") and (
            (pd.to_datetime(DAYS[i - 1]).month == 12 and pd.to_datetime(DAYS[i]).month == 1)
            or (pd.to_datetime(DAYS[i - 1]).month == 3 and pd.to_datetime(DAYS[i]).month == 4)
            or (pd.to_datetime(DAYS[i - 1]).month == 6 and pd.to_datetime(DAYS[i]).month == 7)
            or (pd.to_datetime(DAYS[i - 1]).month == 9 and pd.to_datetime(DAYS[i]).month == 10)
        ):
            if CheckValidReblance(DATA_NP, i, MINDays, MINFunds, delay):
                reblanceIndexes.append(index)

        elif (REBALANCEFrequency.upper() == "H") and (
            (pd.to_datetime(DAYS[i - 1]).month == 12 and pd.to_datetime(DAYS[i]).month == 1)
            or (pd.to_datetime(DAYS[i - 1]).month == 6 and pd.to_datetime(DAYS[i]).month == 7)
        ):
            if CheckValidReblance(DATA_NP, i, MINDays, MINFunds, delay):
                reblanceIndexes.append(index)

        elif (REBALANCEFrequency.upper() == "Y") and (pd.to_datetime(DAYS[i - 1]).year != pd.to_datetime(DAYS[i]).year):
            if CheckValidReblance(DATA_NP, i, MINDays, MINFunds, delay):
                reblanceIndexes.append(index)

    if (rows - 1) not in reblanceIndexes:
        reblanceIndexes.append(rows - 1)

    return np.array(reblanceIndexes, dtype=np.int64)

def GetBacktestReturns(DATA, ALLOCATIONS, REBALANCES, CASHRate):
    rows = DATA.shape[0]
    cols = DATA.shape[1]
    numberOfReblances = ALLOCATIONS.shape[0]

    if rows != CASHRate.shape[0]:
        raise ValueError("Cash Rate Data Points Are Not Equal.")

    backTestRORs = np.zeros(rows, dtype=np.float64)
    backTestRORs[:] = np.nan

    counter = 0
    capital = np.float64(100000)
    performanceRow = np.empty(cols + 1, dtype=np.float64)

    for iDay in range(REBALANCES[counter] + 1, rows):
        if counter < numberOfReblances and iDay - 1 == REBALANCES[counter]:
            performanceRow[:] = 0
            for iCol in range(cols):
                if (
                    not np.isnan(ALLOCATIONS[counter, iCol])
                    and ALLOCATIONS[counter, iCol] > 0.000001
                ):
                    performanceRow[iCol] = (
                        capital * ALLOCATIONS[counter, iCol] * (1 + DATA[iDay, iCol])
                    )
            if (
                not np.isnan(ALLOCATIONS[counter, cols])
                and ALLOCATIONS[counter, cols] > 0.000001
            ):
                performanceRow[cols] = (
                    capital * ALLOCATIONS[counter, cols] * (1 + CASHRate[iDay])
                )
            counter += 1
        else:
            for iCol in range(cols):
                if not np.isnan(DATA[iDay, iCol]):
                    performanceRow[iCol] = performanceRow[iCol] * (1 + DATA[iDay, iCol])
            performanceRow[cols] = performanceRow[cols] * (1 + CASHRate[iDay])

        backTestRORs[iDay] = (np.sum(performanceRow) / capital) - 1
        capital = np.sum(performanceRow)

    return backTestRORs