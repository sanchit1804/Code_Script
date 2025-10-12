#include <stdio.h>
#include <stdbool.h>
#include <math.h>

bool isPrime(int num) {
    if (num <= 1) return false;
    if (num == 2) return true;
    if (num % 2 == 0) return false;
    
    int limit = (int)sqrt(num);
    for (int i = 3; i <= limit; i += 2) {
        if (num % i == 0) return false;
    }
    
    return true;
}

int main() {
    int number;
    
    printf("Prime Number Checker\n");
    printf("Enter a number: ");
    
    if (scanf("%d", &number) != 1) {
        printf("Invalid input!\n");
        return 1;
    }
    
    if (isPrime(number)) {
        printf("%d is Prime\n", number);
    } else {
        printf("%d is Not Prime\n", number);
    }
    
    return 0;
}

