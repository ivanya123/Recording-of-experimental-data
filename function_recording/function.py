def check_float(string: str):
    try:
        float(string)
        return True
    except ValueError:
        return False