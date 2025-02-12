# importing the appropriate libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# reading the data
df = pd.read_csv('https://storage.googleapis.com/courses_data/Assignment%20CSV/finance_liquor_sales.csv')

# cleaning the data
df.dropna(inplace = True)

# DATA ANALYSIS
# formatting the date to datetime
df['date'] = pd.to_datetime(df['date'])

#  identifying the predominant item per zipcode
grouped_items = df.groupby(['zip_code', 'item_description'])['bottles_sold'].sum().reset_index()
predominant_items = grouped_items.groupby(['zip_code', 'item_description'])['bottles_sold'].idxmax()

# calculating the proportion of sales for each store between 2016 and 2019
filtered_df = df[(df['date'].dt.year >= 2016) & (df['date'].dt.year <= 2019)]

grouped_sales = filtered_df.groupby(['store_name', 'date'])['sale_dollars'].sum().reset_index()

total_sales_per_store = grouped_sales.groupby('store_name')['sale_dollars'].sum().reset_index()
total_sales_per_store = total_sales_per_store.rename(columns = {'sale_dollars': 'total_sales'})

grouped_sales = pd.merge(grouped_sales,total_sales_per_store, on = 'store_name')
grouped_sales['sales_proportion'] = grouped_sales['sale_dollars'] / grouped_sales['total_sales']

# printing analytical report
print('The Data Analysis is:')
print()
print('Predominant items per zip_code')
print(predominant_items)
print()
print('proportion of sales for each store between 2016 and 2019')
print(grouped_sales[['store_name', 'date', 'sales_proportion']])
print()

# DATA VISUALIZATION
# calculating the percentage of sales per store
sales_per_store = df.groupby('store_name')['sale_dollars'].sum().reset_index()
total_sales = sales_per_store['sale_dollars'].sum()
sales_per_store['percentage'] = (sales_per_store['sale_dollars'] / total_sales) * 100
print('The percentage of sales per store is:')
print(sales_per_store)

# creating a scatter plot showing the relationship between zip code and  bottles sold
plt.figure(figsize = (12, 6))
colors = np.random.rand(len(grouped_items))
plt.scatter(grouped_items['zip_code'], grouped_items['bottles_sold'], c = colors, cmap = 'viridis')
plt.colorbar(label = 'Color Scale')
plt.title('Bottles sold per zip code')
plt.xlabel('zip code')
plt.ylabel('Bottles sold')
plt.show()

# creating bar plot showing the sales percentage per store (top 15)
top_15_stores = sales_per_store.sort_values(by = 'percentage', ascending = False).head(15)
fig = px.bar(top_15_stores, x='percentage', y='store_name', orientation='h', title='Percentage Sales per Store')
fig.update_layout(showlegend=False)
fig.show()