import pandas as pd
import numpy as np

def generate_random_csv(filename: str, rows: int) -> None:
    data = {
        'open': np.round(np.random.uniform(1, 100, rows), 2),
        'close': np.round(np.random.uniform(1, 100, rows), 2)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Write to CSV
    df.to_csv(filename, index=False)

# Example usage
generate_random_csv('random_data.csv', 10000)
