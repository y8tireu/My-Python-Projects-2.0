def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def prime_and_composite_numbers(start, end):
    """Return two lists: one of prime numbers and one of composite numbers within a given range."""
    prime_numbers = []
    composite_numbers = []

    for num in range(start, end + 1):
        if is_prime(num):
            prime_numbers.append(num)
        elif num > 1:
            composite_numbers.append(num)
    
    return prime_numbers, composite_numbers

# Define the range
start = 1
end = 1000

# Get prime and composite numbers
primes, composites = prime_and_composite_numbers(start, end)

# Display the results
print("Prime Numbers between 1 and 1000:")
print(primes)
print("\nComposite Numbers between 1 and 1000:")
print(composites)
