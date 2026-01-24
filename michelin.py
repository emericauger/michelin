"""Extract Michelin starred restaurants and save to Excel."""

import pandas as pd
from scraper import extract_restaurants_etoiles


def main():
    data = extract_restaurants_etoiles(verbose=True)
    df = pd.DataFrame.from_dict(data, orient="index")
    df.to_excel("export.xlsx", index_label="id")
    print(f"✓ Saved {len(df)} restaurants to export.xlsx")


if __name__ == "__main__":
    main()
