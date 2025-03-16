import streamlit as st
import pandas as pd
from datetime import timedelta, datetime, date
import plotly.express as px
import numpy as np
from scipy import stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from auth import logout

# Authentication check at the very top
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.switch_page("pages/Login.py")

# Set page config
st.set_page_config(page_title="Dashboard - YouTube Analytics", layout="wide")

# Add logout button with a unique key
if st.sidebar.button("Logout", key="dashboard_logout"):
    st.session_state.authenticated = False
    st.session_state.user_name = None
    st.switch_page("streamlit_app.py")

# Display welcome message
st.sidebar.markdown(f"Welcome, {st.session_state.user_name}")

# Helper functions
@st.cache_data
def load_data():
    data = pd.read_csv("youtube_channel_data.csv")
    data['DATE'] = pd.to_datetime(data['DATE'])
    data['NET_SUBSCRIBERS'] = data['SUBSCRIBERS_GAINED'] - data['SUBSCRIBERS_LOST']
    return data

def custom_quarter(date):
    if isinstance(date, (datetime, pd.Timestamp)):
        month = date.month
        year = date.year
    else:  # Handle date objects
        month = date.month
        year = date.year
    
    if month in [2, 3, 4]:
        return pd.Period(year=year, quarter=1, freq='Q')
    elif month in [5, 6, 7]:
        return pd.Period(year=year, quarter=2, freq='Q')
    elif month in [8, 9, 10]:
        return pd.Period(year=year, quarter=3, freq='Q')
    else:  # month in [11, 12, 1]
        return pd.Period(year=year if month != 1 else year-1, quarter=4, freq='Q')

def aggregate_data(df, freq):
    if freq == 'Q':
        df = df.copy()
        df['CUSTOM_Q'] = df['DATE'].apply(custom_quarter)
        df_agg = df.groupby('CUSTOM_Q').agg({
            'VIEWS': 'sum',
            'WATCH_HOURS': 'sum',
            'NET_SUBSCRIBERS': 'sum',
            'LIKES': 'sum',
            'COMMENTS': 'sum',
            'SHARES': 'sum',
        })
        return df_agg
    else:
        return df.resample(freq, on='DATE').agg({
            'VIEWS': 'sum',
            'WATCH_HOURS': 'sum',
            'NET_SUBSCRIBERS': 'sum',
            'LIKES': 'sum',
            'COMMENTS': 'sum',
            'SHARES': 'sum',
        })

def get_weekly_data(df):
    return aggregate_data(df, 'W-MON')

def get_monthly_data(df):
    return aggregate_data(df, 'M')

def get_quarterly_data(df):
    return aggregate_data(df, 'Q')

def format_with_commas(number):
    return f"{number:,}"

