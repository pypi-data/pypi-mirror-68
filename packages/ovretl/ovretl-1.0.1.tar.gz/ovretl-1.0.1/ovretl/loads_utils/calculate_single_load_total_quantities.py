import pandas as pd


def calculate_single_load_total_weight(single_load):
    return single_load["unit_weight"] * single_load["unit_number"]


def calculate_single_load_total_volume(single_load):
    return (
        single_load["unit_length"]
        * single_load["unit_width"]
        * single_load["unit_height"]
        * single_load["unit_number"]
        / 1000000
    )


def calculate_single_load_total_quantities(single_load: pd.Series):
    single_load["total_weight"] = (
        single_load["total_weight"]
        if not pd.isna(single_load["total_weight"])
        else calculate_single_load_total_weight(single_load)
    )
    single_load["total_volume"] = (
        single_load["total_volume"]
        if not pd.isna(single_load["total_volume"])
        else calculate_single_load_total_volume(single_load)
    )
    return single_load
