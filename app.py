from webbrowser import get
from Bio import Entrez
from numpy import mean
import streamlit as st
import pandas as pd
import GEOparse
Entrez.email = '25smuppala@gmail.com'

@st.cache_data
def load_expression_matrix():
    gds = GEOparse.get_GEO(geo = "GDS6063", destdir = "./")
    df = gds.table
    return df

def get_gene_summary(gene_sym):
    try:
        search_term = f"{gene_sym.strip()}[Gene Name] AND human[Organism]"
        with Entrez.esearch(db = "gene", term = search_term) as handle:
            results = Entrez.read(handle)
        
        id_list = results.get("IdList", [])
        if not id_list:
            return "Not Found"
        
        gene_id = id_list[0]
        with Entrez.esummary(db = "gene", id = gene_id) as esummary_handle:
            esummary_results = Entrez.read(esummary_handle)
        
        gene_data = esummary_results["DocumentSummarySet"]["DocumentSummary"][0]
        return gene_data.get("Summary", "No written description provided.")
    except Exception as e:
        return f"NCBI network timeout or parsing error: {str(e)}"

print(get_gene_summary("TP53"))

st.set_page_config(page_title="NCBI Requests", layout="wide")
st.title("Explorer and Expression Matrix")
st.markdown("Data Extraction Dashboard")
st.sidebar.header("Search Console")
gene_input = st.sidebar.text_input("Enter Human Gene Symbol", value="TP53").strip().upper()
submit_button = st.sidebar.button("Run Analysis")

if gene_input:
    st.header(f"Target Analysis: {gene_input}")
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.subheader("Official NCBI Description")
        with st.spinner("Getting details from NCBI"):
            summary_text = get_gene_summary(gene_input)
        
        if summary_text:
            st.info(summary_text)
        else:
            st.error(f"Could not locate gene identifier: {gene_input}")

    with col2:
        st.subheader("Expression Matrix Profile (GDS6063)")
        with st.spinner("Analyzing microarray matrix..."):
            try:
                df = load_expression_matrix()
                gene_df = df[df['IDENTIFIER'].str.upper() == gene_input]

                if not gene_df.empty:
                    numeric_cols = gene_df.select_dtypes(include=['float64', 'int64'])
                    mean_values = round(float(numeric_cols.mean(axis=1).iloc[0]), 2)
                    max_value = round(float(numeric_cols.max(axis=1).iloc[0]), 2)
                    min_value = round(float(numeric_cols.min(axis=1).iloc[0]), 2)

                    st.metric(label = "Average Abundance Level", value = f"{mean_values} units")
                    st.metric(label = "Peak Signal Intensity", value = f"{max_value} units")
                    st.metric(label = "Minimum Detection Floor", value = f"{min_value} units")
                else:
                    st.warning("No records found in dataset")
            except Exception:
                st.error("Error Processing Dataset")
