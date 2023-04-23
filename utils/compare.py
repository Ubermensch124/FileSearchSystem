""" Dictionary for compare operations with creation_time and file_size """

compare_dict = {
    "eq": lambda item, value: item == value,
    "gt": lambda item, value: item > value,
    "lt": lambda item, value: item < value,
    "ge": lambda item, value: item >= value,
    "le": lambda item, value: item <= value,
}
