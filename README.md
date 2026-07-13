# Gene Requests

<img width="1424" height="797" alt="Screenshot 2026-07-12 at 1 25 42 PM" src="https://github.com/user-attachments/assets/88ed73ff-ea07-4cc8-b360-e8207aec75c9" />

## Description
The **Gene Requests** project is a data analysis tool designed to analyze microarray gene expression tracking matrices directly from public repositories and the NCBI Gene Expression Omnibus (GEO). 

## Features
* **Data Fetching**: Interacts with online data resources and includes pathways to accommodate for shifted GitHub repositories, branch updates, or structural changes.
* **Matrix Parsing**: Reads and cleans large microarray expression tracking matrices into Pandas DataFrames.
* **NCBI GEO Integration**: Uses data queries to interact with the NCBI Gene Expression Omnibus via series matrix accessions
* **Error Handling**: Contains built-in checks to handle inconsistent data types, tracking logs, and missing table data or fragments
