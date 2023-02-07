def get_vars(stat_type, player, season=None):
    vars = {
        'statcast_running': {
            'keys': ['player_id', 'season', 'ft/s', 'hp-1st', 'bolts',
                'pos_rank', 'age_rank', 'league_rank', 'percentile'],
            'elements': ['td[1]', 'td[3]', 'td[4]', 'td[5]', 'td[6]', 'td[7]',
                'td[8]', 'td[9]'],
            'test_header': 'Sprint Speed (ft/s)',
            'test_header_index': 2,
            'url': f'https://baseballsavant.mlb.com/savant-player/{player}'
                    '?stats=statcast-r-running-mlb',
        },
        'statcast_season': {
            'keys': ['player_id', 'season', 'pitches', 'balls', 'barrels',
                'barrel%', 'barrel/pa', 'ev', 'max_ev', 'la',
                'sweet_spot%', 'xba', 'xslg', 'woba', 'xwoba', 'xwobacon',
                'hh%', 'k%', 'bb%'],
            'elements': ['td[1]', 'td[3]', 'td[4]', 'td[5]', 'td[6]', 'td[7]',
                'td[8]', 'td[9]', 'td[10]', 'td[11]', 'td[12]', 'td[13]', 
                'td[14]', 'td[15]', 'td[16]', 'td[17]', 'td[18]', 'td[19]', ],
            'test_header': 'Barrels',
            'test_header_index': 4,
            'url': f'https://baseballsavant.mlb.com/savant-player/{player}'
                    '?stats=statcast-r-hitting-mlb',
        },
        'statcast_at_bat': {
            'keys': ['player_id', 'date', 'opponent', 'result', 'ev',
                'la', 'distance', 'direction', 'pitch_velo', 'pitch_type',],
            'elements': ['td[2]', 'td[5]', 'td[6]', 'td[7]', 'td[8]', 'td[9]',
                'td[10]', 'td[11]', 'td[12]',],
            'test_header': 'Result',
            'test_header_index': 4,
            'url': f'https://baseballsavant.mlb.com/savant-player/{player}?'
                   f'stats=gamelogs-r-hitting-statcast&season={season}',
        },
        'standard_game': {
            'keys': ['player_id', 'date', 'home', 'away', 'pa', 'ab', 'r', 'h',
                '2B', '3B', 'hr', 'rbi', 'bb', 'k', 'sb', 'cs', 'hbp', 'avg',
                'obp', 'slg',],
            'elements': ['td[1]', 'td[2]', 'td[3]', 'td[4]', 'td[5]', 'td[6]',
                'td[7]', 'td[8]', 'td[9]', 'td[10]', 'td[11]', 'td[12]',
                'td[13]', 'td[14]', 'td[15]', 'td[16]', 'td[17]', 'td[18]',
                'td[19]',],
            'test_header': 'Away Tm',
            'test_header_index': 2,
            'url': f'https://baseballsavant.mlb.com/savant-player/{player}?'
                   f'stats=gamelogs-r-hitting-mlb&season={season}',
        },
        'standard_season': {
            'keys': ['player_id', 'season', 'g', 'pa', 'ab', 'r', 'h',
                '2B', '3B', 'hr', 'rbi', 'bb', 'k', 'sb', 'cs', 'hbp', 'avg',
                'obp', 'slg',],
            'elements': ['td[2]', 'td[5]', 'td[6]', 'td[7]', 'td[8]', 'td[9]',
                'td[10]', 'td[11]', 'td[12]', 'td[13]', 'td[14]', 'td[15]',
                'td[16]', 'td[17]', 'td[18]', 'td[19]', 'td[20]', 'td[21]',],
            'test_header': 'G',
            'test_header_index': 4,
            'url': f'https://baseballsavant.mlb.com/savant-player/{player}?'
                   f'stats=career-r-hitting-mlb',
        },
    }
    
    return vars[stat_type]
