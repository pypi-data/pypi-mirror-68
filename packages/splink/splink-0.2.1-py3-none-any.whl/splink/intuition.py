from .chart_definitions import adjustment_factor_chart_def
from .params import Params

altair_installed = True
try:
    import altair as alt
except ImportError:
    altair_installed = False


initial_template = """
Initial probability of match (prior) = λ = {lam}
"""

col_template = """
Comparison of {col_name}.  Values are:
{col_name}_l: {value_l}
{col_name}_r: {value_r}
Comparison has {num_levels} levels
𝛾 for this comparison = {gamma_col_name} = {gamma_value}
Amongst matches, P(𝛾 = {prob_m}):
Amongst non matches, P(𝛾 = {prob_nm}):
Adjustment factor = p1/(p1 + p2) = {adj}
New probability of match (updated belief): {updated_belief}
"""

end_template = """
Final probability of match = {final}
"""


def intuition_report(row_dict:dict, params:Params):
    """Generate a text summary of a row in the comparison table which explains how the match_probability was computed

    Args:
        row_dict (dict): A python dictionary representing the comparison row
        params (Params): splink params object

    Returns:
        string: The intuition report
    """

    pi = params.params["π"]
    lam = params.params["λ"]

    report = initial_template.format(lam=lam)

    gamma_keys = pi.keys() # gamma_0, gamma_1 etc.

    # Create dictionary to fill in template
    d = {}
    d["current_p"] = lam

    for gk in gamma_keys:

        col_params = pi[gk]

        d["col_name"] = col_params["column_name"]
        col_name = d["col_name"]
        if pi[gk]["custom_comparison"] == False:
            d["value_l"] = row_dict[col_name + "_l"]
            d["value_r"] = row_dict[col_name + "_r"]
        else:
            d["value_l"] = ", ".join([str(row_dict[c + "_l"]) for c in pi[gk]["custom_columns_used"] ])
            d["value_r"] = ", ".join([str(row_dict[c + "_r"]) for c in pi[gk]["custom_columns_used"] ])
        d["num_levels"] = col_params["num_levels"]

        d["gamma_col_name"] = gk
        d["gamma_value"] = row_dict[gk]

        d["prob_m"] = float(row_dict[f"prob_{gk}_match"])
        d["prob_nm"] = float(row_dict[f"prob_{gk}_non_match"])

        d["adj"] = d["prob_m"]/(d["prob_m"] + d["prob_nm"])

        # Update beleif
        adj = d["adj"]
        current_prob = d["current_p"]

        a = adj*current_prob
        b = (1-adj) * (1-current_prob)
        new_p = a/(a+b)
        d["updated_belief"] = new_p
        d["current_p"] = new_p

        col_report = col_template.format(**d)

        report += col_report

    report += end_template.format(final=new_p)

    return report

def _get_adjustment_factors(row_dict, params):

    pi = params.params["π"]

    gamma_keys = pi.keys() # gamma_0, gamma_1 etc.

    adjustment_factors  = []


    for gk in gamma_keys:

        col_params = pi[gk]

        col_name = col_params["column_name"]

        prob_m = float(row_dict[f"prob_{gk}_match"])
        prob_nm = float(row_dict[f"prob_{gk}_non_match"])

        adj = prob_m/(prob_m + prob_nm)

        adjustment_factors.append({"gamma": gk,"col_name": col_name, "value": adj, "normalised": adj-0.5})

    return adjustment_factors

def adjustment_factor_chart(row_dict, params):

    adjustment_factor_chart_def["data"]["values"] = _get_adjustment_factors(row_dict, params)

    if altair_installed:
        return alt.Chart.from_dict(adjustment_factor_chart_def)
    else:
        return adjustment_factor_chart_def

