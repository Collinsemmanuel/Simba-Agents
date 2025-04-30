import requests
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import pickle
import os

class ResearchAgent:
    def __init__(self):
        self.data = []
        self.past_queries = {}
        self.model = None
        self.vectorizer = None
        self.load_model()

    def collect_data(self, query):
        """Collect data from the web based on the query."""
        search_url = f"https://www.google.com/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('h3')  # Example: extracting titles from search results
            self.data = [result.get_text() for result in results]
        else:
            print("Failed to retrieve data.")

    def analyze_data(self):
        """Analyze the collected data using clustering."""
        if not self.data:
            return "No data to analyze."
        
        # Vectorize the data
        self.vectorizer = CountVectorizer()
        X = self.vectorizer.fit_transform(self.data)

        # Apply KMeans clustering
        self.model = KMeans(n_clusters=3)  # Example: 3 clusters
        self.model.fit(X)

        # Return cluster labels
        return self.model.labels_

    def report(self):
        """Generate a report based on the analysis."""
        report_data = {
            "query": " ".join(self.data),
            "results_count": len(self.data),
            "results": self.data,
            "clusters": self.analyze_data().tolist() if self.model else []
        }
        return report_data

    def save_query(self, query):
        """Save past queries for learning."""
        if query not in self.past_queries:
            self.past_queries[query] = self.data
            with open('past_queries.pkl', 'wb') as f:
                pickle.dump(self.past_queries, f)

    def load_model(self):
        """Load past queries from a file."""
        if os.path.exists('past_queries.pkl'):
            with open('past_queries.pkl', 'rb') as f:
                self.past_queries = pickle.load(f)

    def run_research(self, query):
        """Run the research process."""
        self.collect_data(query)
        self.save_query(query)
        report = self.report()
        return report

if __name__ == "__main__":
    agent = ResearchAgent()
    user_query = input("Enter your research query: ")
    report = agent.run_research(user_query)
    
    print("\nResearch Report:")
    print(f"Query: {user_query}")
    print(f"Number of Results: {report['results_count']}")
    print("Results:")
    for result in report['results']:
        print(f"- {result}")
    print(f"Clusters: {report['clusters']}")