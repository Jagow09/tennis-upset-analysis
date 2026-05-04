# Expect the Unexpected: What 30 Years of Tennis Data Reveals About Upsets

A data-driven interactive blog analysing upset patterns across Grand Slam and Masters 1000 tennis tournaments from 1991 to 2024.

## Live Blog

View the published interactive blog here:
https://jagow09.github.io/tennis-upset-analysis/

## Research Question

What factors determine the likelihood of an upset in professional tennis? Does tournament level, surface, round, or ranking gap matter most?

## Data Source

All data comes from Jeff Sackmann's Tennis ATP dataset:
https://github.com/JeffSackmann/tennis_atp

The dataset covers ATP match results from 1991 to 2024, including player rankings, match statistics, and tournament information.

## Project Structure

tennis-upset-analysis/
├── README.md
├── runAll.py
├── blog.ipynb
├── index.html
├── src/
│   ├── 01_scrape.py
│   ├── 02_clean.py
│   ├── 03_analysis.py
│   └── 04_figures.py
├── data/
│   ├── raw/
│   └── clean/
└── output/
    └── figures/

## How to Replicate

### Requirements

pip install pandas numpy scikit-learn plotly requests

### Steps

1. Clone this repository:
git clone https://github.com/Jagow09/tennis-upset-analysis.git
cd tennis-upset-analysis

2. Run the full pipeline with a single command:
python runAll.py

This will automatically:
- Download all raw match data from Jeff Sackmann's GitHub repo
- Clean and merge the data into a single dataset
- Run the analysis and generate summary statistics
- Generate all 6 interactive figures

3. Open blog.ipynb in Jupyter to view the analysis notebook.

### Running Scripts Individually

python src/01_scrape.py    # Download raw data
python src/02_clean.py     # Clean and merge data
python src/03_analysis.py  # Run analysis
python src/04_figures.py   # Generate figures

## Key Findings

- Nearly 1 in 3 matches ends in an upset overall
- Masters 1000 events (34.0%) produce significantly more upsets than Grand Slams (28.2%)
- Early rounds are far more volatile than later rounds
- Ranking gap is the strongest predictor of match outcome
- Betting markets appear to underestimate upset probability

## Tools Used

- Python 3.12
- pandas - data cleaning and wrangling
- scikit-learn - logistic regression model
- Plotly - interactive visualisations
- requests - web scraping
- Jupyter Notebook - analysis notebook
- HTML/CSS/JavaScript - interactive blog webpage

## Author

Jago - University of Exeter, BEE2041 Data Science in Economics, 2026
