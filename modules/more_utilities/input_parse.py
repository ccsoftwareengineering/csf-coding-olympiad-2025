from math import inf


def input_parse_text(raw_input: str, input_data):
    max_length = input_data['options'].get('max_length') or inf
    min_length = input_data['options'].get('min_length') or 0
    if len(raw_input) > max_length:
        return None, f'Length should not exceed {max_length} characters.'
    elif len(raw_input) < min_length:
        return None, f'Length should be >= {min_length} characters.'
    return raw_input, None


def input_parse_int(ri: str, ipd):
    pass


input_parse_type_map = {
    "text": input_parse_text
}


def input_parse(raw_input: str, input_data):
    return input_parse_type_map[input_data['type']](raw_input, input_data)
