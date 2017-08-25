# initial traffic conditions
speed_limit = 0.7

splits = {
    'lams': ['hodnik', 'parkirisce'],
    'lmsv': ['parkirisce', 'lmsv'],
    'hodnik': ['lams', 'zunanjost'],
    'zunanjost': [],
    'parkirisce': []
}


aryco_id_to_split_name = {
    31: 'lamsv',
    32: 'hodnik',
    33: 'lams'
}