# Words Across Borders

An interactive dashboard providing an enhanced version of the Google Ngrams Viewer that includes translations and synonyms to allow the comparison of word frequencies over time across languages.

**Live Demo:** [https://words-across-borders.streamlit.app/](https://words-across-borders.streamlit.app/)

-- Project Status: Completed

## User Manual
For detailed information on how to use the dashboard and interpret the data, please refer to the user manual included in the [live dashboard](https://words-across-borders.streamlit.app/).

## Intro
Our inspiration came from perceived linguistic differences between different cultures, such as the stereotype that Asians are sterner and/or less likely to praise their children. Using the Google Ngram Viewer dataset, we aimed to create an engaging dashboard focused on visualizing differences in word usage in the literature between various languages, hence acting as an enhanced version to the pre-existing Google Ngram Viewer which only shows word frequencies for a single language at a time through a singular type of visualization (time series graph). 
## Partners
* [Apurv Gude](https://github.com/ApurvGude2000)
* [Daniel Yan](https://github.com/danielyan21)
* [Jahanvi Jeswani](https://github.com/jahanvi-j)
* [Juan Pablo Reyes Martinez](https://github.com/jpreyesm03)
* [Eva Reutercrona](https://github.com/EReutercrona)

## Methods Used
* API Wrappers
* EDA and Data Visualization
* Interactive Web App Development
* Guerilla Usability Testing and General User Feedback/Iteration

## Technologies
* Tableau (deprecated)
* Python
* Streamlit
* Pandas, Jupyter, Plotly

## Project Description
* Sources: [Google Ngram Viewer dataset](https://books.google.com/ngrams/info) for word frequencies, [World Languages Dataset](https://resourcewatch.org/data/explore/soc_071_world_languages?section=Discover&selectedCollection=&zoom=1.3858624006414608&lat=0&lng=19.342290857936067&pitch=0&bearing=0&basemap=dark&labels=light&layers=%5B%7B%22dataset%22%3A%2220662342-dcdd-4a42-9f58-bcc80217de71%22%2C%22opacity%22%3A1%2C%22layer%22%3A%22f2d76e6b-060d-4dc9-83ea-284bef6b2aae%22%7D%5D&aoi=&page=1&sort=most-viewed&sortDirection=-1) to determine each country's primary language for the choropleth, Synonyms list via word-finding query engine [Datamuse API](https://www.datamuse.com/api/)

Our dashboard allows users to query for any word or phrase, and compare how often it shows up (frequency) across all languages included in the Google Ngram Viewer dataset through multiple visualizations each focused on showing trends across different variables (e.g. time, location, language, etc.): choropleth, bar graph, word cloud, and time series. We also provide a time series and heatmap for users to compare frequencies of different words in the same language, just like the built-in Google Ngram Viewer. 

This project was primarily an exercise in creating meaningful visualizations with compelling user interaction and flow. As such, less focus was spent on data cleaning and analysis compared to creating a streamlined and intuitive user experience. The aim of our dashboard was to not feel like an internal tool, but rather a public web app that the general population (any curious mind, essentially) could quickly understand how to use to produce easily interpretable visualizations. 
While less focus was spent on data cleaning and processing, several initial iterations of this project revolved around exploring and selecting the right tools (APIs and data sources). Below is a non-exhaustive list of notable issues that lead to pivots, with most of them being part of the initial iterations mentioned previously. 
* Multiple terabytes of data from Google Ngram required us to use an API calls instead of downloading it. This made us switch off of Tableau (which has poor compatibility with dynamic data).
* Without an official API, multiple unofficial ones were tested, each with issues of their own such as only including the English language. Ultimately, we used a back end JSON endpoint to the public Google Ngrams Viewer.
* Selecting practical, informative, and non-redundant visualizations.
* Wrangling translation packages and APIs: To find a translation resource that worked reliably and efficiently for this project, we first looked at the widely used google_translate Python package but quickly had to shift due to its unreliability and tendency to break on a regular basis. Official API translation sources were also too costly for this project. Ultimately the deep_translate package was chosen due to its ability to run translation through official Google Translate which we viewed as reliable in generating outputs.
* We noticed early on that API calls to Google Translate cannot return alternative translations (synonyms) the way the direct web version does. The big hurdle we encountered with trying other synonym search methods was that classic ones such as NLTK wordnets often returned incomplete results, as they are not designed for pure semantic synonym search. Online multilingual thesaurus API services were also prohibitively expensive, so we ultimately chose to run synonym search through a word-finding engine called Datamuse and merge multilingual synonyms with the translation step - translating English synonyms rather than finding true synonyms for the translation in other languages. This workaround is a common cause of any odd synonyms that may show up in our dashboard for certain queries.
* Relatively small sample sizes for works published before 1600 resulted in spikes in word frequencies. This led us to use a rolling average for the time-series graph, and only query data from 1600 onwards.
* We iteratively tested our data dashboard internally and with external users. Significant time was spent fine-tuning the format, tooltips text, titles, placement of visuals or text, etc., all for a more consistent, clear, and intuitive user experience/flow.  

## Running Locally
To run this application on your local machine, follow the steps below.

### Prerequisites
- Python 3.x installed
- pip (Python package installer)

### Installation & Usage
1. **Install Dependencies**
   Open your terminal or command prompt, navigate to the project directory, and install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Application**
    Start the dashboard by running the main.py script:
    ```bash
   streamlit run main.py
   ```
