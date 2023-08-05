import pandas as pd
from ovretl.loads_utils.calculate_single_load_total_quantities import (
    calculate_single_load_total_quantities,
)


def calculate_entity_loads(loads_df: pd.DataFrame, key: str):
    entity_loads = loads_df[~loads_df[key].isnull()]
    return (
        entity_loads.groupby(key)
        .sum()[["total_volume", "total_weight"]]
        .reset_index()
        .drop_duplicates(subset=[key])
    )


def calculate_shipments_propositions_loads(loads_df: pd.DataFrame):
    loads_df = loads_df.apply(calculate_single_load_total_quantities, axis=1)
    loads_df = loads_df.dropna(subset=["total_volume", "total_weight"])
    propositions_loads = calculate_entity_loads(loads_df=loads_df, key="proposition_id")
    shipments_loads = calculate_entity_loads(loads_df=loads_df, key="shipment_id")
    return pd.concat([propositions_loads, shipments_loads], sort=False)
