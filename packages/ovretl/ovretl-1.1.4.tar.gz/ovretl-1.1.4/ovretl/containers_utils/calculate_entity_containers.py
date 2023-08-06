import pandas as pd
from ovretl.containers_utils.calculate_single_container_teus import (
    calculate_single_container_teus,
)


def calculate_entity_containers(containers_df: pd.DataFrame, key: str):
    entity_containers = containers_df[~containers_df[key].isnull()]
    return (
        entity_containers.groupby(key)["teus"]
        .agg(["sum", "count"])
        .rename(columns={"sum": "teus", "count": "tc"})
        .reset_index()
        .drop_duplicates(subset=[key])
    )


def calculate_shipments_propositions_containers(containers_df: pd.DataFrame):
    containers_df = containers_df.apply(calculate_single_container_teus, axis=1)
    containers_df = containers_df.dropna(subset=["teus"])
    propositions_containers = calculate_entity_containers(
        containers_df=containers_df, key="proposition_id"
    )
    shipments_containers = calculate_entity_containers(
        containers_df=containers_df, key="shipment_id"
    )
    return pd.concat([propositions_containers, shipments_containers], sort=False)
