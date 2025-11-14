# Global Cost of Living API

A FastAPI-based REST API that provides comprehensive cost of living data for cities and countries around the world. Data is sourced from a Kaggle dataset covering 55 different cost categories including food, transportation, housing, and entertainment.

## Features

- 🌍 **Global Coverage**: Access cost of living data for multiple countries and cities
- 📊 **Comprehensive Categories**: 55 cost categories including meals, transportation, housing, utilities, and more
- 🚀 **Fast & Scalable**: Built with FastAPI for high performance
- 📱 **RESTful API**: Simple POST endpoints for querying data
- 🔄 **Auto-Update**: Automated dataset refresh capability
- 💾 **Caching Support**: Built-in caching mechanisms for improved performance

## Getting Started

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd global-cost-of-living-api
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download the dataset:

```bash
python scripts/update_dataset.py
```

4. Run the API:

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### Health Check

```
GET /health
```

Returns the API status and dataset availability.

**Response:**

```json
{
  "status": "healthy",
  "dataset_exists": true
}
```

#### Get Country Data

```
POST /country_data
```

Returns all cost of living data for a specific country.

**Request Body:**

```json
{
  "country": "Japan"
}
```

**Response:**

```json
[
  {
    "country": "Japan",
    "city": "Tokyo",
    "Meal, Inexpensive Restaurant (USD)": 8.50,
    "Meal for 2 People, Mid-range Restaurant, Three-course (USD)": 50.00,
    ...
  }
]
```

#### Get City Data

```
POST /city_data
```

Returns cost of living data for a specific city in a country.

**Request Body:**

```json
{
  "city": "Paris",
  "country": "France"
}
```

**Response:**

```json
[
  {
    "country": "France",
    "city": "Paris",
    "Meal, Inexpensive Restaurant (USD)": 15.00,
    "Meal for 2 People, Mid-range Restaurant, Three-course (USD)": 60.00,
    ...
  }
]
```

## Data Categories

The API includes pricing data for 55 different categories, grouped by:

- **Dining & Groceries** (x1-x26): Restaurant meals, beverages, and grocery items
- **Transportation** (x28-x35): Public transport, taxi, and vehicle costs
- **Utilities & Services** (x36-x38): Electricity, phone plans, and internet
- **Leisure & Education** (x39-x43): Fitness, sports, cinema, and school costs
- **Clothing & Footwear** (x44-x47): Apparel and shoe prices
- **Housing** (x48-x53): Rental and property prices
- **Salaries** (x54-x55): Average salary and mortgage rates

## Project Structure

```
.
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── render.yaml              # Render deployment configuration
├── startup.sh               # Startup script
├── data/
│   └── cost-of-living_v2.csv # Dataset file
├── scripts/
│   └── update_dataset.py     # Script to fetch/update dataset
└── src/
    ├── main.py              # FastAPI application
    └── cache.py             # Caching utilities
```

## Dependencies

- **fastapi**: Web framework for building APIs
- **uvicorn**: ASGI server for FastAPI
- **pandas**: Data manipulation and analysis
- **kaggle**: API client for downloading datasets from Kaggle

## Deployment

This project is configured for deployment on [Render](https://render.com) using the provided `render.yaml` configuration.

### To deploy on Render:

1. Push the repository to GitHub
2. Connect your GitHub repository to Render
3. The `render.yaml` file will automatically configure the deployment
4. The API will be available at your Render deployment URL

## Development

### Running Locally with Auto-Reload

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Updating the Dataset

```bash
python scripts/update_dataset.py
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: No data found for specified country/city
- `500 Internal Server Error`: Dataset not found (run update_dataset.py)

## License

[Specify your license here]

## Contributing

[Add contribution guidelines here]

## Data Source

This project uses the [Cost of Living Dataset](https://www.kaggle.com/datasets/aniruddha3475/cost-of-living) from Kaggle.

## Support

For issues, questions, or suggestions, please open an issue in the repository.
