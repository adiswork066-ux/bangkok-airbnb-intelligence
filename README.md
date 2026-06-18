# Bangkok Airbnb Market Intelligence App

A live, interactive market intelligence web app built on **23,000+ real Airbnb listings** from Bangkok across **50 neighbourhoods** in which i made pricing trends, geospatial heatmaps, host behaviour patterns.

🔗 **[Live App](https://bangkok-airbnb-intelligence-byadi.streamlit.app/)** &nbsp;|&nbsp; 📂 **[GitHub](https://github.com/adiswork066-ux/bangkok-airbnb-intelligence)**

> I've built an EDA on real Airbnb data — not a cleaned Kaggle toy dataset.

---

## Key Findings

| Insight | Finding |
|---------|---------|
| > Room type premium | Entire homes cost **1.38x more** than private rooms (฿1,500 vs ฿1,089/night) |
| > Market structure | **53.6% of total supply** is controlled by business hosts (10+ listings) |
| > Price gap | Parthum Wan (฿2,248/night) is **3.9x more expensive** than Nong Khaem (฿581/night) |
| > Superhost premium | Superhosts earn **1.5% more per night** (ALMOST NEGLIGIBLE) (฿1,390 vs ฿1,370 median) |
| > Most expensive type | Hotel rooms command the highest median at **฿1,708/night** |

---

## Geospatial Visualisations

Also built three interactive maps with **Folium**:

| Map | Type | Description |
|-----|------|-------------|
| Price Heatmap | HeatMap | Red = expensive zones, blue = affordable |
| Listing Clusters | MarkerCluster | Density of listings across Bangkok |
| Superhost Distribution | CircleMarker | Gold = superhosts, blue = regular hosts |

---

## App Pages

**Page 1 — Market Overview**
- Neighbourhood dropdown + price range slider + minimum nights filter
- KPI cards: total listings, avg price, median review score, superhost %
- Room type distribution bar chart
- Top 10 most expensive neighbourhoods table

**Page 2 — Interactive Map**
- Toggle between Price Heatmap and Listing Clusters
- Neighbourhood filter that updates the map in real time
- Top 10 listings table for selected area with price and rating

**Page 3 — Host Intelligence**
- Business vs individual host pie chart and price comparison
- Superhost price premium metric card
- Median price comparison chart (Regular vs Superhost)
- Top 10 hosts by listing count with superhost badge

---

## Currency Toggle Feature

Switch between **Thai Baht (฿)** and **Indian Rupee (₹)** instantly from the sidebar. Every price — KPI cards, charts, tables, map popups — updates in real time.

```
1 Thai Baht = ₹2.5 Indian Rupee (Rate as of June 2026)
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Pandas | Data cleaning & analysis |
| Folium | Interactive geospatial maps |
| Streamlit | Web app framework & deployment |
| Matplotlib / Seaborn | Charts and visualisations |
| GitHub | Version control |
| Streamlit Cloud | Free hosting |

---

## Project Structure

```
bangkok-airbnb-intelligence/
│
├── app.py                  # Main Streamlit application (3 pages)
├── listings_clean.csv      # Cleaned dataset (23,000+ rows)
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Data Cleaning Decisions

| Issue | Decision |
|-------|----------|
| Price stored as `$1,234.00` string | Stripped `$` and `,`, converted to float |
| Currency mislabelled as USD | Identified as Thai Baht based on value ranges |
| Listings above ฿50,000/night | Removed as extreme outliers (only 37 listings) |
| Null values in review columns | Handled per-analysis with `.dropna()` |
| `host_is_superhost` as `t`/`f` | Mapped to readable labels for display |

---

## Data Source

**Inside Airbnb** — [insideairbnb.com/get-the-data](http://insideairbnb.com/get-the-data)

**Dataset stats:**
- 70+ raw columns
- 28,000+ raw rows → 23,234 after cleaning
- 50 neighbourhoods across Bangkok

---

## 👤 Author

**Adi**
- [LinkedIn](https://www.linkedin.com/in/aditya-chotalia-6a5bbb284?utm_source=share_via&utm_content=profile&utm_medium=member_ios)
- [GitHub](https://github.com/adiswork066-ux)
