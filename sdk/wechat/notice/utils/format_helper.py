
def list2FormattedIds(l:list)->str:
    if len(l) == 0:
        return ''
    if len(l) == 1:
        return str(l[0])
    return '|'.join(l)

def formattedIds2List(s:str)->list:
    if s == '':
        return []
    if '|' not in s:
        return [s]
    return [str(item) for item in s.split('|')]