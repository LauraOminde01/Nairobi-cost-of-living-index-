import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from pathlib import Path

st.set_page_config(
    page_title="Nairobi Cost of Living Index",
    layout="wide"
)

from pathlib import Path

@st.cache_data
def load_data():
    # Get the directory where app.py is located
    BASE_DIR = Path(__file__).resolve().parent

    # Path to the data folder
    DATA_DIR = BASE_DIR / "data"

    # Optional: Display path in Streamlit if files are not found
    if not DATA_DIR.exists():
        st.error(f"Data folder not found: {DATA_DIR}")
        st.stop()

    # Load CSV files
    cpi = pd.read_csv(DATA_DIR / "kenya_cpi.csv")
    fuel = pd.read_csv(DATA_DIR / "fuel_prices.csv")
    basket = pd.read_csv(DATA_DIR / "basket_features.csv")
    forecast = pd.read_csv(DATA_DIR / "cost_forecast.csv")

    # Convert date columns
    fuel["date"] = pd.to_datetime(fuel["date"])
    basket["date"] = pd.to_datetime(basket["date"])
    forecast["date"] = pd.to_datetime(forecast["date"])

    return cpi, fuel, basket, forecast

cpi, fuel, basket, forecast = load_data()

st.sidebar.title("Nairobi Cost of Living Index")
st.sidebar.markdown("Tracking the real cost of living in Nairobi using KNBS, EPRA, and World Bank data.")
st.sidebar.markdown("---")
st.sidebar.markdown("**Data Sources:**")
st.sidebar.markdown("- World Bank Kenya CPI")
st.sidebar.markdown("- EPRA Monthly Fuel Prices")
st.sidebar.markdown("- KNBS Consumer Basket")
st.sidebar.markdown("---")
st.sidebar.markdown("**Coverage:** 2020-2024")
st.sidebar.markdown("**Forecast:** 6 months ahead")

page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Cost Breakdown", "Fuel Prices", "CPI History", "Forecast", "Methodology"]
)

