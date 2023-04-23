from datetime import datetime, timedelta


templates = [
    {
    "text": "abra",
    "file_mask": "*.*",
    "size": {
        "value": 42000000,
        "operator": "le"
    },
    "creation_time": {
        "value": str(datetime.now()+timedelta(days=1)),
        "operator": "le"
    }
    },
    ########
    {
    "text": "",
    "file_mask": "...",
    "size": {
        "value": -123,
        "operator": "aa"
    },
    "creation_time": {
        "value": "string",
        "operator": "bb"
    }
    },
    ########
]


data_example = {"standard": templates[0], "bad": templates[1]}
