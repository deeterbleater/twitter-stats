# Tweet Stats Dashboard

This Python script generates an interactive dashboard to visualize statistics from your Twitter data.

## Features

- Automatically converts your Twitter data export (tweets.js) to a CSV file
- Displays tweet activity over time
- Shows average engagement (likes and retweets) over time
- Visualizes tweet frequency by hour of the day
- Presents a scatter plot of likes vs. hour to identify "banger" tweets
- Generates a word cloud from your tweet content

## Prerequisites

- Python 3.7+
- pip (Python package installer)

## Installation

1. Clone this repository or download the `tweet_stats.py` file.

2. Install the required Python packages:

   ```
   pip install pandas plotly dash wordcloud
   ```

## Usage

1. Export your Twitter data and locate the `tweets.js` file.

2. Create a `data` folder in the same directory as `tweet_stats.py`.

3. Place your `tweets.js` file in the `data` folder.

4. Run the script:

   ```
   python tweet_stats.py
   ```

5. Open a web browser and go to `http://127.0.0.1:8050/` to view your dashboard.

## How It Works

1. The script first checks for a `tweets.csv` file in the `data` folder.
2. If `tweets.csv` doesn't exist, it looks for `tweets.js` and generates the CSV file.
3. The data is then processed and used to create various visualizations.
4. A Dash app is created to display these visualizations in an interactive dashboard.

## Customization

You can modify the script to change the appearance of the graphs or add new visualizations. Look for the callback functions in the script to adjust existing graphs.

## Troubleshooting

- If you encounter a `FileNotFoundError`, make sure your `tweets.js` file is in the `data` folder.
- For other issues, ensure you have all the required packages installed and are using a compatible Python version.

## Privacy Note

This script runs locally on your machine and does not send your data anywhere. However, always be cautious with your personal data and avoid sharing the generated dashboard publicly.

## License

This project is open source and available under the [MIT License](LICENSE).