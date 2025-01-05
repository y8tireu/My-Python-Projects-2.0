def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def list_prime_and_composite(start, end):
    primes = []
    composites = []
    for num in range(start, end + 1):
        if is_prime(num):
            primes.append(num)
        elif num > 1:
            composites.append(num)
    return primes, composites

# Example usage
start = 1
end = 100
primes, composites = list_prime_and_composite(start, end)
print("Prime numbers:", primes)
print("Composite numbers:", composites)

