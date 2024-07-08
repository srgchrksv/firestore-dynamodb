from decimal import Decimal

def floats_to_decimals(data):
    """ Recursively convert float values to Decimal in the given data """
    if isinstance(data, list):
        return [floats_to_decimals(item) for item in data]
    elif isinstance(data, dict):
        return {k: floats_to_decimals(v) for k, v in data.items()}
    elif isinstance(data, float):
        return Decimal(str(data))
    else:
        return data

def decimals_to_floats(data):
    """ Recursively convert Decimal values to float in the given data """
    if isinstance(data, list):
        return [decimals_to_floats(item) for item in data]
    elif isinstance(data, dict):
        return {k: decimals_to_floats(v) for k, v in data.items()}
    elif isinstance(data, Decimal):
        return float(data)
    else:
        return data