def validate_links_length(value):
    if value < 5:
        raise "The length must be greater than or equal to 5"
    return value


def validate_links_scope(value):
    if not any(value):
        raise "At least one value must be selected"
    return value
