import pandas as pd

def save_to_csv(data, filename="manga_data.csv"):
    """save the scraped manga data to a CSV file"""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to '{filename}'")