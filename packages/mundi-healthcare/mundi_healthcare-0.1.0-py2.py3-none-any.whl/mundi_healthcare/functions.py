import sys
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Union, Tuple

import mundi
import pandas as pd

ModRef = Union[str, ModuleType]


def hospital_capacity(df):
    return capacity(df)["hospital_capacity"]


def hospital_capacity_public(df):
    return capacity(df)["hospital_capacity_public"]


def icu_capacity(df):
    return capacity(df)["icu_capacity"]


def icu_capacity_public(df):
    return capacity(df)["icu_capacity_public"]


def capacity(df):
    """
    Return total capacity
    """
    data, is_row = loader("mundi_healthcare", "capacity", df)
    return data


def loader(package: ModRef, db_name, idx) -> Tuple[pd.DataFrame, bool]:
    """
    Load distribution from package.

    Return a tuple of (Data, is_row). The boolean "is_row" tells
    the returned data concerns a collection of items or a single row in the
    database.
    """

    db = database(package, db_name + ".pkl.gz")

    if isinstance(idx, (pd.DataFrame, pd.Series)):
        idx = idx.index
    elif isinstance(idx, str):
        idx = mundi.code(idx)
        df, _ = loader(package, db_name, [idx])
        return df.iloc[0], True

    # Try to get from index
    reindex = db.reindex(idx)
    return reindex, False


@lru_cache(32)
def database(package, name):
    """Lazily load db from name"""

    if isinstance(package, str):
        package = sys.modules[package]
    path = Path(package.__file__).parent.absolute()
    db_path = path / "databases" / name
    return pd.read_pickle(db_path)
