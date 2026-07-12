# Gene Requests

## Description
The **Gene Requests** project is a data analysis tool designed to analyze microarray gene expression tracking matrices directly from public repositories and the NCBI Gene Expression Omnibus (GEO). 

## Features
* **Data Fetching**: Interacts with online data resources and includes pathways to accommodate for shifted GitHub repositories, branch updates, or structural changes.
* **Matrix Parsing**: Reads and cleans large microarray expression tracking matrices into Pandas DataFrames.
* **NCBI GEO Fallback Integration**: Uses data queries to interact with the NCBI Gene Expression Omnibus via series matrix accessions
* **Error Handling**: Contains built-in checks to handle inconsistent data types, tracking logs, and missing table data or fragments
