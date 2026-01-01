import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("archive (3).zip")

# Preview column names
print("Columns in dataset:", df.columns.tolist())

# Convert 'date_added' to datetime safely
if 'date_added' in df.columns:
    df['date_added'] = pd.to_datetime(df['date_added'], format='%B %d, %Y', errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
else:
    df['year_added'] = None
    df['month_added'] = None

# Fill missing values
for col in ['country', 'director', 'cast', 'rating', 'duration']:
    if col in df.columns:
        df[col] = df[col].fillna('Unknown')

# Ensure 'duration' is string before using .str
if 'duration' in df.columns:
    df['duration'] = df['duration'].astype(str)
    df['duration_int'] = df['duration'].str.extract(r'(\d+)').astype(float)
    df['duration_type'] = df['duration'].str.extract(r'([a-zA-Z]+)')
else:
    df['duration_int'] = None
    df['duration_type'] = None

# Create genre list column without overwriting original
if 'genres' in df.columns:
    df['genre_list'] = df['genres'].apply(lambda x: [g.strip() for g in x.split(',')] if pd.notnull(x) else [])
else:
    df['genre_list'] = [[] for _ in range(len(df))]

# Drop duplicates safely (exclude unhashable columns)
df.drop_duplicates(subset=[col for col in df.columns if df[col].apply(lambda x: isinstance(x, list)).sum() == 0], inplace=True)

# Set seaborn style
sns.set(style='whitegrid')

# 1. Content Type Distribution
if 'type' in df.columns:
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x='type', hue='type', palette='Set2', legend=False)
    plt.title('Distribution of Movies vs TV Shows')
    plt.xlabel('Type')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.show()

# 2. Top 10 Countries by Content Count
if 'country' in df.columns:
    plt.figure(figsize=(10, 5))
    top_countries = df['country'].value_counts().head(10)
    sns.barplot(x=top_countries.values, y=top_countries.index, hue=top_countries.index, palette='Blues_r', legend=False)
    plt.title('Top 10 Countries by Content Count')
    plt.xlabel('Number of Titles')
    plt.ylabel('Country')
    plt.tight_layout()
    plt.show()

# 3. Content Added by Year
if 'year_added' in df.columns and df['year_added'].notnull().any():
    plt.figure(figsize=(10, 5))
    df['year_added'].value_counts().sort_index().plot(kind='bar', color='orange')
    plt.title('Netflix Content Added by Year')
    plt.xlabel('Year Added')
    plt.ylabel('Number of Titles')
    plt.tight_layout()
    plt.show()

# 4. Release Year Distribution
if 'release_year' in df.columns:
    plt.figure(figsize=(10, 5))
    df['release_year'].value_counts().sort_index().plot(kind='hist', bins=20, color='purple')
    plt.title('Distribution of Release Years')
    plt.xlabel('Release Year')
    plt.ylabel('Number of Titles')
    plt.tight_layout()
    plt.show()

# 5. Rating Distribution
if 'rating' in df.columns:
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, y='rating', order=df['rating'].value_counts().index, hue='rating', palette='coolwarm',
                  legend=False)
    plt.title('Content Rating Distribution')
    plt.xlabel('Count')
    plt.ylabel('Rating')
    plt.tight_layout()
    plt.show()

# 6. Movie Duration Distribution
if 'type' in df.columns and 'duration_int' in df.columns:
    plt.figure(figsize=(10, 5))
    movies = df[df['type'] == 'Movie']
    sns.histplot(movies['duration_int'].dropna(), bins=30, kde=True, color='green')
    plt.title('Movie Duration Distribution (in minutes)')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Count')
    plt.tight_layout()

    plt.show()
