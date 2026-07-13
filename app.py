from webbrowser import get
from Bio import Entrez
import streamlit as st
import pandas as pd
from io import StringIO
import requests
import gzip
Entrez.email = '25smuppala@gmail.com'

@st.cache_data(show_spinner="Getting data from official NCBI datasets", max_entries=2)
def load_gds_data(gds_id):
    gds_id = str(gds_id).upper().strip()
    try:
        if len(gds_id) > 6:
            folder = f"{gds_id[:-3]}nnn"
        else:
            folder = "GDSnnn"
        url = f"https://ftp.ncbi.nlm.nih.gov/geo/datasets/{folder}/{gds_id}/soft/{gds_id}.soft.gz"
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            return (None, f"NCBI dataset not found (Status: {response.status_code})")
        
        lines = []
        start_reading = False
        with gzip.GzipFile(fileobj=response.raw) as gzipped_file:
            for binary_line in gzipped_file:
                line = binary_line.decode("utf-8")
                cleaned = line.strip()
                if cleaned == "!dataset_table_begin":
                    start_reading = True
                    continue
                if cleaned == "!dataset_table_end":
                    break
                if start_reading:
                    lines.append(line)
        if not lines:
            return (None, "No expression columns found in this GDS structure")
        df = pd.read_csv(StringIO("\n".join(lines)), sep="\t")
        df.columns = [col.lower() for col in df.columns]
        return df, None
    except Exception as e:
        return None, str(e)

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

st.set_page_config(page_title="NCBI Requests", layout="wide")
st.title("Explorer and Expression Matrix")
st.markdown("Data Extraction Dashboard")
st.sidebar.header("Search Console")
with st.sidebar.form(key="Search Form"):
    gds_input = st.sidebar.text_input("1. Enter NCBI GDS ID: ", value = "GDS3929").strip().upper()
    gene_input = st.sidebar.text_input("2. Enter Human Gene Symbol: ", value = "ERBB2").strip().upper()
    submit_button = st.form_submit_button(label="Run Analysis")

if submit_button:
    if gene_input and gds_input:
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
            st.subheader(f"Expression Matrix Profile: {gds_input}")
            with st.spinner("Analyzing microarray matrix..."):
                try:
                    df, error_msg = load_gds_data(gds_input)
                    if error_msg:
                        st.error(f"Error processing dataset: {error_msg}")
                    else:
                        symbol_col = next((c for c in ['identifier', 'gene symbol', 'gene_symbol', 'id'] if c in df.columns), None)
                        if not symbol_col:
                            st.error("Could not find a valid gene identity column in this dataset")
                        else:
                            gene_df = df[df[symbol_col].astype(str).str.upper() == gene_input]

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
