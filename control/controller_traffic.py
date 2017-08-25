# initial traffic conditions
speed_limit = 0.7

splits = {
    'center': ['parkirisce', 'hodnik'],
    'stranski': ['center', 'parkirisce'],
    'hodnik': ['stranski', 'zunanjost'],
    'zunanjost': [],
    'parkirisce': []
}


aryco_id_to_split_name = {
    33: 'hodnik',
    35: 'center',
    38: 'stranski'
}