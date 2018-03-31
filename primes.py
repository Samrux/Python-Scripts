exit_keywords = ('cancel', 'close', 'exit', 'break')


def is_prime(num):
    if num < 2 or num != int(num):
        return False

    for i in range(2, int(num**0.5 + 1)):
        if num % i == 0:
            return False
    return True


def run():
    print('--- Prime Evaluator ---')

    while True:
        var = input('> Enter an integer: ')
        if var.lower() in exit_keywords:
            print('Closing.')
            break

        try:
            number = int(var)
        except ValueError:
            print(f'Error: "{var}" is not an integer.')
            continue

        isprime = is_prime(number)

        print(f'{number} is {"prime" if isprime else "not prime"}.')


if __name__ == '__main__':
    run()
