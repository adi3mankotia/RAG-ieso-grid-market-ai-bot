import inspect
from typing import Any

import pandas as pd
from gridstatus import IESO


ieso = IESO()


IESO_METHOD_CATALOG = {
    "forecast_surplus_baseload_generation": {
        "method": "get_forecast_surplus_baseload_generation",
        "description": "Forecast surplus baseload generation, surplus state, actions, export forecast, and minimum generation status.",
    },
    "fuel_mix": {
        "method": "get_fuel_mix",
        "description": "Hourly output and capability for each fuel type, summed over all generators.",
    },
    "generator_report_hourly": {
        "method": "get_generator_report_hourly",
        "description": "Hourly output for each generator, including capability or available capacity.",
    },
    "hoep_historical_hourly": {
        "method": "get_hoep_historical_hourly",
        "description": "Historical hourly Ontario energy price data. Mostly legacy/older market data.",
    },
    "hoep_real_time_hourly": {
        "method": "get_hoep_real_time_hourly",
        "description": "Real-time hourly Ontario energy price data. Mostly legacy/older market data.",
    },
    "in_service_transmission_limits": {
        "method": "get_in_service_transmission_limits",
        "description": "Transmission limits for in-service transmission elements.",
    },
    "intertie_actual_schedule_flow_hourly": {
        "method": "get_intertie_actual_schedule_flow_hourly",
        "description": "Hourly actual scheduled flow on interties.",
    },
    "intertie_flow_5_min": {
        "method": "get_intertie_flow_5_min",
        "description": "5-minute intertie flow data.",
    },
    "intertie_limits_day_ahead_hourly": {
        "method": "get_intertie_limits_day_ahead_hourly",
        "description": "Day-ahead intertie scheduling limits.",
    },
    "intertie_limits_real_time_5_min": {
        "method": "get_intertie_limits_real_time_5_min",
        "description": "Real-time 5-minute intertie scheduling limits.",
    },
    "lmp_day_ahead_hourly": {
        "method": "get_lmp_day_ahead_hourly",
        "description": "Day-ahead LMP data.",
    },
    "lmp_day_ahead_hourly_intertie": {
        "method": "get_lmp_day_ahead_hourly_intertie",
        "description": "Day-ahead hourly intertie LMP data.",
    },
    "lmp_day_ahead_hourly_ontario_zonal": {
        "method": "get_lmp_day_ahead_hourly_ontario_zonal",
        "description": "Day-ahead hourly Ontario zonal price data.",
    },
    "lmp_day_ahead_hourly_virtual_zonal": {
        "method": "get_lmp_day_ahead_hourly_virtual_zonal",
        "description": "Day-ahead hourly virtual zonal LMP data.",
    },
    "lmp_day_ahead_operating_reserves": {
        "method": "get_lmp_day_ahead_operating_reserves",
        "description": "Day-ahead operating reserve LMP data.",
    },
    "lmp_predispatch_hourly": {
        "method": "get_lmp_predispatch_hourly",
        "description": "Predispatch hourly LMP data.",
    },
    "lmp_predispatch_hourly_intertie": {
        "method": "get_lmp_predispatch_hourly_intertie",
        "description": "Predispatch hourly intertie LMP data.",
    },
    "lmp_predispatch_hourly_ontario_zonal": {
        "method": "get_lmp_predispatch_hourly_ontario_zonal",
        "description": "Predispatch hourly Ontario zonal price data.",
    },
    "lmp_predispatch_hourly_virtual_zonal": {
        "method": "get_lmp_predispatch_hourly_virtual_zonal",
        "description": "Predispatch hourly virtual zonal LMP data.",
    },
    "lmp_real_time_5_min": {
        "method": "get_lmp_real_time_5_min",
        "description": "Real-time 5-minute LMP data.",
    },
    "lmp_real_time_5_min_intertie": {
        "method": "get_lmp_real_time_5_min_intertie",
        "description": "Real-time 5-minute intertie LMP data.",
    },
    "lmp_real_time_5_min_ontario_zonal": {
        "method": "get_lmp_real_time_5_min_ontario_zonal",
        "description": "Real-time 5-minute Ontario zonal price data.",
    },
    "lmp_real_time_5_min_virtual_zonal": {
        "method": "get_lmp_real_time_5_min_virtual_zonal",
        "description": "Real-time 5-minute virtual zonal LMP data.",
    },
    "lmp_real_time_operating_reserves": {
        "method": "get_lmp_real_time_operating_reserves",
        "description": "Real-time operating reserve LMP data.",
    },
    "load": {
        "method": "get_load",
        "description": "5-minute load for Market and Ontario. May be legacy/less reliable after IESO Market Renewal.",
    },
    "load_forecast": {
        "method": "get_load_forecast",
        "description": "Forecasted load for Ontario.",
    },
    "load_zonal_5_min": {
        "method": "get_load_zonal_5_min",
        "description": "5-minute zonal load data.",
    },
    "load_zonal_hourly": {
        "method": "get_load_zonal_hourly",
        "description": "Hourly zonal load data.",
    },
    "mcp_historical_5_min": {
        "method": "get_mcp_historical_5_min",
        "description": "Historical 5-minute market clearing price data.",
    },
    "mcp_real_time_5_min": {
        "method": "get_mcp_real_time_5_min",
        "description": "Real-time 5-minute market clearing price data.",
    },
    "outage_transmission_limits": {
        "method": "get_outage_transmission_limits",
        "description": "Transmission limits related to outages.",
    },
    "real_time_totals": {
        "method": "get_real_time_totals",
        "description": "Real-time totals such as Ontario demand, market demand, and operating reserve.",
    },
    "resource_adequacy_report": {
        "method": "get_resource_adequacy_report",
        "description": "Resource adequacy report data.",
    },
    "resource_adequacy_report_by_last_modified": {
        "method": "get_resource_adequacy_report_by_last_modified",
        "description": "Resource adequacy reports modified after a selected time.",
    },
    "shadow_prices_day_ahead_hourly": {
        "method": "get_shadow_prices_day_ahead_hourly",
        "description": "Day-ahead hourly shadow price data.",
    },
    "shadow_prices_real_time_5_min": {
        "method": "get_shadow_prices_real_time_5_min",
        "description": "Real-time 5-minute shadow price data.",
    },
    "solar_embedded_forecast": {
        "method": "get_solar_embedded_forecast",
        "description": "Embedded solar forecast.",
    },
    "solar_market_participant_forecast": {
        "method": "get_solar_market_participant_forecast",
        "description": "Market participant solar forecast.",
    },
    "transmission_outages_planned": {
        "method": "get_transmission_outages_planned",
        "description": "Planned transmission outages.",
    },
    "wind_embedded_forecast": {
        "method": "get_wind_embedded_forecast",
        "description": "Embedded wind forecast.",
    },
    "wind_market_participant_forecast": {
        "method": "get_wind_market_participant_forecast",
        "description": "Market participant wind forecast.",
    },
    "yearly_intertie_actual_schedule_flow_hourly": {
        "method": "get_yearly_intertie_actual_schedule_flow_hourly",
        "description": "Yearly intertie actual schedule flow hourly data.",
    },
    "zonal_load_forecast": {
        "method": "get_zonal_load_forecast",
        "description": "Forecasted load by forecast zone, such as Ontario, East, and West.",
    },
}


