# Gene Requests

<img width="1425" height="808" alt="Screenshot 2026-07-13 at 4 43 38 PM" src="https://github.com/user-attachments/assets/b79b22ee-b2fd-4ca2-9a06-612f18b12a48" />

## Description
The **Gene Requests** project is a data analysis tool designed to analyze microarray gene expression tracking matrices directly from public repositories and the NCBI Gene Expression Omnibus (GEO). 

## Features
* **Matrix Parsing**: Reads and cleans large microarray expression tracking matrices into Pandas DataFrames.
* **NCBI GEO Integration**: Interacts with the NCBI Gene Expression Omnibus via series matrix accessions.
* **Output**: Returns data based on user-input human gene symbols and GDS IDs.
* **Error Handling**: Contains built-in checks to handle inconsistent data types, tracking logs, and missing table data or fragments.
