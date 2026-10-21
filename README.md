# Intelligent Student Performance Analysis System

A small Streamlit dashboard for file-based academic record search and analysis. It uses a normalized ERP dictionary for direct lookup, a binary search tree for CGPA range retrieval, and a max heap for top-N ranking. Graph and dynamic-programming examples are isolated in `algorithms/` and are not connected to the intentionally disabled Demonstration item.

## Setup

1. Use Python 3.10 or newer.
2. Install dependencies: `python -m pip install -r requirements.txt`
3. The synthetic `student_sample_data.txt` is included in `data/`.
4. Start the dashboard: `streamlit run app.py`

The data file contains 80 synthetic records and uses `ERP|Name|CGPA|OperatingSystems|DSA|Mathematics`, with optional comments and header. The app validates all values and never creates replacement records. Names and scores are invented for this academic prototype and do not represent actual students.

## Dashboard

The summary cards are calculated from loaded rows. Refresh rereads the same file. Search by ERP (or numeric roll number such as `1` for `ST-001`) reveals the selected student's name and details. Range filters update live and combine with AND logic. Exact marks counts use the selected subject and active CGPA bounds. Results are paginated at eight rows, with names omitted from result tables.

The Demonstration sidebar item is intentionally disabled in this phase. There is no database, authentication, external API, or generated fallback data.

## Algorithms

Graph functions: BFS, DFS, Prim, Kruskal, Dijkstra, and Bellman–Ford. DP functions: 0/1 knapsack, LCS length, matrix-chain multiplication cost, and resource allocation. Resource allocation accepts `returns[project][allocation]`, where each value is the return for assigning that integer allocation to a project; its DP state is best return for a total budget, and its transition tries every split of that budget across the current project and previous projects.

Run the lightweight checks with `python -m unittest discover -s tests`.
