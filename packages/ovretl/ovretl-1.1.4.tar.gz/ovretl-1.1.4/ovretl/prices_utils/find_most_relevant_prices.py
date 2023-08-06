import pandas as pd

from typing import Optional


def find_prices_from_entity(
    entity_df: pd.DataFrame, prices_df: pd.DataFrame, entity_key_in_prices_df: str, entity_key_in_entity_df="id",
) -> Optional[pd.DataFrame]:
    if len(entity_df) > 0:
        entity_id = entity_df.loc[0, entity_key_in_entity_df]
        return prices_df[prices_df[entity_key_in_prices_df] == entity_id]
    return None


def find_most_relevant_prices_factory(
    prices_propositions_by_category_df: pd.DataFrame,
    final_checks_df: pd.DataFrame,
    prices_final_check_by_category_df: pd.DataFrame,
    billings_df: pd.DataFrame,
    prices_billings_by_category_df: pd.DataFrame,
):
    def find_most_relevant_prices(shipment_id: str, proposition_id: str, initial_proposition=False):
        if initial_proposition == True:
            final_checks_df_filtered = final_checks_df[final_checks_df["shipment_id"] == shipment_id].reset_index(
                drop=True
            )
            prices_initial_proposition_filtered = find_prices_from_entity(
                entity_df=final_checks_df_filtered,
                prices_df=prices_propositions_by_category_df,
                entity_key_in_prices_df="proposition_id",
                entity_key_in_entity_df="initial_proposition_id",
            )
            if prices_initial_proposition_filtered is not None and len(prices_initial_proposition_filtered) > 0:
                return prices_initial_proposition_filtered

        billings_df_filtered = billings_df[billings_df["shipment_id"] == shipment_id].reset_index(drop=True)
        prices_billings_filtered = find_prices_from_entity(
            entity_df=billings_df_filtered,
            prices_df=prices_billings_by_category_df,
            entity_key_in_prices_df="billing_id",
        )
        if prices_billings_filtered is not None and len(prices_billings_filtered) > 0:
            return prices_billings_filtered

        final_checks_df_filtered = final_checks_df[final_checks_df["shipment_id"] == shipment_id].reset_index(drop=True)
        prices_final_check_filtered = find_prices_from_entity(
            entity_df=final_checks_df_filtered,
            prices_df=prices_final_check_by_category_df,
            entity_key_in_prices_df="final_check_id",
        )
        if prices_final_check_filtered is not None and len(prices_final_check_filtered) > 0:
            return prices_final_check_filtered

        if not pd.isna(proposition_id):
            return prices_propositions_by_category_df[
                prices_propositions_by_category_df["proposition_id"] == proposition_id
            ]
        return None

    return find_most_relevant_prices