def list_available_ieso_functions() -> str:
    lines = ["Available GridStatus IESO functions:"]
    for key, item in IESO_METHOD_CATALOG.items():
        lines.append(f"- {key}: {item['description']}")
    return "\n".join(lines)


def _method_accepts_date(method: Any) -> bool:
    signature = inspect.signature(method)
    return "date" in signature.parameters


def _method_accepts_verbose(method: Any) -> bool:
    signature = inspect.signature(method)
    return "verbose" in signature.parameters


def _call_ieso_method(method_name: str, date: str = "latest") -> pd.DataFrame:
    if not hasattr(ieso, method_name):
        raise ValueError(f"IESO does not have method: {method_name}")

    method = getattr(ieso, method_name)
    kwargs = {}

    if _method_accepts_date(method):
        kwargs["date"] = date

    if _method_accepts_verbose(method):
        kwargs["verbose"] = False

    try:
        return method(**kwargs)

    except TypeError:
        if _method_accepts_date(method):
            return method(date)
        return method()

    except Exception as first_error:
        if date == "latest" and _method_accepts_date(method):
            try:
                kwargs["date"] = "today"
                return method(**kwargs)
            except Exception:
                pass

        raise first_error


def _safe_round(value, decimals: int = 2):
    if value is None or pd.isna(value):
        return "N/A"

    try:
        return round(float(value), decimals)
    except Exception:
        return value


