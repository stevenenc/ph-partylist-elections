ph-partylist-elections/
│
├── partylist_scraper/                  # Main Scrapy project
│   ├── spiders/                        # Contains web scraping spiders
│   │   ├── partylist_template.py       # Scrapes structured vote results from Wikipedia template pages
│   │   └── partylist_attributes.py     # Scrapes infobox metadata (e.g., leadership, ideology) from each party's page
│   ├── __init__.py
│   ├── items.py                        # Defines Scrapy items (currently unused)
│   ├── middlewares.py                 # Scrapy middleware config (default)
│   ├── pipelines.py                   # Scrapy pipelines config (default)
│   └── settings.py                    # Scrapy project settings
│
├── plots_per_year/                    # Optional folder for exporting plots by year
│
├── debug_partylist.ipynb              # Notebook for inspecting raw data and debug HTML files
│
├── normalize_attributes.py            # Normalizes and deduplicates scraped attributes (e.g., ideology variants)
├── merge_cleaned_results.py           # Merges scraped metadata and vote results into one CSV or JSON
├── clean_results.py                   # Optional preprocessing of raw tables (e.g., for 2025 results)
├── visualize.py                       # General plotting script for vote and seat trends
├── visualize_progressive_trends.py    # Specialized analysis for Left/Progressive party performance
├── plot_political_position_trends.py  # Visualization of vote trends by ideology/political position
│
├── partylist_template.csv             # Scraped party-list election results (1998–2025)
├── partylist_attributes.json          # Raw scraped attributes from party Wikipedia pages
├── partylist_attributes_cleaned.json  # Cleaned and normalized party metadata
│
├── results_fixed.csv                  # Optional cleaned version of vote results
├── merged_partylist_with_links.csv    # Merged results + party links
├── .gitignore                         # Standard Git ignore file
└── scrapy.cfg                         # Scrapy project config
