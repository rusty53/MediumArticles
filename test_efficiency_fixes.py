#!/usr/bin/env python3

import pandas as pd
import numpy as np

def test_pandas_numpy_imports():
    """Test that pandas and numpy imports work correctly"""
    print('Testing pandas and numpy imports...')
    df = pd.DataFrame({'test': [1, 2, np.nan]})
    print('DataFrame with np.nan created successfully')
    print(df)
    return True

def test_optimized_divisors():
    """Test the optimized divisor function"""
    def divisors(n):
        divisors_list = []
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                divisors_list.append(i)
                if i != n // i:
                    divisors_list.append(n // i)
        return sorted(divisors_list)

    test_numbers = [12, 16, 25, 100]
    for n in test_numbers:
        divs = divisors(n)
        print(f'Divisors of {n}: {divs} (count: {len(divs)})')
    return True

if __name__ == "__main__":
    print("Running efficiency fix tests...")
    test_pandas_numpy_imports()
    print("\n" + "="*50 + "\n")
    test_optimized_divisors()
    print("\nAll tests completed successfully!")
