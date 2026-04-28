from openai import OpenAI
import streamlit as st
from openai import AzureOpenAI

openai_api_key = st.secrets["AZURE_OPENAI_API_KEY"]
openai_api_endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]

client = AzureOpenAI(
    api_key=openai_api_key,
    api_version="2024-02-15-preview",
    azure_endpoint=openai_api_endpoint
)

def ask_ai(question, cities):
    # limit data so prompt isn't huge
    top_cities = cities[:10]

    context = "\n".join([
        f"{c['city']} ({c['country']}): score={c['score']}, remaining=${c['remaining_monthly_budget']}"
        for c in top_cities
    ])

    prompt = f"""
    You are a helpful assistant for a city affordability app.

    Here are top cities:
    {context}

    User question:
    {question}

    Give a clear, helpful answer based ONLY on this data.
    """

    response = client.chat.completions.create(
        model=st.secrets["AZURE_OPENAI_MODEL"],
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )


    return response.choices[0].message.content

def get_recommendation(cities):
    top = cities[:5]

    context = "\n".join([
        f"{c['city']} ({c['country']}): score={c['score']}, remaining=${c['remaining_monthly_budget']}"
        for c in top
    ])

    prompt = f"""
Based on these cities:

{context}

Recommend the BEST city and explain why it is the best choice.
Be decisive.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content