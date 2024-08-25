# Data Selector

A Streamlit application to go through bourbon barcodes and simplify data to single rows.

## Description

This project is a Streamlit application that connects to a SQLite database (`BourbonDB.db`), selects a random bottle's data from the `to_organize` table, and displays it. Upon submission it pushes it to a SQL table and deletes from the staging table.
