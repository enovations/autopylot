# initial traffic conditions
speed_limit = 0.7

splits = {
    'center': ['parkirisce', 'hodnik'],
    'stranski': ['obracalisce', 'parkirisce'],
    'hodnik': ['stranski', 'zunanjost'],
    'zunanjost': [],
    'parkirisce': [],
    'izhodisce': ['center', 'hodnik'],
    'obracalisce': ['center', 'izhodisce']
}


aryco_id_to_split_name = {
    33: 'hodnik',
    35: 'center',
    38: 'stranski',
    39: 'izhodisce',
    37: 'obracalisce0'

}