LeftAlign = ('left', 'l', '', None,)
RightAlign = ('right', 'r',)
CenterAlign = ('center', 'c',)
AllAlignments = LeftAlign + RightAlign + CenterAlign


def columnize(lst, ncolumns, align='left', vertical=False, padding=1, padchar=' '):
    # type: (iter, int, str, bool, int, str) -> str
    """Takes an iterable and returns a string with the items organized in
    columns. Left alignment and left-to-right order by default.

    :param lst: Iterable to make columns of
    :param ncolumns: Number of columns
    :param align: left, center or right
    :param vertical: If True, goes top-to-bottom first
    :param padding: Number of characters between columns
    :param padchar: Character with which to fill columns
    """

    if ncolumns < 0:
        raise ValueError('Negative number of columns')

    align = align.lower()
    if align not in AllAlignments:
        raise ValueError('Unknown alignment: ' + align)


    if not lst or ncolumns == 0:
        return ''

    lst = [str(x) for x in lst]

    # Add items so the length of the list is divisible by ncolumns
    if len(lst) % ncolumns > 0:
        lst += ['']*(ncolumns - len(lst) % ncolumns)

    # Column width and number of rows
    width = max(len(s) for s in lst) + padding
    nrows = len(lst) // ncolumns

    # index: Returns the index of the object desired to be at position x,y
    if vertical:
        def index(x, y): return nrows*x + y
    else:
        def index(x, y): return x + ncolumns*y

    # aligned: Returns the object with padding around it to align in a column
    if align in CenterAlign:
        def aligned(item):
            p = padchar * (width - len(item))
            return p[:len(p)//2] + item + p[len(p)//2:]
    elif align in RightAlign:
        def aligned(item): return padchar*(width - len(item)) + item
    else:  # LeftAlign
        def aligned(item): return item + padchar*(width - len(item))

    # Builds and returns string in columnized form from the list
    return '\n'.join(
               ''.join(
                   aligned(lst[index(x, y)])
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
    names = ['CarloSebaX', 'Akrome', 'AxlKings', 'epanke11', 'Mac666', 'Raid Max', 'Luxarx', 'RicardoCayupe', 'polmacarlni', '[RCG]wolfman-1999', 'llç', 'Bizzarresound Cross', 'Josué', 'tomas', 'Ramm4', 'Sowk', 'Rowlet', 'cokeohi', 'kakaman593', 'nekokami', 'Rythm', 'Failing22', 'Spec7re', 'JereDick', 'Oskyar', 'Shoddybike', 'miaumiau08', 'Pac-Man', 'Crastiv', 'SilverCrow', 'djprieto', 'TheChileanKink', 'MasterTurra27', 'nts', 'Anthony', 'elnaico21', 'Parabol', 'ZeroXD', 'Joaquin Caqueo', 'Alejo_el_Manco', 'Negragu', 'Mr. Anacletus', 'CPG Yuri', 'Mariogros7', 'Tatsumaki', 'MATU', 'Zinx', 'Kah', 'Maxistorm', 'Hugoku', 'Xavierutox', 'Jetsu99', 'DeadSoul158', 'Inkhemi', 'fabiraptor99', 'Sebahdn', 'ArmoredReaper', 'Seiraku', 'JJBprodutcions', 'wxblex', 'Spartage', 'Reo (leonardo)', 'Colorin', 'Baron', 'Dinodrill', 'El Hector', 'suoxrt', 'supervixo', 'Draccel', 'Tohsaka rin', 'C0t300', 'Seba', 'Wachimingo', 'ThexRoritrox', 'Jamaicano Blanco', 'Sambot', 'zancres', 'Monsoon', 'argentum', 'moya76', 'phryzq', 'Nicolas', 'EdisonV', 'Mikasa Ackerman', 'Spec7re', 'Axel', 'PatchBot', 'Samrux', 'Umbingelelo', 'tom;fa', 'faker', 'Zeo', 'SpaceTraveler', 'mati', 'Raserii', 'Sudenth']

    print('\n' + columnize(names, 5, align='center', vertical=True))
