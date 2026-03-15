import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Settings
platforms = ['Facebook', 'Instagram', 'Twitter', 'LinkedIn']
campaigns = ['Summer Sale', 'Brand Launch', 'Influencer Collab', 'Holiday Deal', 'Product Demo']
n_rows = 500  # 500 rows ka data banayen ge taakay dashboard bhara hua lagay

# Generating Basic Data
data = {
    'Post_ID': [f"P-{1000+i}" for i in range(n_rows)],
    'Platform': [np.random.choice(platforms) for _ in range(n_rows)],
    'Campaign_Name': [np.random.choice(campaigns) for _ in range(n_rows)],
    'Post_Date': [datetime(2026, 1, 1) + timedelta(days=np.random.randint(0, 75)) for _ in range(n_rows)],
    'Impressions': np.random.randint(2000, 25000, n_rows)
}

df = pd.DataFrame(data)

# Marketing Logic (Realism)
# Reach hamesha Impressions se kam hoti hai
df['Reach'] = (df['Impressions'] * np.random.uniform(0.5, 0.8, n_rows)).astype(int)
# Engagement Reach ka 2% to 12% hota hai
df['Engagement'] = (df['Reach'] * np.random.uniform(0.02, 0.12, n_rows)).astype(int)
# Conversions Engagement ka 1% to 5% hota hai
df['Conversions'] = (df['Engagement'] * np.random.uniform(0.01, 0.05, n_rows)).astype(int)

# Save to CSV
df.to_csv('social_media_data.csv', index=False)
print("✅ social_media_data.csv successfully created in your folder!")