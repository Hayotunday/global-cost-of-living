# src/main.py
from fastapi import FastAPI, Request, HTTPException
import pandas as pd
import os
import numpy as np
from pathlib import Path

app = FastAPI(
    title="Global Cost of Living API",
    description="Returns cost of living data for a city in a specific country.",
    version="1.0"
)

# --- ABSOLUTE PATH ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "cost-of-living_v2.csv"
# ---------------------

COLUMN_MAP = {
    "x1": {
        "en": "Meal, Inexpensive Restaurant",
        "de": "Mahlzeit, Günstiges Restaurant"
    },
    "x2": {
        "en": "Meal for 2 People, Mid-range Restaurant, Three-course",
        "de": "Mahlzeit für 2 Personen, Mittelklasse-Restaurant, Drei-Gänge-Menü"
    },
    "x3": {
        "en": "McMeal at McDonalds (or Equivalent Combo Meal)",
        "de": "McMeal bei McDonalds (oder Äquivalentes Combo-Menü)"
    },
    "x4": {
        "en": "Domestic Beer (1 pint draught)",
        "de": "Inländisches Bier (0,5 Liter vom Fass)"
    },
    "x5": {
        "en": "Imported Beer (12 oz small bottle)",
        "de": "Importiertes Bier (0,33 Liter Flasche)"
    },
    "x6": {
        "en": "Cappuccino (regular)",
        "de": "Cappuccino (normal)"
    },
    "x7": {
        "en": "Coke/Pepsi (12 oz small bottle)",
        "de": "Cola/Pepsi (0,33 Liter Flasche)"
    },
    "x8": {
        "en": "Water (12 oz small bottle)",
        "de": "Wasser (0,33 Liter Flasche)"
    },
    "x9": {
        "en": "Milk (regular), (1 gallon)",
        "de": "Milch (normal), (3,78 Liter)"
    },
    "x10": {
        "en": "Loaf of Fresh White Bread (1 lb)",
        "de": "Laib frisches Weißbrot (500g)"
    },
    "x11": {
        "en": "Rice (white), (1 lb)",
        "de": "Reis (weiß), (500g)"
    },
    "x12": {
        "en": "Eggs (regular) (12)",
        "de": "Eier (normal) (12)"
    },
    "x13": {
        "en": "Local Cheese (1 lb)",
        "de": "Lokaler Käse (500g)"
    },
    "x14": {
        "en": "Chicken Fillets (1 lb)",
        "de": "Hähnchenfilets (500g)"
    },
    "x15": {
        "en": "Beef Round (1 lb) (or Equivalent Back Leg Red Meat)",
        "de": "Rindfleisch (500g) (oder Äquivalentes rotes Fleisch vom Hinterbein)"
    },
    "x16": {
        "en": "Apples (1 lb)",
        "de": "Äpfel (500g)"
    },
    "x17": {
        "en": "Banana (1 lb)",
        "de": "Banane (500g)"
    },
    "x18": {
        "en": "Oranges (1 lb)",
        "de": "Orangen (500g)"
    },
    "x19": {
        "en": "Tomato (1 lb)",
        "de": "Tomate (500g)"
    },
    "x20": {
        "en": "Potato (1 lb)",
        "de": "Kartoffel (500g)"
    },
    "x21": {
        "en": "Onion (1 lb)",
        "de": "Zwiebel (500g)"
    },
    "x22": {
        "en": "Lettuce (1 head)",
        "de": "Salat (1 Kopf)"
    },
    "x23": {
        "en": "Water (1.5 liter bottle)",
        "de": "Wasser (1,5 Liter Flasche)"
    },
    "x24": {
        "en": "Bottle of Wine (Mid-Range)",
        "de": "Flasche Wein (Mittelklasse)"
    },
    "x25": {
        "en": "Domestic Beer (0.5 liter bottle)",
        "de": "Inländisches Bier (0,5 Liter Flasche)"
    },
    "x26": {
        "en": "Imported Beer (12 oz small bottle)",
        "de": "Importiertes Bier (0,33 Liter Flasche)"
    },
    "x27": {
        "en": "Cigarettes 20 Pack (Marlboro)",
        "de": "Zigaretten 20er Pack (Marlboro)"
    },
    "x28": {
        "en": "One-way Ticket (Local Transport)",
        "de": "Einzelfahrschein (Lokaler Transport)"
    },
    "x29": {
        "en": "Monthly Pass (Regular Price)",
        "de": "Monatskarte (Regulärer Preis)"
    },
    "x30": {
        "en": "Taxi Start (Normal Tariff)",
        "de": "Taxi Start (Normaler Tarif)"
    },
    "x31": {
        "en": "Taxi 1 mile (Normal Tariff)",
        "de": "Taxi 1 km (Normaler Tarif)"
    },
    "x32": {
        "en": "Taxi 1 hour Waiting (Normal Tariff)",
        "de": "Taxi 1 Stunde Warten (Normaler Tarif)"
    },
    "x33": {
        "en": "Gasoline (1 gallon)",
        "de": "Benzin (3,78 Liter)"
    },
    "x34": {
        "en": "Volkswagen Golf 1.4 90 KW Trendline (Or Equivalent New Car)",
        "de": "Volkswagen Golf 1.4 90 KW Trendline (Oder Äquivalentes Neuwagen)"
    },
    "x35": {
        "en": "Toyota Corolla Sedan 1.6l 97kW Comfort (Or Equivalent New Car)",
        "de": "Toyota Corolla Sedan 1.6l 97kW Comfort (Oder Äquivalentes Neuwagen)"
    },
    "x36": {
        "en": "Basic (Electricity, Heating, Cooling, Water, Garbage) for 915 sq ft Apartment",
        "de": "Grundversorgung (Strom, Heizung, Kühlung, Wasser, Müll) für 85m2 Wohnung"
    },
    "x37": {
        "en": "Mobile Phone Monthly Plan with Calls and 10GB+ Data",
        "de": "Mobilfunk Monatsplan mit Anrufen und 10GB+ Daten"
    },
    "x38": {
        "en": "Internet (60 Mbps or More, Unlimited Data, Cable/ADSL)",
        "de": "Internet (60 Mbps oder mehr, Unbegrenzte Daten, Kabel/ADSL)"
    },
    "x39": {
        "en": "Fitness Club, Monthly Fee for 1 Adult",
        "de": "Fitnessclub, Monatsgebühr für 1 Erwachsenen"
    },
    "x40": {
        "en": "Tennis Court Rent (1 Hour on Weekend)",
        "de": "Tennisplatz Miete (1 Stunde am Wochenende)"
    },
    "x41": {
        "en": "Cinema, International Release, 1 Seat",
        "de": "Kino, Internationaler Film, 1 Sitzplatz"
    },
    "x42": {
        "en": "Preschool (or Kindergarten), Full Day, Private, Monthly for 1 Child",
        "de": "Kindergarten (oder Vorschule), Ganztags, Privat, Monatlich für 1 Kind"
    },
    "x43": {
        "en": "International Primary School, Yearly for 1 Child",
        "de": "Internationale Grundschule, Jährlich für 1 Kind"
    },
    "x44": {
        "en": "1 Pair of Jeans (Levis 501 Or Similar)",
        "de": "1 Paar Jeans (Levis 501 Oder Ähnlich)"
    },
    "x45": {
        "en": "1 Summer Dress in a Chain Store (Zara, H&M, ...)",
        "de": "1 Sommerkleid in einer Kette (Zara, H&M, ...)"
    },
    "x46": {
        "en": "1 Pair of Nike Running Shoes (Mid-Range)",
        "de": "1 Paar Nike Laufschuhe (Mittelklasse)"
    },
    "x47": {
        "en": "1 Pair of Men Leather Business Shoes",
        "de": "1 Paar Herren Lederschuhe (Business)"
    },
    "x48": {
        "en": "Apartment (1 bedroom) in City Centre",
        "de": "Wohnung (1 Schlafzimmer) im Stadtzentrum"
    },
    "x49": {
        "en": "Apartment (1 bedroom) Outside of Centre",
        "de": "Wohnung (1 Schlafzimmer) außerhalb des Zentrums"
    },
    "x50": {
        "en": "Apartment (3 bedrooms) in City Centre",
        "de": "Wohnung (3 Schlafzimmer) im Stadtzentrum"
    },
    "x51": {
        "en": "Apartment (3 bedrooms) Outside of Centre",
        "de": "Wohnung (3 Schlafzimmer) außerhalb des Zentrums"
    },
    "x52": {
        "en": "Price per Square Feet to Buy Apartment in City Centre",
        "de": "Preis pro Quadratmeter für Wohnungskauf im Stadtzentrum"
    },
    "x53": {
        "en": "Price per Square Feet to Buy Apartment Outside of Centre",
        "de": "Preis pro Quadratmeter für Wohnungskauf außerhalb des Zentrums"
    },
    "x54": {
        "en": "Average Monthly Net Salary (After Tax)",
        "de": "Durchschnittliches Monatsnettoeinkommen (Nach Steuern)"
    },
    "x55": {
        "en": "Mortgage Interest Rate in Percentages (%), Yearly, for 20 Years Fixed-Rate",
        "de": "Hypothekenzins in Prozent (%), Jährlich, für 20 Jahre Festzins"
    }
}