def _latest_row(df: pd.DataFrame) -> pd.Series:
    if df is None or df.empty:
        raise ValueError("The DataFrame is empty.")
    return df.tail(1).iloc[0]


def _format_time_range(row: pd.Series) -> str:
    start = row.get("Interval Start", None)
    end = row.get("Interval End", None)

    if start is not None and end is not None:
        return f"{start} to {end}"

    if start is not None:
        return str(start)

    return "the latest available interval"


def _format_dataframe_result(df: pd.DataFrame, max_rows: int = 8) -> str:
    if df is None:
        return "The function returned no data."

    if not isinstance(df, pd.DataFrame):
        return f"The function returned: {df}"

    if df.empty:
        return "The function returned an empty DataFrame."

    lines = [
        f"Rows returned: {len(df)}",
        f"Columns: {list(df.columns)}",
        "",
        "Latest rows:",
        df.tail(max_rows).to_string(index=False),
    ]

    return "\n".join(lines)


def format_realtime_ontario_price(df: pd.DataFrame) -> str:
    if df is None or df.empty:
        return "I could not find real-time Ontario zonal price data."

    latest = _latest_row(df)
    time_range = _format_time_range(latest)

    lmp = latest.get("LMP", None)
    energy = latest.get("Energy", None)
    congestion = latest.get("Congestion", None)
    loss = latest.get("Loss", None)

    if lmp is None:
        return (
            "I found Ontario price data, but could not identify the LMP column.\n"
            f"Available columns: {list(df.columns)}"
        )

    answer = (
        f"The latest real-time Ontario zonal price is {_safe_round(lmp)} $/MWh "
        f"for {time_range}."
    )

    components = []
    if energy is not None:
        components.append(f"energy: {_safe_round(energy)} $/MWh")
    if congestion is not None:
        components.append(f"congestion: {_safe_round(congestion)} $/MWh")
    if loss is not None:
        components.append(f"loss: {_safe_round(loss)} $/MWh")

    if components:
        answer += "\n\nPrice components: " + ", ".join(components) + "."

    return answer


def format_day_ahead_ontario_price(df: pd.DataFrame) -> str:
    if df is None or df.empty:
        return "I could not find day-ahead Ontario zonal price data."

    rows = df.tail(6)

    lines = ["Latest available day-ahead Ontario zonal prices:"]
    for _, row in rows.iterrows():
        time_range = _format_time_range(row)
        lmp = row.get("LMP", row.get("Price", None))

        if lmp is not None:
            lines.append(f"- {time_range}: {_safe_round(lmp)} $/MWh")
        else:
            lines.append(f"- {time_range}: price column not found")

    return "\n".join(lines)


def format_real_time_totals(df: pd.DataFrame) -> str:
    """
    Current Ontario demand/load questions should use get_real_time_totals,
    not get_load.
    """
    if df is None or df.empty:
        return "I could not find IESO real-time totals data."

    latest = _latest_row(df)
    time_range = _format_time_range(latest)

    lines = [f"Latest IESO real-time totals for {time_range}:"]

    preferred_cols = [
        "Ontario Demand",
        "Market Demand",
        "Total Energy",
        "Total Energy Demand",
        "Operating Reserve",
        "Total Operating Reserve",
        "OR Requirement",
    ]

    found_any = False

    for col in preferred_cols:
        if col in df.columns:
            value = latest.get(col)
            if value is not None and pd.notna(value):
                lines.append(f"- {col}: {_safe_round(value)} MW")
                found_any = True

    if not found_any:
        lines.append("I found real-time totals data, but could not identify the standard demand columns.")
        lines.append(f"Available columns: {list(df.columns)}")
        lines.append("")
        lines.append("Latest row:")
        lines.append(latest.to_string())

    return "\n".join(lines)


def format_fuel_mix(df: pd.DataFrame) -> str:
    if df is None or df.empty:
        return "I could not find fuel mix data."

    latest = _latest_row(df)
    time_range = _format_time_range(latest)

    fuel_columns = [
        col
        for col in df.columns
        if col not in ["Interval Start", "Interval End"]
        and pd.api.types.is_numeric_dtype(df[col])
    ]

    if not fuel_columns:
        return (
            "I found fuel mix data, but could not identify fuel columns.\n"
            f"Available columns: {list(df.columns)}"
        )

    values = []
    for col in fuel_columns:
        value = latest.get(col)
        if value is not None and pd.notna(value):
            values.append((col, float(value)))

    values.sort(key=lambda x: x[1], reverse=True)

    lines = [f"Latest Ontario fuel mix for {time_range}:"]

    for fuel, value in values:
        lines.append(f"- {fuel}: {_safe_round(value)} MW")

    return "\n".join(lines)


