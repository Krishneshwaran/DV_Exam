import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Define regions and product categories GLOBALLY
REGIONS = ['North', 'South', 'East', 'West']
CATEGORIES = ['Electronics', 'Furniture', 'Clothing']

# Set page configuration
st.set_page_config(layout="wide")

# Generate synthetic sales data
def generate_sales_data():
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate data for 2024
    data = []
    for year in [2024]:
        for month in range(1, 13):
            for region in REGIONS:
                for category in CATEGORIES:
                    # Generate sales with some randomness and regional/category variations
                    base_sales = np.random.randint(50000, 200000)
                    
                    # Add some seasonal and regional variations
                    if region == 'North':
                        base_sales *= 1.2  # North has higher sales
                    if category == 'Electronics':
                        base_sales *= 1.5  # Electronics more profitable
                    
                    # Seasonal adjustment
                    if month in [11, 12]:  # Holiday season boost
                        base_sales *= 1.3
                    elif month in [1, 2]:  # Post-holiday dip
                        base_sales *= 0.7
                    
                    # Create date
                    date = pd.Timestamp(year, month, np.random.randint(1, 29))
                    
                    data.append({
                        'Region': region,
                        'Product Category': category,
                        'Sales': base_sales,
                        'Year': year,
                        'Month': month,
                        'Date': date
                    })
    
    return pd.DataFrame(data)

# Generate the dataset
df = generate_sales_data()

# Dashboard Title
st.title("Sales Data Visualization Dashboard")

# Tabs for different visualizations
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Regional & Category Analysis", 
    "Sales Trends", 
    "Distribution & Correlation", 
    "Product Performance", 
    "Timeline Visualization"
])

with tab1:
    # 1. Bar Chart: Total Sales per Region
    st.subheader("1. Total Sales per Region (2024)")
    region_sales = df.groupby('Region')['Sales'].sum().reset_index()
    fig1 = px.bar(region_sales, x='Region', y='Sales', 
                  title='Total Sales by Region',
                  color='Region',
                  labels={'Sales': 'Total Sales ($)'})
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Pie Chart: Sales by Product Category
    st.subheader("2. Sales Percentage by Product Category")
    category_sales = df.groupby('Product Category')['Sales'].sum().reset_index()
    fig2 = px.pie(category_sales, values='Sales', names='Product Category', 
                  title='Sales Share by Product Category')
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    # 3. Line Chart: Monthly Sales Trends by Region
    st.subheader("3. Monthly Sales Trends by Region")
    monthly_regional_sales = df.groupby(['Region', 'Month'])['Sales'].sum().reset_index()
    fig3 = px.line(monthly_regional_sales, x='Month', y='Sales', color='Region',
                   title='Monthly Sales Trends by Region',
                   labels={'Sales': 'Total Sales ($)', 'Month': 'Month of 2024'})
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Scatter Plot: Electronics Sales by Month
    st.subheader("4. Electronics Sales Distribution")
    electronics_sales = df[df['Product Category'] == 'Electronics']
    fig4 = px.scatter(electronics_sales, x='Month', y='Sales', 
                      color='Region', 
                      title='Electronics Sales by Month and Region')
    st.plotly_chart(fig4, use_container_width=True)

with tab3:
    # 5. Stacked Bar Chart: Sales by Region and Product Category
    st.subheader("5. Sales by Region and Product Category")
    regional_category_sales = df.groupby(['Region', 'Product Category'])['Sales'].sum().reset_index()
    fig5 = px.bar(regional_category_sales, x='Region', y='Sales', color='Product Category',
                  title='Sales Breakdown by Region and Product Category')
    st.plotly_chart(fig5, use_container_width=True)

    # 6. Box Plot: Monthly Sales Distribution by Region
    st.subheader("6. Sales Distribution by Region")
    fig6 = px.box(df, x='Region', y='Sales', 
                  title='Sales Distribution Across Regions')
    st.plotly_chart(fig6, use_container_width=True)

with tab4:
    # 7. Tree Map: Sales by Product Category within Regions
    st.subheader("7. Sales Tree Map")
    regional_category_sales = df.groupby(['Region', 'Product Category'])['Sales'].sum().reset_index()
    fig7 = px.treemap(regional_category_sales, 
                      path=['Region', 'Product Category'], 
                      values='Sales',
                      title='Sales Distribution: Region and Product Category')
    st.plotly_chart(fig7, use_container_width=True)

    # 8. Heat Map: Sales Correlation
    st.subheader("8. Sales Correlation Heatmap")
    monthly_regional_sales = df.groupby(['Region', 'Month'])['Sales'].sum().unstack()
    fig8 = px.imshow(monthly_regional_sales, 
                     labels=dict(x="Month", y="Region", color="Sales"),
                     title='Sales Correlation: Months and Regions')
    st.plotly_chart(fig8, use_container_width=True)

with tab5:
    # 9. Area Chart: Cumulative Sales by Region
    st.subheader("9. Cumulative Sales by Region")
    monthly_regional_sales = df.groupby(['Region', 'Month'])['Sales'].sum().reset_index()
    monthly_regional_sales['Cumulative Sales'] = monthly_regional_sales.groupby('Region')['Sales'].cumsum()
    
    fig9 = px.area(monthly_regional_sales, x='Month', y='Cumulative Sales', color='Region',
                   title='Cumulative Sales Growth by Region')
    st.plotly_chart(fig9, use_container_width=True)

    # 10. Gantt Chart: Product Launch Timeline
    st.subheader("10. Product Launch Timeline")
    
    # Create mock launch dates
    launch_data = pd.DataFrame({
        'Product Category': CATEGORIES,
        'Launch Date': [
            pd.Timestamp('2024-01-15'),
            pd.Timestamp('2024-02-01'),
            pd.Timestamp('2024-03-10')
        ],
        'End Date': [
            pd.Timestamp('2024-12-31'),
            pd.Timestamp('2024-12-31'),
            pd.Timestamp('2024-12-31')
        ],
        'Region': REGIONS[:3]  # Use first 3 regions for launch timeline
    })
    
    fig10 = px.timeline(launch_data, x_start='Launch Date', x_end='End Date', 
                        y='Product Category', color='Region',
                        title='Product Launch Timeline Across Regions')
    st.plotly_chart(fig10, use_container_width=True)

# # Add a sidebar with dataset preview
# st.sidebar.header("Dataset Preview")
# st.sidebar.dataframe(df.head())

# Footer
st.markdown("---")
st.markdown("Sales Dashboard | Generated with Streamlit and Plotly")