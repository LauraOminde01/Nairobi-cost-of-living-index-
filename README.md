# Nairobi Cost of Living Index

A data dashboard tracking the real cost of living in Nairobi using World Bank, EPRA, and KNBS data - combining food prices, fuel costs, rent, transport, and electricity into a single monthly index with a 6-month forecast.

## The Problem

Kenya's Consumer Price Index has risen 167.8% since 2010. A Nairobi household that spent KES 18,207 per month in January 2020 now needs KES 29,223 to maintain the same standard of living - a 60.5% increase in just four years. Yet most Kenyans have no single tool that shows them what is driving that increase, which category is rising fastest, and what to expect in the coming months.

## Live Demo

https://cost-index.streamlit.app/

## What It Shows

Five pages of analysis:

**Overview** -headline cost of living figure, total increase since 2020, and full trend chart with 6-month forecast overlay

**Cost Breakdown** -pie chart and trend lines showing how costs split across housing, food, transport, and utilities

**Fuel Prices** - EPRA monthly pump prices for petrol, diesel, and kerosene in Nairobi from 2020 to 2024

**CPI History** - World Bank annual inflation rates and cumulative price increases since 2010

**Forecast** - 6-month cost of living projection with monthly detail and honest limitation disclosure

## Key Findings

- Cost of living rose **60.5%** between January 2020 and December 2024
- Current monthly cost for a typical middle-income Nairobi household: **KES 29,223**
- Housing is the dominant expense at **63.5%** of monthly costs (KES 18,560)
- Food accounts for **20%** (KES 5,835), transport **11.7%** (KES 3,425), utilities **4.8%** (KES 1,403)
- Kenya CPI has risen **167.8%** since 2010
- Worst inflation years were 2011 (14.0%) and 2022-2023 (both around 7.7%)
- Forecast: costs expected to reach KES 29,707 by June 2025, a further 1.7% increase

## Data Sources

| Source | Data | Coverage |
|---|---|---|
| World Bank Open Data API | Kenya Consumer Price Index | 2010-2025 |
| EPRA (Energy and Petroleum Regulatory Authority) | Monthly pump prices for Nairobi | 2020-2024 |
| KNBS Consumer Price Monitoring | Food and household basket prices | 2020-2024 |

All data sources are free and publicly available. No API keys required.

## The Monthly Basket

Monthly costs are calculated for a realistic household of 2-3 adults:

| Item | Quantity | Category |
|---|---|---|
| Unga (maize flour) | 8 x 2kg packets | Food |
| Rice | 4kg | Food |
| Cooking oil | 2 litres | Food |
| Milk | 20 litres | Food |
| Tomatoes | 8kg | Food |
| Matatu fares | 52 trips | Transport |
| Electricity | Monthly bill | Utilities |
| Rent (1-bedroom, Embakasi area) | Monthly | Housing |

## Forecasting Approach

A linear trend model is fitted to 60 months of historical basket data and extended 6 months forward. This captures the long-term cost trajectory but cannot anticipate sudden shocks such as fuel price hikes, drought, or exchange rate movements. All forecasts include an explicit uncertainty disclaimer in the dashboard.

## Tech Stack

- Data collection: World Bank Open Data API, requests, pandas
- Analysis: NumPy, scikit-learn (LinearRegression)
- Dashboard: Streamlit, Plotly
- Language: Python 3.13

## Limitations

- Food and transport prices in the basket are modeled estimates informed by KNBS monitoring data, not direct monthly scrapes from supermarkets
- Rent figures represent middle-income areas such as Embakasi and will differ significantly by neighborhood
- The linear forecast assumes no structural breaks in the cost trend and cannot anticipate policy changes or economic shocks
- Household consumption quantities are illustrative averages for a 2-3 person household