def create_metric_chart(df, column, color, chart_type, height=150, time_frame='Daily'):
    chart_data = df[[column]].copy()
    if time_frame == 'Quarterly':
        # Convert Period index to string format
        chart_data.index = chart_data.index.astype(str)
    elif not isinstance(chart_data.index, pd.DatetimeIndex):
        chart_data.index = pd.to_datetime(chart_data.index)
    
    if chart_type == 'Bar':
        st.bar_chart(chart_data, y=column, color=color, height=height)
    elif chart_type == 'Area':
        st.area_chart(chart_data, y=column, color=color, height=height)
    elif chart_type == 'Line':
        st.line_chart(chart_data, y=column, color=color, height=height)
    elif chart_type == 'Scatter':
        # For scatter plot, we need to use Plotly
        fig = px.scatter(chart_data, y=column)
        fig.update_traces(marker=dict(color=color))
        fig.update_layout(height=height, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

def is_period_complete(date, freq):
    today = datetime.now()
    if freq == 'D':
        return date.date() < today.date() if isinstance(date, pd.Timestamp) else date < today.date()
    elif freq == 'W':
        return date + timedelta(days=6) < today
    elif freq == 'M':
        if isinstance(date, pd.Period):
            date = date.to_timestamp()
        next_month = date.replace(day=28) + timedelta(days=4)
        return next_month.replace(day=1) <= today
    elif freq == 'Q':
        if isinstance(date, pd.Period):
            return date < pd.Period(today, freq='Q')
        current_quarter = custom_quarter(today)
        return date < current_quarter

def calculate_delta(df, column):
    if len(df) < 2:
        return 0, 0
    current_value = df[column].iloc[-1]
    previous_value = df[column].iloc[-2]
    delta = current_value - previous_value
    delta_percent = (delta / previous_value) * 100 if previous_value != 0 else 0
    return delta, delta_percent

def display_metric(col, title, value, df, column, color, time_frame):
    with col:
        with st.container(border=True):
            delta, delta_percent = calculate_delta(df, column)
            delta_str = f"{delta:+,.0f} ({delta_percent:+.2f}%)"
            st.metric(title, format_with_commas(value), delta=delta_str)
            create_metric_chart(df, column, color, time_frame=time_frame, chart_type=chart_selection)
            
            last_period = df.index[-1]
            freq = {'Daily': 'D', 'Weekly': 'W', 'Monthly': 'M', 'Quarterly': 'Q'}[time_frame]
            if not is_period_complete(last_period, freq):
                st.caption(f"Note: The last {time_frame.lower()[:-2] if time_frame != 'Daily' else 'day'} is incomplete.")

def calculate_performance_metrics(df):
    metrics = {
        "Average Views per Day": df['VIEWS'].mean(),
        "Peak Views": df['VIEWS'].max(),
        "Average Watch Hours": df['WATCH_HOURS'].mean(),
        "Subscriber Growth Rate": (df['NET_SUBSCRIBERS'].sum() / len(df)) * 100,
        "Engagement Rate": ((df['LIKES'].sum() + df['COMMENTS'].sum()) / df['VIEWS'].sum()) * 100,
        "Best Performing Day": df['VIEWS'].idxmax().strftime('%Y-%m-%d'),
    }
    return metrics

def calculate_growth_metrics(df):
    metrics = {}
    
    # Calculate day-over-day growth rates
    for column in ['VIEWS', 'WATCH_HOURS', 'NET_SUBSCRIBERS']:
        pct_change = df[column].pct_change() * 100
        metrics[f"{column}_avg_growth"] = pct_change.mean()
        metrics[f"{column}_volatility"] = pct_change.std()
    
    return metrics

def create_distribution_plot(df, metric):
    fig = make_subplots(rows=2, cols=1, subplot_titles=(f'{metric} Distribution', f'{metric} Q-Q Plot'))
    
    # Histogram
    fig.add_trace(
        go.Histogram(x=df[metric], name='Distribution', nbinsx=30),
        row=1, col=1
    )
    
    # Q-Q Plot
    qq = stats.probplot(df[metric], dist="norm")
    fig.add_trace(
        go.Scatter(x=qq[0][0], y=qq[0][1], mode='markers', name='Q-Q Plot'),
        row=2, col=1
    )
    
    fig.update_layout(height=600, showlegend=False)
    return fig

def create_boxplot(df, metrics):
    fig = go.Figure()
    for metric in metrics:
        # Normalize the data for comparison
        normalized_data = (df[metric] - df[metric].mean()) / df[metric].std()
        fig.add_trace(go.Box(y=normalized_data, name=metric))
    
    fig.update_layout(
        title="Normalized Metric Distributions",
        yaxis_title="Standard Deviations from Mean"
    )
    return fig

# Load data
df = load_data()

# Set up input widgets
st.sidebar.image("images/YouTube_logo_(2017).png", width=200)

with st.sidebar:
    st.title("YouTube Channel Dashboard")
    
    st.header("⚙️ Controls")
    
    max_date = df['DATE'].max().date()
    min_date = df['DATE'].min().date()
    default_start_date = max_date - timedelta(days=365)  # Show a year by default
    default_end_date = max_date
    
    start_date = st.date_input("Start date", default_start_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("End date", default_end_date, min_value=min_date, max_value=max_date)
    
    if start_date > end_date:
        st.error("Error: End date must be after start date.")
        st.stop()

    time_frame = st.selectbox("Select time frame",
                              ("Daily", "Weekly", "Monthly", "Quarterly"),
    )
    chart_selection = st.selectbox(
        "Select a chart type",
        ("Bar", "Area", "Line", "Scatter"),
        help="Choose how to visualize your metrics"
    )

    # Add chart customization options
    if chart_selection == "Scatter":
        st.caption("💡 Scatter plots are useful for identifying outliers and patterns")
    elif chart_selection == "Line":
        st.caption("💡 Line charts are great for showing trends over time")
    elif chart_selection == "Area":
        st.caption("💡 Area charts emphasize the magnitude of changes")
    elif chart_selection == "Bar":
        st.caption("💡 Bar charts are perfect for comparing discrete values")

    # Add to the sidebar section
    st.markdown("---")
    st.markdown("### ⚙️ Display Settings")
    
    # Theme selection
    theme = st.selectbox(
        "Color Theme",
        ["Default", "Dark", "Light"]
    )
    
    # Chart animation
    enable_animation = st.toggle("Enable Chart Animations", value=True)
    
    # Decimal precision
    decimal_places = st.slider("Decimal Places", 0, 4, 2)
    
    st.markdown("---")
    st.markdown("### 📱 Contact")
    st.markdown("[GitHub](https://github.com/yourusername)")
    st.markdown("[Twitter](https://twitter.com/yourusername)")

# Prepare data based on selected time frame
if time_frame == 'Daily':
    df_display = df.set_index('DATE')
elif time_frame == 'Weekly':
    df_display = get_weekly_data(df)
elif time_frame == 'Monthly':
    df_display = get_monthly_data(df)
elif time_frame == 'Quarterly':
    df_display = get_quarterly_data(df)

# Display Key Metrics
st.subheader("All-Time via Cursor Statistics")

metrics = [
    ("Total Subscribers", "NET_SUBSCRIBERS", '#29b5e8'),
    ("Total Views", "VIEWS", '#FF9F36'),
    ("Total Watch Hours", "WATCH_HOURS", '#D45B90'),
    ("Total Likes", "LIKES", '#7D44CF')
]

cols = st.columns(4)
for col, (title, column, color) in zip(cols, metrics):
    total_value = df[column].sum()
    display_metric(col, title, total_value, df_display, column, color, time_frame)

# Display Key Metrics
if df_display.empty:
    st.warning("No data available for the selected date range.")
    st.stop()

st.subheader("Selected Duration")

if time_frame == 'Quarterly':
    start_quarter = custom_quarter(start_date)
    end_quarter = custom_quarter(end_date)
    mask = (df_display.index >= start_quarter) & (df_display.index <= end_quarter)
else:
    mask = (df_display.index >= pd.Timestamp(start_date)) & (df_display.index <= pd.Timestamp(end_date))
df_filtered = df_display.loc[mask]

cols = st.columns(4)
for col, (title, column, color) in zip(cols, metrics):
    display_metric(col, title.split()[-1], df_filtered[column].sum(), df_filtered, column, color, time_frame)

# Add after the DataFrame display
st.subheader("🎯 Goal Tracking")

with st.expander("Set and Track Goals"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        goal_metric = st.selectbox(
            "Select Metric",
            ["VIEWS", "SUBSCRIBERS", "WATCH_HOURS", "LIKES"]
        )
        
    with col2:
        goal_value = st.number_input(
            "Goal Value",
            min_value=0,
            value=10000
        )
        
    with col3:
        goal_date = st.date_input(
            "Target Date",
            min_value=date.today()
        )
    
    # Calculate progress
    current_value = df_filtered[goal_metric].sum()
    progress = (current_value / goal_value) * 100
    
    st.progress(min(progress / 100, 1.0))
    st.metric(
        "Progress",
        f"{current_value:,.0f} / {goal_value:,.0f}",
        f"{progress:.1f}%"
    )

# DataFrame display
with st.expander('See DataFrame (Selected time frame)'):
    st.dataframe(df_filtered)

# Add this before the DataFrame display
st.subheader("📊 Channel Performance Analysis")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Key Performance Indicators")
    metrics = calculate_performance_metrics(df_filtered)
    for metric, value in metrics.items():
        if isinstance(value, (int, float)):
            if metric.endswith("Rate"):
                st.metric(metric, f"{value:.2f}%")
            else:
                st.metric(metric, f"{value:,.0f}")
        else:
            st.metric(metric, value)

with col2:
    st.markdown("### Trend Analysis")
    trend_metric = st.selectbox("Select metric to analyze", 
                              ["VIEWS", "WATCH_HOURS", "NET_SUBSCRIBERS", "LIKES"])
    
    # Calculate rolling average
    rolling_data = df_filtered[trend_metric].rolling(window=7).mean()
    fig = px.line(rolling_data, title=f'7-Day Rolling Average: {trend_metric}')
    st.plotly_chart(fig, use_container_width=True)

# Add after the Performance Analysis section
st.subheader("🔄 Metric Correlations")

correlation_metrics = ['VIEWS', 'WATCH_HOURS', 'NET_SUBSCRIBERS', 'LIKES', 'COMMENTS', 'SHARES']
correlation_matrix = df_filtered[correlation_metrics].corr()

fig = px.imshow(
    correlation_matrix,
    labels=dict(color="Correlation"),
    color_continuous_scale="RdBu",
    aspect="auto"
)
fig.update_layout(title="Correlation Heatmap")
st.plotly_chart(fig, use_container_width=True)

# Show strongest correlations
st.markdown("### Strongest Correlations")
correlations = []
for i in range(len(correlation_metrics)):
    for j in range(i+1, len(correlation_metrics)):
        correlations.append({
            'Metrics': f"{correlation_metrics[i]} vs {correlation_metrics[j]}",
            'Correlation': correlation_matrix.iloc[i,j]
        })

correlations_df = pd.DataFrame(correlations)
correlations_df = correlations_df.sort_values('Correlation', key=abs, ascending=False)
st.dataframe(correlations_df)

# Add this new section before the DataFrame display
st.subheader("📈 Advanced Analytics Dashboard")

# Create tabs for different analyses
tab1, tab2, tab3 = st.tabs(["Growth Analysis", "Statistical Distribution", "Seasonal Patterns"])

with tab1:
    st.markdown("### Growth Metrics")
    growth_metrics = calculate_growth_metrics(df_filtered)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Average Daily Growth Rates")
        for metric in ['VIEWS', 'WATCH_HOURS', 'NET_SUBSCRIBERS']:
            st.metric(
                f"{metric.replace('_', ' ')} Growth",
                f"{growth_metrics[f'{metric}_avg_growth']:.2f}%",
                help="Average day-over-day growth rate"
            )
    
    with col2:
        st.markdown("#### Metric Volatility")
        for metric in ['VIEWS', 'WATCH_HOURS', 'NET_SUBSCRIBERS']:
            st.metric(
                f"{metric.replace('_', ' ')} Volatility",
                f"{growth_metrics[f'{metric}_volatility']:.2f}%",
                help="Standard deviation of daily growth rates"
            )
    
    # Growth trends visualization
    st.markdown("### Growth Trends")
    growth_metric = st.selectbox(
        "Select metric for growth analysis",
        ['VIEWS', 'WATCH_HOURS', 'NET_SUBSCRIBERS']
    )
    
    growth_data = df_filtered[growth_metric].pct_change() * 100
    fig = px.line(growth_data, title=f'{growth_metric} Daily Growth Rate (%)')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Statistical Distribution Analysis")
    
    dist_metric = st.selectbox(
        "Select metric to analyze",
        ['VIEWS', 'WATCH_HOURS', 'NET_SUBSCRIBERS', 'LIKES', 'COMMENTS']
    )
    
    # Create and display distribution plots
    dist_fig = create_distribution_plot(df_filtered, dist_metric)
    st.plotly_chart(dist_fig, use_container_width=True)
    
    # Add statistical tests
    st.markdown("#### Statistical Tests")
    col1, col2 = st.columns(2)
    
    with col1:
        # Normality test
        stat, p_value = stats.normaltest(df_filtered[dist_metric])
        st.metric("Normality Test p-value", f"{p_value:.4f}")
        if p_value < 0.05:
            st.caption("❗ Data is not normally distributed (p < 0.05)")
        else:
            st.caption("✅ Data appears normally distributed (p >= 0.05)")
    
    with col2:
        # Basic statistics
        st.metric("Skewness", f"{stats.skew(df_filtered[dist_metric]):.4f}")
        st.metric("Kurtosis", f"{stats.kurtosis(df_filtered[dist_metric]):.4f}")

with tab3:
    st.markdown("### Seasonal Pattern Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        # Day of week analysis
        df_filtered['DayOfWeek'] = df_filtered.index.dayofweek
        dow_avg = df_filtered.groupby('DayOfWeek')['VIEWS'].mean()
        fig = px.bar(
            x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            y=dow_avg.values,
            title="Average Views by Day of Week"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Month analysis
        df_filtered['Month'] = df_filtered.index.month
        month_avg = df_filtered.groupby('Month')['VIEWS'].mean()
        fig = px.bar(
            x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            y=month_avg.values,
            title="Average Views by Month"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Box plot comparison
    st.markdown("### Metric Comparisons")
    comparison_fig = create_boxplot(df_filtered, ['VIEWS', 'WATCH_HOURS', 'NET_SUBSCRIBERS', 'LIKES'])
    st.plotly_chart(comparison_fig, use_container_width=True) 