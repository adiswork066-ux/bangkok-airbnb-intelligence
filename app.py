import pandas as pd
import numpy as np
import streamlit as st
import folium
import matplotlib.pyplot as plt
import seaborn as sns
from folium.plugins import HeatMap, MarkerCluster

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Bangkok Airbnb Intelligence",
    page_icon="🏠",
    layout="wide"
)

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('listings_clean.csv')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df[df['price'] < 50000].copy()
    return df

df = load_data()
neighbourhoods = sorted(df['neighbourhood_cleansed'].unique())

# ─────────────────────────────────────────
# CURRENCY TOGGLE (Sidebar)
# ─────────────────────────────────────────
st.sidebar.title("🏠 Bangkok Airbnb")

currency = st.sidebar.radio(
    "💱 Display Currency",
    ["฿ Thai Baht", "₹ Indian Rupee"]
)

THB_TO_INR = 2.5  # 1 THB ≈ 2.5 INR

def format_price(thb_amount):
    """Convert and format price based on selected currency."""
    if currency == "₹ Indian Rupee":
        return f"₹{thb_amount * THB_TO_INR:,.0f}"
    else:
        return f"฿{thb_amount:,.0f}"

def price_label():
    """Return the correct currency label for axis/column headers."""
    return "₹ INR" if currency == "₹ Indian Rupee" else "฿ THB"

def convert(amount):
    """Return numeric converted value."""
    if currency == "₹ Indian Rupee":
        return amount * THB_TO_INR
    return amount

# ─────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["📊 Market Overview", "🗺️ Interactive Map", "👤 Host Intelligence"]
)

# Show conversion rate as info
if currency == "₹ Indian Rupee":
    st.sidebar.info("1 Thai Baht = ₹2.5 INR\n(Rate as of June 2026)")

# ═══════════════════════════════════════════════════════
# PAGE 1 — MARKET OVERVIEW
# ═══════════════════════════════════════════════════════
if page == "📊 Market Overview":
    st.title("📊 Bangkok Airbnb Market Overview")
    st.markdown(f"Explore pricing and listing data by neighbourhood. Prices shown in **{currency}**.")

    # --- FILTERS ---
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_neighbourhood = st.selectbox(
            "Select Neighbourhood",
            ["All"] + neighbourhoods
        )
    with col2:
        max_price = int(convert(df['price'].max()))
        price_range = st.slider(
            f"Price Range ({price_label()} per night)",
            min_value=0,
            max_value=max_price,
            value=(0, int(convert(5000)))
        )
    with col3:
        min_nights = st.slider(
            "Maximum Minimum Nights",
            min_value=1,
            max_value=30,
            value=7
        )

    # --- FILTER DATA ---
    # Convert slider values back to THB for filtering
    if currency == "₹ Indian Rupee":
        price_min_thb = price_range[0] / THB_TO_INR
        price_max_thb = price_range[1] / THB_TO_INR
    else:
        price_min_thb = price_range[0]
        price_max_thb = price_range[1]

    filtered = df.copy()
    if selected_neighbourhood != "All":
        filtered = filtered[filtered['neighbourhood_cleansed'] == selected_neighbourhood]
    filtered = filtered[
        (filtered['price'] >= price_min_thb) &
        (filtered['price'] <= price_max_thb) &
        (filtered['minimum_nights'] <= min_nights)
    ]

    # --- KPI CARDS ---
    st.markdown("### Key Metrics")
    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Total Listings", f"{len(filtered):,}")
    k2.metric(
        f"Avg Price / Night ({price_label()})",
        format_price(filtered['price'].mean())
    )
    k3.metric(
        "Median Review Score",
        f"{filtered['review_scores_rating'].median():.1f}"
    )
    superhost_pct = (filtered['host_is_superhost'] == 't').mean() * 100
    k4.metric("Superhost %", f"{superhost_pct:.1f}%")

    # --- ROOM TYPE CHART ---
    st.markdown("### Room Type Distribution")
    room_counts = filtered['room_type'].value_counts()

    fig, ax = plt.subplots(figsize=(8, 4))
    room_counts.plot(kind='bar', ax=ax, color=['steelblue', 'coral', 'green', 'purple'])
    ax.set_title(f"Room Types — {selected_neighbourhood}")
    ax.set_ylabel("Number of Listings")
    ax.set_xlabel("")
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)

    # --- NEIGHBOURHOOD PRICE TABLE ---
    st.markdown("### Top 10 Most Expensive Neighbourhoods")
    top_n = (
        df.groupby('neighbourhood_cleansed')['price']
        .median()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_n.columns = ['Neighbourhood', 'Median Price']
    top_n['Median Price'] = top_n['Median Price'].apply(format_price)
    st.dataframe(top_n, use_container_width=True)


# ═══════════════════════════════════════════════════════
# PAGE 2 — INTERACTIVE MAP
# ═══════════════════════════════════════════════════════
elif page == "🗺️ Interactive Map":
    st.title("🗺️ Bangkok Price Heatmap")
    st.markdown(f"Red zones = expensive areas. Zoom in to explore. Prices in **{currency}**.")

    map_type = st.radio(
        "Select Map Type",
        ["Price Heatmap", "Listing Clusters"],
        horizontal=True
    )

    selected_n = st.selectbox("Filter by Neighbourhood", ["All"] + neighbourhoods)

    map_df = df.copy()
    if selected_n != "All":
        map_df = map_df[map_df['neighbourhood_cleansed'] == selected_n]

    # Build map
    m = folium.Map(location=[13.7563, 100.5018], zoom_start=11)

    if map_type == "Price Heatmap":
        heat_data = map_df[['latitude', 'longitude', 'price']].dropna().values.tolist()
        HeatMap(
            heat_data,
            min_opacity=0.3,
            radius=15,
            blur=10,
            gradient={0.2: 'blue', 0.5: 'lime', 0.8: 'orange', 1.0: 'red'}
        ).add_to(m)

    else:
        mc = MarkerCluster().add_to(m)
        for _, row in map_df.sample(min(2000, len(map_df))).iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=3,
                color='steelblue',
                fill=True,
                fill_opacity=0.5,
                popup=f"{format_price(row['price'])} | {row['neighbourhood_cleansed']}"
            ).add_to(mc)

    # Display map in Streamlit
    map_html = m._repr_html_()
    st.components.v1.html(map_html, height=500)

    # Top 10 listings table
    st.markdown("### Top 10 Listings in Selected Area")
    top_listings = (
        map_df[['name', 'neighbourhood_cleansed', 'room_type', 'price', 'review_scores_rating']]
        .sort_values('price', ascending=False)
        .head(10)
        .reset_index(drop=True)
    )
    top_listings['price'] = top_listings['price'].apply(format_price)
    top_listings.columns = ['Name', 'Neighbourhood', 'Room Type', f'Price ({price_label()})', 'Rating']
    st.dataframe(top_listings, use_container_width=True)


