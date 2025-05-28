import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from statsmodels.nonparametric.smoothers_lowess import lowess
import numpy as np
import os
from datetime import datetime

def get_google_trends(keyword):
    # Setup
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], timeframe='today 12-m')
    data = pytrends.interest_over_time()

    if data.empty:
        print("No Google Trends data found.")
        return None, None

    if 'isPartial' in data.columns:
        data = data.drop(columns=['isPartial'])

    # Apply LOWESS smoothing
    smoothed = lowess(data[keyword], np.arange(len(data)), frac=0.3)

    # Plot
    plt.figure(figsize=(10, 4))
    plt.plot(data.index, smoothed[:, 1], color='black', linewidth=2)
    plt.xticks(rotation=45, fontsize=9)
    plt.yticks(fontsize=9)
    plt.title(f'"{keyword}" Google Trends (Smoothed - Past Year)', fontsize=12)
    plt.ylim()
    plt.box(False)
    plt.tick_params(top=False, right=False)
    plt.tight_layout()

    # Save to file
    os.makedirs("graphs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"graphs/{keyword}_trends_{timestamp}.png"
    plt.savefig(filename, dpi=150)
    plt.close()

    return data[keyword], filename
