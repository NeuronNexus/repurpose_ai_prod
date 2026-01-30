def normalize_list(items):
    """
    Converts list items to strings.
    If item is dict, extract 'description' or stringify safely.
    """
    normalized = []
    for item in items:
        if isinstance(item, str):
            normalized.append(item)
        elif isinstance(item, dict):
            if "description" in item:
                normalized.append(item["description"])
            else:
                normalized.append(str(item))
        else:
            normalized.append(str(item))
    return normalized
