LeftAlign = ('left', 'Left', 'l', 'L', '', None)
RightAlign = ('right', 'Right', 'r', 'R')
CenterAlign = ('center', 'Center', 'c', 'C')


def aligned(item, width, char, align):
    pad = char * (width - len(item))

    if align in CenterAlign:
        cut = len(pad) // 2
        return pad[:cut] + item + pad[cut:]
    elif align in RightAlign:
        return pad + item
    else:
        return item + pad


def columnize(lst, ncolumns, align='left', vertical=False, padding=1, padchar=' '):
    """Takes an iterable and returns a string with the items organized in
    columns. Left alignment and left-to-right order by default.
    """

    if not lst or ncolumns == 0:
        return ''

    lst = [str(x) for x in lst]

    # Add items so the length of the list is divisible by ncolumns
    if len(lst) % ncolumns > 0:
        lst += [''] * (ncolumns - (len(lst) % ncolumns))

    nrows = len(lst) // ncolumns
    width = max(len(s) for s in lst) + padding
    index = (lambda x,y: nrows*x + y) if vertical else (lambda x,y: x + ncolumns*y)

    return '\n'.join(
               ''.join(
                   aligned(lst[index(x, y)], width, padchar, align)
                   for x in range(ncolumns)
               ) for y in range(nrows)
            )


# Examples
if __name__ == '__main__':

    roots = [round(x**0.5, 5) for x in range(70, 120)]
    # Columnize numbers, right-aligned
    print('\n' + columnize(roots, 5, align='right'))
    # Align to period using format()
    print('\n' + columnize(("{:7.4f}".format(x) for x in roots), 5, padding=2))

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
