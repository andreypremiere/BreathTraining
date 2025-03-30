def parse_fullname(fullname):
    parts = fullname.strip().split()
    if len(parts) == 1:
        return {'lastname': parts[0], 'name': None, 'surname': None}
    elif len(parts) == 2:
        return {'lastname': parts[0], 'name': parts[1], 'surname': None}
    elif len(parts) == 3:
        return {'lastname': parts[0], 'name': parts[1], 'surname': parts[2]}
    else:
        return {'lastname': None, 'name': None, 'surname': None}