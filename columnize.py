def columnize(lst, amount, padding=1, padchar=' ', align='left') -> str:
    """Takes an iterable and returns a string with the items organized in
    columns, left-to-right top-to-bottom.
    """

    lst = [str(x) for x in lst]  # Convert to list of strings

    if amount < 1:
        return ''
    elif amount == 1:
        return '\n'.join(lst)

    lst += [''] * (amount-(len(lst) % amount))  # Fill empty slots
    width = max(len(x) for x in lst) + padding

    # Organize data into sublists of length 'amount'
    rows = []
    for i in range(0, len(lst), amount):
        group = []
        for j in range(amount):
            group.append(lst[i+j])
        rows.append(group)

    # Make columns
    result = ''
    for group in rows:
        for item in group:
            pad = padchar * (width - len(item))
            if align in ('right', 'r'):
                algnitem = pad + item
            elif align in ('center', 'c'):
                algnitem = pad[:len(pad)//2] + item + pad[len(pad)//2:]
            else:
                algnitem = item + pad
            result += algnitem

        result += '\n'

    return result


if __name__ == '__main__':
    from random import sample, randint, uniform as randfloat

    names = ['Akexus', 'Akrytael', 'Albinos', 'Aren', 'Atlahika', 'Cybershell12',
             'Dae', 'Darky', 'Dja', 'Dotare', 'E-crafter', 'Eli', 'Faye',
             'Felvine', 'Fluffy', 'Frykas', 'Félinx', 'GabNagi', 'Gaiko',
             'Hdi64', 'Heddy', 'Heliander', 'Hueco', 'Jlaime', "Ju'", 'Julie',
             'Kitty', 'Kurybat', 'LaGeek', 'Lagartha', 'Laukhlass', 'Luomi',
             'Magicarpe', 'Maxime62', 'Microman', 'Nataire', 'Oulumor', 'Pikalou',
             'Pixocode', 'Ryouh', 'Seth', 'Shisõka', 'Skoyatt', 'Stefstef',
             'Tonitch', 'Topy', 'Tsumyane', 'Vayan', 'Yoshi24', 'Zood']

    nums = map(lambda _: round(randfloat(0, 1), randint(2, 7)), [None]*64)

    print('EXAMPLE 1:\n' + columnize(sample(names, 30), 4))
    print('EXAMPLE 2:\n' + columnize(names, 7, align='center'))
    print('EXAMPLE 3:\n' + columnize(nums, 6, align='r', padding=2))
