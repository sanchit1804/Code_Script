# Prime Number Checker

A C program to check if a number is prime or not.

## What it does

Takes a number as input and tells you whether it's prime or not. Pretty straightforward.

## How to compile

```bash
gcc prime_checker.c -o prime_checker -lm
```

The `-lm` flag is needed for the math library.

## Usage

```bash
./prime_checker
```

Then just enter a number when it asks.

## Examples

```
Prime Number Checker
Enter a number: 17
17 is Prime
```

```
Prime Number Checker
Enter a number: 24
24 is Not Prime
```

## How it works

The program checks divisibility up to the square root of the number. If nothing divides it evenly, it's prime. Numbers less than 2 aren't considered prime.

## Test it with these

Some primes to try: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97

Some non-primes: 4, 6, 8, 9, 10, 12, 15, 16, 18, 20, 21, 24, 25, 27, 28, 30