# ═══════════════════════════════════════════════════════
# PAGE 3 — HOST INTELLIGENCE
# ═══════════════════════════════════════════════════════
elif page == "👤 Host Intelligence":
    st.title("👤 Host Intelligence Dashboard")
    st.markdown(f"All prices in **{currency}**.")

    # Business vs Individual
    df['host_type'] = np.where(
        df['host_listings_count'] >= 10, 'Business Host', 'Individual Host'
    )

    st.markdown("### Business vs Individual Hosts")
    h1, h2 = st.columns(2)

    with h1:
        host_counts = df['host_type'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(host_counts, labels=host_counts.index,
               autopct='%1.1f%%', colors=['steelblue', 'coral'])
        ax.set_title("Host Type Breakdown")
        st.pyplot(fig)

    with h2:
        host_price = df.groupby('host_type')['price'].median().reset_index()
        host_price['price'] = host_price['price'].apply(convert)
        fig, ax = plt.subplots()
        ax.bar(host_price['host_type'], host_price['price'],
               color=['steelblue', 'coral'])
        ax.set_title("Median Price by Host Type")
        ax.set_ylabel(f"Price ({price_label()})")
        plt.tight_layout()
        st.pyplot(fig)

    # Superhost comparison
    st.markdown("### Superhost vs Regular Host")
    s1, s2 = st.columns(2)

    with s1:
        super_price = df.groupby('host_is_superhost')['price'].median()
        regular_price = super_price.get('f', 0)
        super_p = super_price.get('t', 0)
        premium = ((super_p - regular_price) / regular_price * 100).round(1)
        diff = convert(super_p - regular_price)
        symbol = "₹" if currency == "₹ Indian Rupee" else "฿"
        st.metric(
            "Superhost Price Premium",
            f"{premium}%",
            delta=f"{symbol}{diff:,.0f} more per night"
        )

    with s2:
        fig, ax = plt.subplots()
        labels = ['Regular Host', 'Superhost']
        values = [convert(regular_price), convert(super_p)]
        ax.bar(labels, values, color=['coral', 'gold'])
        ax.set_title("Median Price Comparison")
        ax.set_ylabel(f"Price ({price_label()})")
        plt.tight_layout()
        st.pyplot(fig)

    # Top 10 hosts by listing count
    st.markdown("### Top 10 Hosts by Number of Listings")
    top_hosts = (
        df.groupby('host_name')
        .agg(
            Total_Listings=('id', 'count'),
            Avg_Price=('price', 'mean'),
            Superhost=('host_is_superhost', lambda x: '⭐' if (x == 't').any() else '—')
        )
        .sort_values('Total_Listings', ascending=False)
        .head(10)
        .reset_index()
    )
    top_hosts['Avg_Price'] = top_hosts['Avg_Price'].apply(format_price)
    top_hosts.columns = ['Host Name', 'Total Listings', f'Avg Price ({price_label()})', 'Superhost']
    st.dataframe(top_hosts, use_container_width=True)
