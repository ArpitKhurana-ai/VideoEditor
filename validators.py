def validate_input(data):
    required = ['url', 'start', 'end', 'row_id']
    missing = [field for field in required if field not in data]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    return True, None