# ============================================
# PAGE 0 - OVERVIEW
# ============================================
if page == "Overview":
    st.title("Nairobi Cost of Living Index")
    st.markdown(
        "Tracking what it actually costs to live in Nairobi — combining food prices, "
        "fuel costs, rent, transport, and electricity into a single monthly index. "
        "Data covers 2020 to 2024 with a 6-month forecast."
    )
    st.markdown("---")

    latest = basket.iloc[-1]
    earliest = basket.iloc[0]
    total_increase = ((latest['monthly_total'] - earliest['monthly_total'])
                      / earliest['monthly_total'] * 100)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Monthly Cost (Latest)",
        f"KES {latest['monthly_total']:,.0f}",
        delta=f"+{total_increase:.1f}% since 2020"
    )
    col2.metric(
        "Housing",
        f"KES {latest['housing_cost']:,.0f}",
        delta=f"{latest['housing_cost']/latest['monthly_total']*100:.1f}% of total"
    )
    col3.metric(
        "Food",
        f"KES {latest['food_cost']:,.0f}",
        delta=f"{latest['food_cost']/latest['monthly_total']*100:.1f}% of total"
    )
    col4.metric(
        "Petrol (Nairobi)",
        f"KES {fuel['petrol_nairobi'].iloc[-1]:.2f}/L"
    )

    st.markdown("---")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=basket['date'],
        y=basket['monthly_total'],
        mode='lines',
        name='Monthly Cost',
        line=dict(color='#e74c3c', width=2),
        fill='tozeroy',
        fillcolor='rgba(231, 76, 60, 0.1)'
    ))
    fig.add_trace(go.Scatter(
        x=forecast['date'],
        y=forecast['forecasted_total'],
        mode='lines',
        name='Forecast',
        line=dict(color='orange', width=2, dash='dash')
    ))
    fig.update_layout(
        title='Nairobi Monthly Cost of Living 2020-2024 with 6-Month Forecast',
        xaxis_title='Date',
        yaxis_title='Monthly Cost (KES)',
        height=400,
        legend=dict(orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Key Findings")
    col1, col2 = st.columns(2)

    with col1:
        st.info(
            f"Cost of living in Nairobi has risen by **{total_increase:.1f}%** "
            f"between January 2020 and December 2024, from "
            f"KES {earliest['monthly_total']:,.0f} to KES {latest['monthly_total']:,.0f} "
            f"per month for a typical middle-income household."
        )

    with col2:
        cpi_increase = ((cpi['cpi'].iloc[-1] - cpi[cpi['year']==2010]['cpi'].iloc[0])
                        / cpi[cpi['year']==2010]['cpi'].iloc[0] * 100)
        st.warning(
            f"Kenya's Consumer Price Index has risen **{cpi_increase:.1f}%** since 2010, "
            f"meaning goods and services that cost KES 100 in 2010 now cost "
            f"KES {cpi['cpi'].iloc[-1]:.0f} in 2025."
        )

# ============================================
# PAGE 1 - COST BREAKDOWN
# ============================================
elif page == "Cost Breakdown":
    st.title("Monthly Cost Breakdown")
    st.markdown("How a typical Nairobi middle-income household spends their money each month.")

    latest = basket.iloc[-1]

    col1, col2 = st.columns(2)

    with col1:
        categories = ['Housing', 'Food', 'Transport', 'Utilities']
        values = [
            latest['housing_cost'],
            latest['food_cost'],
            latest['transport_cost'],
            latest['utilities_cost']
        ]
        colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']

        fig = px.pie(
            values=values,
            names=categories,
            color=categories,
            color_discrete_sequence=colors,
            title='Cost Distribution (Latest Month)'
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Breakdown in KES")
        breakdown_df = pd.DataFrame({
            'Category': categories,
            'Monthly Cost (KES)': [f"{v:,.0f}" for v in values],
            'Share': [f"{v/sum(values)*100:.1f}%" for v in values]
        })
        st.dataframe(breakdown_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("What drives the most cost?")
        st.error(
            f"Housing accounts for {latest['housing_cost']/latest['monthly_total']*100:.1f}% "
            f"of monthly expenses at KES {latest['housing_cost']:,.0f}. "
            "A Nairobi resident cannot meaningfully reduce costs without either "
            "relocating to a cheaper area or increasing income."
        )

    st.markdown("---")
    st.subheader("Category Trends Over Time")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=basket['date'], y=basket['housing_cost'],
                              name='Housing', line=dict(color='#e74c3c', width=2)))
    fig2.add_trace(go.Scatter(x=basket['date'], y=basket['food_cost'],
                              name='Food', line=dict(color='#3498db', width=2)))
    fig2.add_trace(go.Scatter(x=basket['date'], y=basket['transport_cost'],
                              name='Transport', line=dict(color='#2ecc71', width=2)))
    fig2.add_trace(go.Scatter(x=basket['date'], y=basket['utilities_cost'],
                              name='Utilities', line=dict(color='#f39c12', width=2)))
    fig2.update_layout(
        title='Cost Category Trends 2020-2024',
        xaxis_title='Date',
        yaxis_title='Monthly Cost (KES)',
        height=400,
        legend=dict(orientation='h')
    )
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# PAGE 2 - FUEL PRICES
# ============================================
elif page == "Fuel Prices":
    st.title("Nairobi Fuel Price Tracker")
    st.markdown("EPRA-published pump prices for Nairobi, showing petrol, diesel, and kerosene trends.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Petrol", f"KES {fuel['petrol_nairobi'].iloc[-1]:.2f}/L",
                delta=f"{((fuel['petrol_nairobi'].iloc[-1] - fuel['petrol_nairobi'].iloc[0])/fuel['petrol_nairobi'].iloc[0]*100):.1f}% since 2020")
    col2.metric("Diesel", f"KES {fuel['diesel_nairobi'].iloc[-1]:.2f}/L",
                delta=f"{((fuel['diesel_nairobi'].iloc[-1] - fuel['diesel_nairobi'].iloc[0])/fuel['diesel_nairobi'].iloc[0]*100):.1f}% since 2020")
    col3.metric("Kerosene", f"KES {fuel['kerosene_nairobi'].iloc[-1]:.2f}/L",
                delta=f"{((fuel['kerosene_nairobi'].iloc[-1] - fuel['kerosene_nairobi'].iloc[0])/fuel['kerosene_nairobi'].iloc[0]*100):.1f}% since 2020")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fuel['date'], y=fuel['petrol_nairobi'],
                             name='Petrol', line=dict(color='#e74c3c', width=2), mode='lines+markers'))
    fig.add_trace(go.Scatter(x=fuel['date'], y=fuel['diesel_nairobi'],
                             name='Diesel', line=dict(color='#3498db', width=2), mode='lines+markers'))
    fig.add_trace(go.Scatter(x=fuel['date'], y=fuel['kerosene_nairobi'],
                             name='Kerosene', line=dict(color='#f39c12', width=2), mode='lines+markers'))
    fig.update_layout(
        title='Nairobi Pump Prices 2020-2024 (KES per Litre)',
        xaxis_title='Date',
        yaxis_title='Price (KES/Litre)',
        height=450,
        legend=dict(orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Historical Fuel Price Data")
    st.dataframe(fuel.sort_values('date', ascending=False), use_container_width=True)

# ============================================
# PAGE 3 - CPI HISTORY
# ============================================
elif page == "CPI History":
    st.title("Kenya Consumer Price Index History")
    st.markdown("World Bank annual CPI data for Kenya, showing how prices have evolved since 2010.")

    cpi_2010 = cpi[cpi['year'] >= 2010].copy()
    cpi_2010['inflation_rate'] = cpi_2010['cpi'].pct_change() * 100
    cpi_2010['cumulative_increase'] = ((cpi_2010['cpi'] - cpi_2010['cpi'].iloc[0])
                                        / cpi_2010['cpi'].iloc[0] * 100)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            cpi_2010.dropna(subset=['inflation_rate']),
            x='year', y='inflation_rate',
            color='inflation_rate',
            color_continuous_scale='RdYlGn_r',
            title='Annual Inflation Rate (%)',
            labels={'inflation_rate': 'Inflation Rate (%)'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.line(
            cpi_2010, x='year', y='cumulative_increase',
            title='Cumulative Price Increase Since 2010 (%)',
            labels={'cumulative_increase': 'Cumulative Increase (%)'}
        )
        fig2.update_traces(line=dict(color='#e74c3c', width=2))
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("CPI Data Table")
    st.dataframe(
        cpi_2010[['year', 'cpi', 'inflation_rate', 'cumulative_increase']].sort_values('year', ascending=False),
        use_container_width=True
    )

# ============================================
# PAGE 4 - FORECAST
# ============================================
elif page == "Forecast":
    st.title("6-Month Cost of Living Forecast")
    st.markdown(
        "Linear trend model forecasting Nairobi monthly costs for the next 6 months, "
        "based on historical basket data from 2020-2024."
    )

    current = basket['monthly_total'].iloc[-1]
    forecast_6m = forecast['forecasted_total'].iloc[-1]
    increase = ((forecast_6m - current) / current * 100)

    col1, col2, col3 = st.columns(3)
    col1.metric("Current Monthly Cost", f"KES {current:,.0f}")
    col2.metric("Forecast in 6 Months", f"KES {forecast_6m:,.0f}", delta=f"+{increase:.1f}%")
    col3.metric("Monthly Increase", f"KES {(forecast_6m-current)/6:,.0f}/month")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=basket['date'], y=basket['monthly_total'],
        mode='lines', name='Historical',
        line=dict(color='#3498db', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=forecast['date'], y=forecast['forecasted_total'],
        mode='lines+markers', name='Forecast',
        line=dict(color='orange', width=2, dash='dash')
    ))
    fig.add_vrect(
        x0=forecast['date'].iloc[0],
        x1=forecast['date'].iloc[-1],
        fillcolor='orange', opacity=0.05,
        annotation_text='Forecast Period'
    )
    fig.update_layout(
        title='Nairobi Cost of Living Forecast',
        xaxis_title='Date',
        yaxis_title='Monthly Cost (KES)',
        height=450,
        legend=dict(orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monthly Forecast Detail")
    forecast_display = forecast.copy()
    forecast_display['date'] = forecast_display['date'].dt.strftime('%B %Y')
    forecast_display['forecasted_total'] = forecast_display['forecasted_total'].apply(lambda x: f"KES {x:,.0f}")
    forecast_display.columns = ['Month', 'Forecasted Monthly Cost']
    st.dataframe(forecast_display, use_container_width=True, hide_index=True)

    st.warning(
        "This forecast uses a linear trend model and assumes current economic conditions continue. "
        "It cannot anticipate sudden shocks such as fuel price hikes, drought, or policy changes."
    )

# ============================================
# PAGE 5 - METHODOLOGY
# ============================================
elif page == "Methodology":
    st.title("Methodology and Data Sources")
    st.markdown("""
    ### Data Sources

    **World Bank Kenya CPI**
    Annual Consumer Price Index for Kenya from the World Bank Open Data API (no API key required).
    Base year 2010 = 100. Coverage: 2010-2025.

    **EPRA Fuel Prices**
    Monthly pump prices published by the Energy and Petroleum Regulatory Authority of Kenya.
    Covers petrol, diesel, and kerosene prices for Nairobi. Source: epra.co.ke.

    **KNBS Consumer Basket**
    Monthly cost estimates for a typical Nairobi middle-income household based on the Kenya
    National Bureau of Statistics consumer price monitoring framework, covering:
    - Food (unga, rice, cooking oil, milk, tomatoes)
    - Housing (1-bedroom rental, Embakasi area)
    - Transport (matatu fares)
    - Utilities (electricity)

    ### Cost of Living Index Construction
    Monthly costs are aggregated using realistic consumption quantities for a household of
    2-3 adults: 8 packets of unga, 4kg rice, 2L cooking oil, 20L milk, 8kg tomatoes,
    52 matatu trips, one month of electricity, and one month of rent.

    ### Forecasting
    A simple linear trend model is fitted to 60 months of historical basket data and
    extended 6 months forward. This approach captures the long-term cost trajectory
    but cannot anticipate sudden shocks.

    ### Honest Limitations
    - Food and transport prices in the basket are modeled estimates informed by KNBS
      monitoring data, not direct monthly scrapes
    - Rent figures represent middle-income areas and will differ significantly by neighborhood
    - The linear forecast assumes no structural breaks in the cost trend
    - Household consumption quantities are illustrative averages, not universal

    ### Why This Matters
    Kenya's CPI has risen 167.8% since 2010. A Nairobi household spending KES 18,207
    in January 2020 now needs KES 29,223 to maintain the same standard of living,
    a 60.5% increase in just 4 years. Housing alone consumes 63.5% of a typical
    monthly budget, leaving limited room for savings or investment.
    """)