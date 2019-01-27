images_dir = '../images'
generation_dir = '/generation'
instance_dir = '/instance'
image_name = '/'


def convert_to_float(data):
    for i in data:
        i[0], i[1] = float(i[0]), float(i[1])
    return data


def convert_to_string(data):
    return str(data)


def sort_to_order(data):
    data.sort(key=lambda i: int(''.join(filter(str.isdigit, i))))
    return data