def format_generator_report(df: pd.DataFrame, max_generators: int = 10) -> str:
    if df is None or df.empty:
        return "I could not find generator-level output data."

    if "Output MW" not in df.columns:
        return (
            "I found generator output data, but could not find the Output MW column.\n"
            f"Available columns: {list(df.columns)}"
        )

    latest_time = df["Interval Start"].max() if "Interval Start" in df.columns else None

    if latest_time is not None:
        latest_df = df[df["Interval Start"] == latest_time].copy()
    else:
        latest_df = df.copy()

    latest_df = latest_df.sort_values("Output MW", ascending=False).head(max_generators)

    lines = [f"Top {max_generators} generator outputs for {latest_time or 'latest interval'}:"]

    for _, row in latest_df.iterrows():
        name = row.get("Generator Name", row.get("Facility", "Unknown generator"))
        fuel = row.get("Fuel Type", "Unknown fuel")
        output = row.get("Output MW", None)
        capacity = row.get("Available Capacity MW", None)

        line = f"- {name} ({fuel}): {_safe_round(output)} MW"

        if capacity is not None and pd.notna(capacity):
            line += f", available capacity: {_safe_round(capacity)} MW"

        lines.append(line)

    return "\n".join(lines)


def format_forecast(df: pd.DataFrame, label: str) -> str:
    if df is None or df.empty:
        return f"I could not find {label} data."

    rows = df.tail(8)

    lines = [f"Latest available {label}:"]

    for _, row in rows.iterrows():
        time_range = _format_time_range(row)
        zone = row.get("Zone", "Ontario")

        value = None
        for possible_col in ["Generation Forecast", "Load Forecast", "Forecast MW", "Forecast"]:
            if possible_col in row.index:
                value = row.get(possible_col)
                break

        if value is not None and pd.notna(value):
            lines.append(f"- {time_range} | {zone}: {_safe_round(value)} MW")
        else:
            lines.append(f"- {time_range} | {zone}")

    return "\n".join(lines)


def format_grid_snapshot() -> str:
    """
    Used for questions like:
    - How does the grid look?
    - What is the grid status?
    """
    parts = ["Ontario grid snapshot:"]

    try:
        price_df = _call_ieso_method("get_lmp_real_time_5_min_ontario_zonal")
        parts.append("")
        parts.append(format_realtime_ontario_price(price_df))
    except Exception as e:
        parts.append(f"\nPrice data unavailable: {e}")

    try:
        totals_df = _call_ieso_method("get_real_time_totals")
        parts.append("")
        parts.append(format_real_time_totals(totals_df))
    except Exception as e:
        parts.append(f"\nReal-time totals unavailable: {e}")

    try:
        fuel_df = _call_ieso_method("get_fuel_mix")
        parts.append("")
        parts.append(format_fuel_mix(fuel_df))
    except Exception as e:
        parts.append(f"\nFuel mix unavailable: {e}")

    return "\n".join(parts)


def run_gridstatus_function(function_key: str, date: str = "latest") -> str:
    if function_key == "grid_snapshot":
        return format_grid_snapshot()

    if function_key not in IESO_METHOD_CATALOG:
        return (
            f"Unknown IESO function key: {function_key}\n\n"
            + list_available_ieso_functions()
        )

    method_name = IESO_METHOD_CATALOG[function_key]["method"]
    description = IESO_METHOD_CATALOG[function_key]["description"]

    try:
        df = _call_ieso_method(method_name, date=date)

        if function_key == "lmp_real_time_5_min_ontario_zonal":
            return format_realtime_ontario_price(df)

        if function_key == "lmp_day_ahead_hourly_ontario_zonal":
            return format_day_ahead_ontario_price(df)

        if function_key == "real_time_totals":
            return format_real_time_totals(df)

        if function_key == "fuel_mix":
            return format_fuel_mix(df)

        if function_key == "generator_report_hourly":
            return format_generator_report(df)

        if function_key in ["wind_market_participant_forecast", "wind_embedded_forecast"]:
            return format_forecast(df, "wind forecast")

        if function_key in ["solar_market_participant_forecast", "solar_embedded_forecast"]:
            return format_forecast(df, "solar forecast")

        if function_key in ["load_forecast", "zonal_load_forecast"]:
            return format_forecast(df, "load forecast")

        return (
            f"GridStatus IESO function: {method_name}\n"
            f"Description: {description}\n\n"
            f"{_format_dataframe_result(df)}"
        )

    except Exception as e:
        return (
            f"Something went wrong while calling {method_name}.\n"
            f"Error: {e}"
        )


