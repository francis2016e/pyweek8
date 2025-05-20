import pandas as pd

# Load the dataset
file_path = "owid-covid-data.csv"  # ensure it's in your working directory
df = pd.read_csv(file_path)

df.columns
df.head()
df.info()
df.isnull().sum()


# Filter countries of interest
countries = ['Kenya', 'United States', 'India']
df = df[df['location'].isin(countries)]

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Drop rows with missing total_cases
df = df.dropna(subset=['total_cases'])

# Fill other columns
df[['new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations']] = df[
    ['new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations']
].fillna(0)


import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10,6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_cases'], label=country)

plt.title('Total COVID-19 Cases Over Time')
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend()
plt.tight_layout()
plt.show()


df['death_rate'] = df['total_deaths'] / df['total_cases']


latest = df[df['date'] == df['date'].max()]
sns.barplot(data=latest, x='location', y='total_cases')
plt.title('Total COVID-19 Cases by Country (Latest)')
plt.show()



plt.figure(figsize=(10,6))
for country in countries:
    subset = df[df['location'] == country]
    plt.plot(subset['date'], subset['total_vaccinations'], label=country)

plt.title('COVID-19 Vaccinations Over Time')
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend()
plt.show()


import plotly.express as px

# Latest vaccination data by country
latest_global = pd.read_csv("owid-covid-data.csv")
latest_global['date'] = pd.to_datetime(latest_global['date'])
latest_data = latest_global[latest_global['date'] == latest_global['date'].max()]
latest_data = latest_data[['iso_code', 'location', 'total_cases']].dropna()

fig = px.choropleth(latest_data,
                    locations="iso_code",
                    color="total_cases",
                    hover_name="location",
                    color_continuous_scale="Reds",
                    title="Total COVID-19 Cases by Country")
fig.show()
