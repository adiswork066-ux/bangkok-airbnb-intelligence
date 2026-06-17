# Bangkok Airbnb Market Intelligence App

A live, interactive market intelligence web app built on **50,000+ real Airbnb listings** from Bangkok. Explore pricing trends, geospatial heatmaps, and host behaviour patterns — all in a deployed web application.

🔗 **[Live App](https://bangkok-airbnb-intelligence-byadi.streamlit.app/)** &nbsp;|&nbsp; ⭐ **[Give it a star if you find it useful!](#)**

---

## App Preview

| Market Overview | Price Heatmap | Host Intelligence |
|:-:|:-:|:-:|
| Neighbourhood filters, KPI cards, room type charts | Interactive Folium heatmap embedded in app | Business vs individual host breakdown |

---

## Key Findings

After analysing 50,000+ listings across 80+ Bangkok neighbourhoods:

- 🏡 **Entire-home listings command a 2x+ price premium** over private rooms
- ⭐ **Superhosts earn ~18% more per night** on average than regular hosts
- 📍 **Silom and Sukhumvit** are the most expensive neighbourhoods by median price
- 🏢 **Business hosts** (10+ listings) account for a significant share of supply but price similarly to individuals
- 📉 Higher review counts do **not** strongly correlate with higher prices — quality matters more than volume

---

## Geospatial Visualisations

Three interactive maps built with **Folium**:

| Map | Type | Description |
|-----|------|-------------|
| Price Heatmap | HeatMap | Red = expensive zones, blue = affordable |
| Listing Clusters | MarkerCluster | Density of listings across the city |
| Superhost Distribution | CircleMarker | Gold = superhosts, blue = regular hosts |

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas | Data cleaning & analysis |
| Folium | Interactive geospatial maps |
| Streamlit | Web app framework |
| Matplotlib / Seaborn | Charts and visualisations |
| Streamlit Cloud | Free deployment & hosting |
| GitHub | Version control |

---

## Project Structure

```
bangkok-airbnb-intelligence/
│
├── app.py                  # Main Streamlit application
├── listings_clean.csv      # Cleaned dataset (50,000+ rows)
├── requirements.txt        # Python dependencies
└── README.md
```

---

##  Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/bangkok-airbnb-intelligence.git
cd bangkok-airbnb-intelligence
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

---

##  Data Source

**Inside Airbnb** — [insideairbnb.com/get-the-data](http://insideairbnb.com/get-the-data)

Real Airbnb listing data scraped directly from the platform. Not a cleaned Kaggle dataset — this is the actual, messy, real-world data including prices, neighbourhood details, host information, availability calendars, and review scores.

**Raw dataset stats:**
- 70+ columns
- 50,000+ rows
- 80+ Bangkok neighbourhoods

---

## 🧹 Data Cleaning Decisions

| Issue | Decision |
|-------|----------|
| Price stored as `$1,234.00` string | Stripped `$` and `,`, converted to float |
| Listings above $1,000/night | Removed as outliers — skewed analysis |
| Null values in review columns | Kept rows, handled per-analysis with `.dropna()` |
| `host_is_superhost` as `t`/`f` | Mapped to readable labels for display |

---

##  App Pages

**Page 1 — Market Overview**
- Neighbourhood dropdown + price range slider + minimum nights filter
- KPI cards: total listings, avg price, median review score, superhost %
- Room type distribution bar chart
- Top 10 most expensive neighbourhoods table

**Page 2 — Interactive Map**
- Toggle between Price Heatmap and Listing Clusters
- Neighbourhood filter that updates the map in real time
- Top 10 listings table for selected area

**Page 3 — Host Intelligence**
- Business vs individual host pie chart
- Median price comparison by host type
- Superhost price premium metric card
- Top 10 hosts by listing count with superhost badge

---

## 👤 Author

**Adi**
- 📧 adiswork066@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/yourprofile)
- 🐙 [GitHub](https://github.com/adiswork066-ux)
