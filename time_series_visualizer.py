import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]
df.index = pd.to_datetime(df.index)

def draw_line_plot():
    # Create copy of dataframe
    df_line = df.copy()

    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_line.index, df_line['value'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Modifying xticks to look more presentable
    x_tick_labels = df_line.index.strftime('%Y-%m').unique()[1::6]
    ax.xaxis.set_major_locator(mticker.MaxNLocator(len(x_tick_labels)-1))
    xtick_positions = ax.get_xticks().tolist()
    ax.xaxis.set_major_locator(mticker.FixedLocator(xtick_positions))
    ax.set_xticklabels(x_tick_labels)

    # Save image and return fig
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_monthly_avg = df.copy()

    # Group by year and month, then calculate the mean
    df_monthly_avg = df_monthly_avg.groupby([df_monthly_avg.index.year, df_monthly_avg.index.month]).mean()

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    df_monthly_avg.unstack().plot(kind='bar', ax=ax)
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', loc='upper left', labels=['January', 'February', 'March',
                                                         'April', 'May', 'June', 'July',
                                                         'August', 'September', 'October',
                                                         'November', 'December'])

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Create copy of dataframe
    df_box = df.copy()

    # Reset index to convert date index to a regular column
    df_box.reset_index(inplace=True)

    # Extract year and month from the 'date' column
    df_box['year'] = [d.year for d in df_box['date']] # int year
    # or           = df_box['date'].dt.year
    df_box['month'] = [d.strftime('%b') for d in df_box['date']] # string month
    # or            = df_box['date'].dt.strftime('%b')

    # Create fig and axes objects
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # Draw box plots (using Seaborn)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=['Jan', 'Feb', 'Mar',
                                                                      'Apr', 'May', 'Jun',
                                                                      'Jul', 'Aug', 'Sep',
                                                                      'Oct', 'Nov', 'Dec'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    plt.tight_layout()

    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig