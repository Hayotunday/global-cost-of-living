# src/main.py
from fastapi import FastAPI, Request, HTTPException
import pandas as pd
import os
import numpy as np

app = FastAPI(
    title="Global Cost of Living API",
    description="Returns cost of living data by country from Kaggle dataset.",
    version="1.0"
)

# -------------------------------
# CONFIG
# -------------------------------
CSV_PATH = "../data/cost-of-living_v2.csv"   # relative to project root

# Human-readable column names
COLUMN_MAP = {
    'x1': 'Meal, Inexpensive Restaurant (USD)',
    'x2': 'Meal for 2 People, Mid-range Restaurant, Three-course (USD)',
    'x3': 'McMeal at McDonalds (or Equivalent Combo Meal) (USD)',
    'x4': 'Domestic Beer (1 pint draught) (USD)',
    'x5': 'Imported Beer (12 oz small bottle) (USD)',
    'x6': 'Cappuccino (regular) (USD)',
    'x7': 'Coke/Pepsi (12 oz small bottle) (USD)',
    'x8': 'Water (12 oz small bottle) (USD)',
    'x9': 'Milk (regular), (1 gallon) (USD)',
    'x10': 'Loaf of Fresh White Bread (1 lb) (USD)',
    'x11': 'Rice (white), (1 lb) (USD)',
    'x12': 'Eggs (regular) (12) (USD)',
    'x13': 'Local Cheese (1 lb) (USD)',
    'x14': 'Chicken Fillets (1 lb) (USD)',
    'x15': 'Beef Round (1 lb) (or Equivalent Back Leg Red Meat) (USD)',
    'x16': 'Apples (1 lb) (USD)',
    'x17': 'Banana (1 lb) (USD)',
    'x18': 'Oranges (1 lb) (USD)',
    'x19': 'Tomato (1 lb) (USD)',
    'x20': 'Potato (1 lb) (USD)',
    'x21': 'Onion (1 lb) (USD)',
    'x22': 'Lettuce (1 head) (USD)',
    'x23': 'Water (1.5 liter bottle) (USD)',
    'x24': 'Bottle of Wine (Mid-Range) (USD)',
    'x25': 'Domestic Beer (0.5 liter bottle) (USD)',
    'x26': 'Imported Beer (12 oz small bottle) (USD)',
    'x27': 'Cigarettes 20 Pack (Marlboro) (USD)',
    'x28': 'One-way Ticket (Local Transport) (USD)',
    'x29': 'Monthly Pass (Regular Price) (USD)',
    'x30': 'Taxi Start (Normal Tariff) (USD)',
    'x31': 'Taxi 1 mile (Normal Tariff) (USD)',
    'x32': 'Taxi 1 hour Waiting (Normal Tariff) (USD)',
    'x33': 'Gasoline (1 gallon) (USD)',
    'x34': 'Volkswagen Golf 1.4 90 KW Trendline (Or Equivalent New Car) (USD)',
    'x35': 'Toyota Corolla Sedan 1.6l 97kW Comfort (Or Equivalent New Car) (USD)',
    'x36': 'Basic (Electricity, Heating, Cooling, Water, Garbage) for 915 sq ft Apartment (USD)',
    'x37': 'Mobile Phone Monthly Plan with Calls and 10GB+ Data (USD)',
    'x38': 'Internet (60 Mbps or More, Unlimited Data, Cable/ADSL) (USD)',
    'x39': 'Fitness Club, Monthly Fee for 1 Adult (USD)',
    'x40': 'Tennis Court Rent (1 Hour on Weekend) (USD)',
    'x41': 'Cinema, International Release, 1 Seat (USD)',
    'x42': 'Preschool (or Kindergarten), Full Day, Private, Monthly for 1 Child (USD)',
    'x43': 'International Primary School, Yearly for 1 Child (USD)',
    'x44': '1 Pair of Jeans (Levis 501 Or Similar) (USD)',
    'x45': '1 Summer Dress in a Chain Store (Zara, H&M, ...) (USD)',
    'x46': '1 Pair of Nike Running Shoes (Mid-Range) (USD)',
    'x47': '1 Pair of Men Leather Business Shoes (USD)',
    'x48': 'Apartment (1 bedroom) in City Centre (USD)',
    'x49': 'Apartment (1 bedroom) Outside of Centre (USD)',
    'x50': 'Apartment (3 bedrooms) in City Centre (USD)',
    'x51': 'Apartment (3 bedrooms) Outside of Centre (USD)',
    'x52': 'Price per Square Feet to Buy Apartment in City Centre (USD)',
    'x53': 'Price per Square Feet to Buy Apartment Outside of Centre (USD)',
    'x54': 'Average Monthly Net Salary (After Tax) (USD)',
    'x55': 'Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate'
}

# -------------------------------
# HELPERS
# -------------------------------
def load_and_clean_csv() -> pd.DataFrame:
    """Load CSV and replace NaN/inf with None (JSON null)."""
    if not os.path.exists(CSV_PATH):
        raise HTTPException(
            status_code=500,
            detail="Dataset not found. Run `python scripts/update_dataset.py` first."
        )
    df = pd.read_csv(CSV_PATH)
    # Convert NaN, inf, -inf → None (becomes null in JSON)
    df = df.replace([np.nan, np.inf, -np.inf], None)
    return df

# -------------------------------
# ROUTES
# -------------------------------

@app.get("/")
async def root():
    return {"message": "Global Cost of Living API is live!", "status": "ready"}


@app.get("/health")
def health():
    """Simple health check."""
    return {
        "status": "healthy",
        "dataset_exists": os.path.exists(CSV_PATH)
    }


@app.post("/country_data")
async def get_country_data(request: Request):
    """
    Return all rows for a given country.
    Body: {"country": "Japan"}
    """
    body = await request.json()
    country = body.get("country")
    if not country or not isinstance(country, str):
        raise HTTPException(status_code=400, detail="Invalid or missing 'country' field.")

    country_key = country.strip().lower()

    # Load fresh data every time (no cache)
    df = load_and_clean_csv()

    # Filter by country
    filtered = df[df['country'].str.lower() == country_key]
    if filtered.empty:
        raise HTTPException(status_code=404, detail=f"No data for country: {country}")

    # Rename columns
    result_df = filtered.rename(columns=COLUMN_MAP)

    # Return as JSON-serializable list of dicts
    return result_df.to_dict(orient="records")


@app.post("/city_data")
async def get_city_data(request: Request):
    """
    Return cost of living data for a **city in a specific country**.
    
    Body:
    {
        "city": "Paris",
        "country": "France"
    }
    """
    body = await request.json()

    city = body.get("city")
    country = body.get("country")

    # Validate inputs
    if not city or not isinstance(city, str):
        raise HTTPException(status_code=400, detail="Missing or invalid 'city' field.")
    if not country or not isinstance(country, str):
        raise HTTPException(status_code=400, detail="Missing or invalid 'country' field.")

    city_key = city.strip().lower()
    country_key = country.strip().lower()

    # Load fresh data
    df = load_and_clean_csv()

    # Filter by BOTH city and country (case-insensitive)
    mask = (df['city'].str.lower() == city_key) & (df['country'].str.lower() == country_key)
    filtered = df[mask]

    if filtered.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for city: '{city}' in country: '{country}'"
        )

    # Rename columns
    result_df = filtered.rename(columns=COLUMN_MAP)

    # Return as list of dicts (usually 1 row)
    return result_df.to_dict(orient="records")