# -------------------------------
# HELPERS
# -------------------------------
def normalize_string(s: str) -> str:
    """Normalize string by replacing hyphens with spaces and converting to lowercase."""
    return s.strip().lower().replace("-", " ")

def load_and_clean_csv() -> pd.DataFrame:
    """Load CSV and replace NaN/inf with None."""
    if not CSV_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail="Dataset not found. Run `python scripts/update_dataset.py` first."
        )
    df = pd.read_csv(CSV_PATH)
    df = df.replace([np.nan, np.inf, -np.inf], None)
    return df

# -------------------------------
# ROUTES
# -------------------------------

@app.get("/")
async def root():
    """Root endpoint for Render health check."""
    return {"message": "Global Cost of Living API is live!", "status": "ready"}

@app.get("/health")
async def health():
    """Detailed health check."""
    dataset_ok = os.path.exists(CSV_PATH)
    return {
        "status": "healthy" if dataset_ok else "unhealthy",
        "dataset_loaded": dataset_ok,
        "endpoints": ["/city_data (POST)", "/health (GET)"]
    }

@app.post("/city_data")
async def get_city_data(request: Request):
    """
    Return cost of living data for a city in a specific country.
    
    Body:
    {
        "city": "Paris",
        "country": "France",
        "language": "en"  # or "de" for German
    }
    """
    body = await request.json()

    city = body.get("city")
    country = body.get("country")
    language = body.get("language", "en").lower()  # Default to English

    # Validate inputs
    if not city or not isinstance(city, str):
        raise HTTPException(status_code=400, detail="Missing or invalid 'city' field.")
    if not country or not isinstance(country, str):
        raise HTTPException(status_code=400, detail="Missing or invalid 'country' field.")
    if language not in ["en", "de"]:
        raise HTTPException(status_code=400, detail="Unsupported language. Use 'en' or 'de'.")

    # Normalize city and country (replace hyphens with spaces, lowercase)
    city_key = normalize_string(city)
    country_key = normalize_string(country)

    # Load fresh data
    df = load_and_clean_csv()

    # Normalize dataset values for matching
    df_normalized = df.copy()
    df_normalized['city'] = df['city'].apply(normalize_string)
    df_normalized['country'] = df['country'].apply(normalize_string)

    # Filter by BOTH city and country (case-insensitive, hyphen-normalized)
    mask = (df_normalized['city'] == city_key) & (df_normalized['country'] == country_key)
    filtered = df.loc[mask]  # Use original df to preserve original values

    if filtered.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for city: '{city}' in country: '{country}'"
        )

    # Rename columns based on language
    rename_map = {k: v[language] for k, v in COLUMN_MAP.items()}
    result_df = filtered.rename(columns=rename_map)

    # Return as list of dicts (usually 1 row)
    return result_df.to_dict(orient="records")