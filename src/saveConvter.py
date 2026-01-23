from singletons import resourceHandler


def check_saves(folder: str) -> None:
    for m_file in resourceHandler.load_dir(f'.\\saves\\{folder}'):
        if m_file.endswith('.json'):
            sheet = resourceHandler.load_json(f'.\\saves\\{folder}\\{m_file}')
            
            if sheet.get('version'):
                continue
            
            sheet = reformat_sheet(sheet)
            
            resourceHandler.save_json(f'.\\saves\\{folder}\\{m_file}', sheet)
        else:
            check_saves(f'{folder}\\{m_file}')
            
def reformat_text(text: str) -> tuple[str, dict[str, dict]]:
    new_text: str = ''
    format_data: dict[str, dict] = {}
    
    index: int = 0
    for word in text.split():
        if word == '{b}':
            format_data[str(index - 1)] = {
                'type': 0,
                'data': ''
            }
            continue
        elif word == '{/b}':
            format_data[str(index - 1)] = {
                'type': 1,
                'data': ''
            }
            continue
        
        elif word == '{i}':
            format_data[str(index - 1)] = {
                'type': 2,
                'data': ''
            }
            continue
        elif word == '{/i}':
            format_data[str(index - 1)] = {
                'type': 3,
                'data': ''
            }
            continue
        
        elif word == '{a}':
            format_data[str(index - 1)] = {
                'type': 4,
                'data': '#D34D35'
            }
            continue
        elif word == '{/a}':
            format_data[str(index - 1)] = {
                'type': 5,
                'data': ''
            }
            continue
        
        elif word == '{t}':
            format_data[str(index - 1)] = {
                'type': 4,
                'data': '#2D638E'
            }
            continue                    
        elif word == '{/t}':
            format_data[str(index - 1)] = {
                'type': 5,
                'data': ''
            }
            continue
        
        elif word == '{lb}':
            format_data[str(index)] = {
                'type': 6,
                'data': ''
            }
            continue
            
        new_text += word + ' '
        index = len(new_text)
        
    new_text = new_text.strip()
    
    return (new_text, format_data)
            
def reformat_sheet(sheet: dict[str]) -> dict[str, dict[str]]:
    new_sheet: dict[str, dict[str]] = {
        'version': '2.0',
        'colors': []
    }
    
    for card_id, card_data in sheet.items():
        card: dict[str, dict] = {
            'width': card_data['width'],
            'height': (card_data['height'] + 2) * 2,
            'components': {
                'Name_Component': card_data['components']['Name_Component'],
                'Top_Stat_Component': card_data['components']['Top_Stat_Component']
            }
        }
        
        for comp_name, comp_data in card_data['components'].items():
            if comp_name == 'Traits_Title':
                card['components']['Traits_Title'] = comp_data
                
            elif comp_name == 'Abilities_Title':
                card['components']['Abilities_Title'] = comp_data
                
            elif comp_name.startswith('Trait'):
                new_desc, format_data = reformat_text(comp_data['desc'])
                
                card['components'][comp_name] = {
                    'name': comp_data['name'],
                    'format': format_data,
                    'desc': new_desc
                }
                
            elif comp_name.startswith('Ability'):
                new_effects: dict[str, str] = {}
                extra_text: str = ''
                
                for effect_name, effect_desc in comp_data['effects'].items():
                    if effect_name.endswith(':'):
                        effect_name = effect_name[:-1]
                        
                    if effect_name == '':
                        effect_desc: str = effect_desc
                        extra_text = effect_desc.strip('{i} {/i}')
                        continue
                        
                    new_desc, format_data = reformat_text(effect_desc)
                    new_effects[effect_name] = {
                        'desc': new_desc,
                        'format': format_data,
                        'in_line': True if effect_name == 'CR' else False
                    }
                    
                new_marker: dict[str, list | int] = None
                
                if comp_data['marker']:
                    new_marker = {
                        'grid_size': comp_data['marker']['gridSize'],
                        'marker_overlay': {
                            'STAKE': [],
                
                            'STACK': [],
                            'STACK_LINE': [],
                            'STACK_MULTI': [],
                            
                            'TANKBUSTER': [],
                            'TANKBUSTER_AOE': [],
                            'TANKBUSTER_CAUTION': [],
                            
                            'PROXIMITY': None
                        },
                        'marker_area': comp_data['marker']['markerArea']
                    }
                    
                    if comp_data['marker']['type'] == 0:
                        new_marker['marker_overlay']['PROXIMITY'] = { 'pos': (comp_data['marker']['gridSize'][0], 0), 'data': '' }
                        
                    elif comp_data['marker']['type'] == 1:
                        for y, col in enumerate(comp_data['marker']['markerArea']):
                            for x, row in enumerate(col):
                                if row == 2:
                                    new_marker['marker_overlay']['STACK'].append({ 'pos': (y, x), 'data': '' })
                                    
                    elif comp_data['marker']['type'] == 2:
                        for y, col in enumerate(comp_data['marker']['markerArea']):
                            for x, row in enumerate(col):
                                if row == 2:
                                    new_marker['marker_overlay']['STAKE'].append({ 'pos': (y, x), 'data': 'red' })
                
                card['components'][comp_name] = {
                    'name': comp_data['name'],
                    'invk': comp_data['invk'],
                    'types': comp_data['types'],
                    'effects': new_effects,
                    'extra_text': extra_text,
                    'marker': new_marker
                }
                
        new_sheet[card_id] = card
        
    return new_sheet