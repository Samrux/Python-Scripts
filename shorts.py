# Print primes up to 1000, in 79 characters
print([x for x in range(2, 10000) if not any(x%i==0 for i in range(2, x//2+1))])