def choose_function_key_from_question(question: str) -> str:
    q = question.lower()

    if "available functions" in q or "list functions" in q or "what functions" in q:
        return "list_functions"

    if "grid" in q or "system status" in q or "grid status" in q:
        return "grid_snapshot"

    if "generator" in q or "plant" in q or "facility" in q:
        return "generator_report_hourly"

    if "fuel mix" in q or "supply mix" in q:
        return "fuel_mix"

    if "solar" in q:
        if "embedded" in q:
            return "solar_embedded_forecast"
        return "solar_market_participant_forecast"

    if "wind" in q:
        if "embedded" in q:
            return "wind_embedded_forecast"
        return "wind_market_participant_forecast"

    if "day-ahead" in q or "day ahead" in q or "tomorrow" in q:
        if "reserve" in q:
            return "lmp_day_ahead_operating_reserves"
        if "intertie" in q:
            return "lmp_day_ahead_hourly_intertie"
        return "lmp_day_ahead_hourly_ontario_zonal"

    if "predispatch" in q or "pre-dispatch" in q:
        if "intertie" in q:
            return "lmp_predispatch_hourly_intertie"
        if "virtual" in q:
            return "lmp_predispatch_hourly_virtual_zonal"
        return "lmp_predispatch_hourly_ontario_zonal"

    if "price" in q or "ontario price" in q or "zonal price" in q or "lmp" in q:
        if "operating reserve" in q or "reserve" in q:
            return "lmp_real_time_operating_reserves"
        if "intertie" in q:
            return "lmp_real_time_5_min_intertie"
        if "virtual" in q:
            return "lmp_real_time_5_min_virtual_zonal"
        return "lmp_real_time_5_min_ontario_zonal"

    if "demand" in q or "load" in q or "mw" in q or "power" in q:
        if "forecast" in q:
            return "load_forecast"
        if "zonal" in q or "zone" in q:
            return "load_zonal_5_min"

        
        return "real_time_totals"

    if "real time total" in q or "real-time total" in q or "operating reserve" in q:
        return "real_time_totals"

    if "resource adequacy" in q:
        return "resource_adequacy_report"

    if "shadow price" in q:
        if "day-ahead" in q or "day ahead" in q:
            return "shadow_prices_day_ahead_hourly"
        return "shadow_prices_real_time_5_min"

    if "transmission outage" in q or "planned outage" in q:
        return "transmission_outages_planned"

    if "transmission limit" in q:
        if "outage" in q:
            return "outage_transmission_limits"
        return "in_service_transmission_limits"

    if "intertie" in q:
        if "limit" in q and ("day-ahead" in q or "day ahead" in q):
            return "intertie_limits_day_ahead_hourly"
        if "limit" in q:
            return "intertie_limits_real_time_5_min"
        if "flow" in q:
            return "intertie_flow_5_min"
        return "intertie_actual_schedule_flow_hourly"

    if "surplus baseload" in q:
        return "forecast_surplus_baseload_generation"

    return "real_time_totals"


def answer_from_gridstatus(question: str) -> str:
    function_key = choose_function_key_from_question(question)

    if function_key == "list_functions":
        return list_available_ieso_functions()

    return run_gridstatus_function(function_key)


if __name__ == "__main__":
    print("Testing full GridStatus IESO client.")
    print("Type 'exit' to quit.")
    print("Type 'list functions' to see all supported IESO functions.")

    while True:
        user_question = input("\nAsk an IESO data question: ")

        if user_question.lower() in ["exit", "quit", "q"]:
            print("Goodbye.")
            break

        answer = answer_from_gridstatus(user_question)
        print("\nGridStatus answer:")
        print(answer)
