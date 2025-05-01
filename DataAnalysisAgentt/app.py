#Sheila Chebii
from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from dotenv import load_dotenv
import os

from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Initialize GPT-4o LLM
llm = ChatOpenAI(model="gpt-4o", openai_api_key=openai_api_key)

# Define the tool
@tool
def summarize_data(data_str: str) -> str:
    """Provides insights based on uploaded data (as a string)."""
    df = pd.read_csv(BytesIO(data_str.encode()))
    summary = f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns.\nColumns: {list(df.columns)}\n"
    summary += df.describe(include='all').to_string()
    return summary

# Setup the agent with tools
tools = [summarize_data]
prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad"],
    template=(
        "You are a data analysis expert. Analyze the dataset provided below and generate "
        "insights that include trends, anomalies, correlations, and any other interesting patterns. "
        "Provide actionable recommendations based on the data.\n\n"
        "Dataset:\n{input}\n\n"
        "Scratchpad:\n{agent_scratchpad}"
    )
)
agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Upload and analyze
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        # Determine file type and load data
        filename = file.filename
        try:
            if filename.endswith('.csv'):
                data = pd.read_csv(file, on_bad_lines='skip', engine='python')
            elif filename.endswith('.xlsx') or filename.endswith('.xls'):
                data = pd.read_excel(file)
            elif filename.endswith('.json'):
                data = pd.read_json(file)
            else:
                return "Unsupported file format. Please upload a CSV, Excel, or JSON file."
        except pd.errors.ParserError as e:
            return f"Error parsing file: {str(e)}. Please check the file format and try again."

        # Analyze the data
        insights = analyze_data(data)

        # Preprocess dataset for agent
        # Limit the dataset to the first 100 rows
        data_sample = data.head(100)
        key_features = extract_key_features(data_sample)
        agent_input = (
            "You are a data analysis expert. Analyze the following key features of the dataset "
            "and provide insights and actionable recommendations:\n\n"
            f"{key_features}"
        )

        # Get agent response
        try:
            agent_response = agent_executor.invoke({"input": agent_input})
        except openai.error.RateLimitError as e:
            return f"Rate limit exceeded: {str(e)}. Please try again later."

        return render_template('results.html', insights=insights)

# Generalized analysis
def analyze_data(data):
    insights = {}

    # Basic statistics
    insights['basic_stats'] = data.describe(include='all').to_html()

    # Detect numeric columns for visualization
    numeric_cols = data.select_dtypes(include=['number']).columns
    if not numeric_cols.empty:
        # Pairplot for numeric columns
        plt.figure(figsize=(10, 5))
        sns.pairplot(data[numeric_cols])
        plt.tight_layout()

        # Convert plot to base64
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        insights['pairplot'] = plot_url

    # Detect categorical columns for summaries
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
    if not categorical_cols.empty:
        insights['categorical_summary'] = {
            col: data[col].value_counts().to_dict() for col in categorical_cols
        }

    return insights

def extract_key_features(data):
    """Extracts key features from the dataset for agent analysis."""
    features = []

    # Check for missing values
    missing_values = data.isnull().sum()
    if missing_values.any():
        features.append(f"Missing values detected in columns: {missing_values[missing_values > 0].to_dict()}")

    # Correlation analysis for numeric columns
    numeric_cols = data.select_dtypes(include=['number'])
    if not numeric_cols.empty:
        correlation_matrix = numeric_cols.corr()
        high_correlations = correlation_matrix[correlation_matrix.abs() > 0.8].stack().reset_index()
        high_correlations = high_correlations[high_correlations['level_0'] != high_correlations['level_1']]
        if not high_correlations.empty:
            features.append(f"High correlations detected: {high_correlations.to_dict(orient='records')}")

    # Detect outliers using IQR
    for col in numeric_cols.columns:
        q1 = data[col].quantile(0.25)
        q3 = data[col].quantile(0.75)
        iqr = q3 - q1
        outliers = data[(data[col] < (q1 - 1.5 * iqr)) | (data[col] > (q3 + 1.5 * iqr))]
        if not outliers.empty:
            features.append(f"Outliers detected in column '{col}'.")

    return "\n".join(features)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
