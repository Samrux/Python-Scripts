from math import ceil

LEFT = 'l'
RIGHT = 'r'
CENTER = 'c'

LeftAlign = ('left', 'l', '', None)
RightAlign = ('right', 'r')
CenterAlign = ('center', 'c')


def columnize(lst: iter, ncolumns: int,
              align: str=LEFT, vertical: bool=False,
              padding: int=1, padchar: str=' ') -> str:
    """Takes an iterable and returns a string with the items organized in
    columns. Left alignment and left-to-right order by default.
    """

    if ncolumns < 0 or padding < 0:
        raise ValueError('Negative padding or number of columns')
    if align not in LeftAlign + RightAlign + CenterAlign:
        raise ValueError('Invalid alignment')

    if ncolumns == 0 or not lst: return ''

    lst = [str(x) for x in lst]

    if ncolumns == 1: return '\n'.join(lst)

    # Add items so the length of the list is divisible by ncolumns
    if len(lst) % ncolumns > 0:
        lst += [''] * (ncolumns - (len(lst) % ncolumns))

    width = max(len(x) for x in lst) + padding
    nrows = len(lst) // ncolumns

    # Organize data into rows
    rows = []
    for i in range(nrows):
        row = []
        for j in range(ncolumns):
            if vertical:
                row.append(lst[i + nrows * j])
            else:
                row.append(lst[ncolumns * i + j])
        rows.append(row)

    # Make indented and justified strings out of those rows
    stringrows = []
    for row in rows:
        rowstr = ''
        for item in row:
            pad = padchar * (width - len(item))
            if align in RightAlign:
                algnitem = pad + item
            elif align in CenterAlign:
                cut = ceil(len(pad) // 2)
                algnitem = pad[:cut] + item + pad[cut:]
            else:
                algnitem = item + pad
            rowstr += algnitem
        stringrows.append(rowstr)

    return '\n'.join(stringrows)


# Examples
if __name__ == '__main__':

    roots = [round(x**0.5, 5) for x in range(70, 120)]

    # Columnize numbers, right-aligned
    print('\n' + columnize(roots, 5, align='right'))

    # Align to period using format()
    print('\n' + columnize(["{:7.4f}".format(x) for x in roots], 5, padding=2))


    # Names in credits style
    names = ['Akexus', 'Akrytael', 'Albinos', 'Aren', 'Atlahika', 'Cybershell12',
             'Dae', 'Darky', 'Dja', 'Dotare', 'E-crafter', 'Eli', 'Faye',
             'Felvine', 'Fluffy', 'Frykas', 'Felinx', 'GabNagi', 'Gaiko',
             'Hdi64', 'Heddy', 'Heliander', 'Hueco', 'Jlaime', "Ju'", 'Julie',
             'Kitty', 'Kurybat', 'LaGeek', 'Lagartha', 'Laukhlass', 'Luomi',
             'Magicarpe', 'Maxime62', 'Microman', 'Nataire', 'Oulumor', 'Pikalou',
             'Pixocode', 'Ryouh', 'Seth', 'Shisoka', 'Skoyatt', 'Stefstef',
             'Tonitch', 'Topy', 'Tsumyane', 'Vayan', 'Yoshi24', 'Zood']

    print('\n' + columnize(names, 3, align='center', vertical=True))
