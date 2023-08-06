def get_sum_for(data) -> float:
    return data[:].sum()


def get_mean_for(data) -> float:
    return data[:].mean()


def get_min_for(data) -> float:
    return data[:].min()


def get_max_for(data) -> float:
    return data[:].max()


def get_positive_values_from(data):
    _data = data[:].copy()
    _data[_data < 0] = 0
    return _data


def get_negative_values_from(data):
    _data = data[:].copy()
    _data[_data > 0] = 0
    return _data
