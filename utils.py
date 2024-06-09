def get_first_name(name_obj):
    if name_obj is None:
        return None
    first_name = str(name_obj).split(" ")[0]
    return first_name
