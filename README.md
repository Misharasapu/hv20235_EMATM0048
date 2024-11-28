
# Fish Hatchery Simulation - Task 1

## Overview
The Fish Hatchery Simulation is a program designed to model the operations of a fish hatchery. **Task 1** focuses on implementing the core functionality of the simulation, including technician management, fish sales, resource handling, and financial operations. The simulation runs for a user-specified number of quarters or until the hatchery goes bankrupt.

The primary goal of this simulation is to balance cash flow, resource management, and labour allocation while meeting customer demand for various fish types.

---

## Key Features
1. **Technician Management**:
   - Hire or fire technicians each quarter.
   - Assign specialisations to technicians for specific fish types, improving efficiency.
   - Pay technician wages at the end of each quarter.

2. **Fish Sales**:
   - Sell fish based on customer demand for each species.
   - Calculate sales revenue while considering resource availability and labour constraints.

3. **Resource Management**:
   - Track resource stock levels (fertiliser, feed, salt) in both main and auxiliary warehouses.
   - Apply depreciation to resources each quarter.
   - Restock resources from suppliers based on pricing and available cash.

4. **Financial Management**:
   - Deduct fixed costs (e.g., rent and utilities) each quarter.
   - Calculate and deduct storage costs for resources.
   - Monitor cash flow to avoid bankruptcy.

---

## How the Simulation Works
The simulation is structured around user-defined quarters, with operations carried out sequentially in each quarter:
1. Specify the number of quarters (1–8) for the simulation.
2. Manage technicians (hire/fire) at the start of each quarter.
3. Sell fish based on customer demand, ensuring sufficient resources and labour are available.
4. Restock resources from selected suppliers while managing cash flow.
5. Pay technician wages, deduct fixed costs, and calculate storage costs.
6. Apply depreciation to resources at the end of each quarter.
7. Repeat the process for the remaining quarters or until bankruptcy.

---

## Running the Simulation
### Prerequisites
- **Python 3.x** installed on your system.
- All required Python files must be in the same directory:
  - `main.py` (entry point for the simulation)
  - `Hatchery.py`
  - `Technician.py`
  - `Warehouse.py`
  - `Fish.py`
  - `Supplier.py`

### Steps to Run
1. Clone or download the project repository:
   ```bash
   git clone https://github.com/Misharasapu/hv20235_EMATM0048.git
   cd ...hv20235_EMATM0048\task1
2. Open a terminal in the project directory.
3. Run the main script:
   ```bash
   python main.py
4. Follow the on-screen prompts:
   - Enter the number of quarters for the simulation.
   - Manage technicians by hiring or firing them.
   - Input quantities of fish to sell for each type.
   - Choose a supplier for resource restocking.

	
### Example Commands
- Input `8` to run the simulation for 8 quarters.
- Hire 2 technicians in the first quarter, with one specialising in "Clef Fins."
- Sell fish based on demand while ensuring sufficient resources are available.
- Restock resources from "Slippery Lakes" as required.

### Example Console Output
```
Please enter the number of quarters (maximum: 8, default: 8 if no input is given): 8
Simulation will run for 8 quarters.

================================
====== SIMULATING quarter 1 ======
================================
To add enter positive, to remove enter negative, no change enter 0.
>>> Enter number of technicians: 2
>>> Enter technician name: Alice
Hired Alice, weekly rate=500
...
Simulation completed.
Final Cash Balance: $9600.00
```

### Project Structure
- **main.py**: Entry point for the simulation
- **Hatchery.py**: Manages overall operations and financials
- **Technician.py**: Handles technician hiring, wages, and specialisation
- **Warehouse.py**: Manages resource stock, costs, and depreciation
- **Fish.py**: Provides fish-related operations and data
- **Supplier.py**: Handles supplier information and pricing
- **README.md**: Documentation for Task 1


### Example Simulation Flow
1. **Quarter 1**:
   - Hire 2 technicians, one specialising in "Clef Fins."
   - Sell 20 units of "Clef Fins" and 10 units of "Timpani Snapper."
   - Restock fertiliser and feed from "Slippery Lakes."
   - Deduct fixed costs, pay technician wages, and calculate storage costs.

2. **Quarter 2**:
   - Hire 1 additional technician specialising in "Plagal Cod."
   - Sell fish based on demand and available resources.
   - Apply depreciation to warehouse resources.

3. **Quarter 3–8**:
   - Repeat the above steps while monitoring cash flow and avoiding bankruptcy.



### Notes
- The simulation ends early if the hatchery goes bankrupt.
- Ensure all required files are in the same directory before running the program.
- Results, including the hatchery's final state, are displayed at the end of the simulation.

---

### Additional Information

#### Suppliers
- The simulation uses two suppliers for resource restocking:
  - **Slippery Lakes**: Offers lower prices for feed and salt.
  - **Scaly Wholesaler**: Offers lower prices for fertiliser.

#### Resources
- `Fertiliser`: Measured in millilitres (ml).
- `Feed`: Measured in kilograms (kg).
- `Salt`: Measured in kilograms (kg).

#### Labour
- Each technician provides **9 weeks** of labour per quarter. Specialised technicians are more efficient when working with their assigned fish types.

---



# Task 2: Data Analysis Project – Comparing Stocks and Cryptocurrencies

## Introduction
This project investigates the performance, volatility, and trading activity of traditional stocks and cryptocurrencies. By leveraging historical data from **Yahoo Finance**, the project aims to provide insights into the key differences between these two asset classes.

### Objectives
- Compare **average daily returns**, **volatility**, and **trading volumes** of stocks and cryptocurrencies.
- Analyse the relationship between **returns** and **volatility** to assess the risk-return dynamics.
- Evaluate **long-term trends** by comparing cumulative performance over the selected time period.

### Scope
The project is structured into the following five key steps:
1. **Crawling Real-World Datasets**: Extract historical price data for selected stocks and cryptocurrencies using the `yfinance` library.
2. **Data Preparation and Cleaning**: Handle missing values, remove outliers, and create new features like daily returns and volatility.
3. **Exploratory Data Analysis**: Use visualisations to summarise and compare metrics such as returns, volatility, and trading volumes.
4. **Formulating and Answering Key Questions**: Address the overarching question: *How do stocks and cryptocurrencies differ in terms of performance and risk?*
5. **Summary and Conclusion**: Summarise the findings and propose ideas for further research.

By completing these steps, the project provides a comprehensive comparison of stocks and cryptocurrencies, highlighting their unique characteristics and roles in modern financial markets.

## Dataset Details

### Data Sources
- **Yahoo Finance**: Historical price data for stocks and cryptocurrencies was fetched using the `yfinance` library.

### Assets Included
- **Stocks**: 
  - Apple (`AAPL`)
  - Tesla (`TSLA`)
  - Amazon (`AMZN`)
- **Cryptocurrencies**:
  - Bitcoin (`BTC-USD`)
  - Ethereum (`ETH-USD`)

### Dataset Structure
- Each dataset contains the following columns:
  - `Date`: The trading date.
  - `Close`: The closing price of the asset.
  - `Volume`: The number of shares or units traded.
  - `High`/`Low`: Daily high and low prices.
  - `Adj Close`: Adjusted closing price, accounting for dividends or splits (for stocks).

### Dataset Highlights
- The project meets the requirements of having:
  - **At least 5 columns**: Key metrics for analysis.
  - **At least 150 rows**: A sufficient timeframe for meaningful comparisons.
- The merged dataset combines both stock and cryptocurrency data, creating a unified dataset for streamlined analysis.

By consolidating data from reliable sources and structuring it appropriately, this project provides a robust foundation for comparing traditional stocks and cryptocurrencies.

## Prerequisites

Before running the project, ensure the following tools and libraries are installed and properly configured.

### Required Tools
- **Python**: Version 3.8 or later.
- **Jupyter Notebook**: For running the provided `.ipynb` file.

### Python Libraries
The following libraries are required:
- **pandas**: For data manipulation and analysis.
- **numpy**: For numerical computations.
- **matplotlib**: For data visualisation.
- **seaborn**: For creating advanced plots.
- **yfinance**: For fetching stock and cryptocurrency price data from Yahoo Finance.

### Installation Instructions

1. Clone the project repository to your local machine.

2. Change the directory to the location of the project:
   ```bash
   cd "...\hv20235_EMATM0048\task2"
    ```
3. Install the required Python libraries using the requirements.txt file

   ```bash
   pip install -r "additional code\requirements.txt"
    ```

    
## Key Steps in the Project

The project is structured into the following five main steps, each addressing a critical aspect of the analysis:

### 1. Crawling Real-World Datasets
- Extracted historical stock and cryptocurrency price data from **Yahoo Finance** using the `yfinance` library.
- Selected a timeframe from **January 1, 2020, to January 1, 2023** to ensure sufficient data for comparison.
- Saved individual datasets as CSV files for reproducibility.

### 2. Data Preparation and Cleaning
- **Handled Missing Values**:
  - Identified and addressed gaps in the dataset using linear interpolation.
- **Removed Outliers**:
  - Applied the Interquartile Range (IQR) method to detect and remove extreme values.
- **Created New Features**:
  - **Daily Returns**: Calculated percentage changes in closing prices.
  - **Volatility**: Measured the daily difference between high and low prices.

### 3. Exploratory Data Analysis
- Generated visualisations to summarise and compare:
  - **Average Daily Returns**: To evaluate performance.
  - **Volatility**: To understand risk profiles.
  - **Trading Volumes**: To analyse trading activity trends.

### 4. Formulating and Answering Key Questions
- Addressed the following overarching question:
  *How do traditional stocks and cryptocurrencies differ in terms of performance, risk, and trading activity?*
- Investigated sub-questions related to performance comparisons, volatility trends, and cumulative returns.

### 5. Summary and Conclusion
- Summarised key findings on the risk-return dynamics, trading activity, and long-term trends of stocks and cryptocurrencies.
- Proposed ideas for future work, such as incorporating additional asset classes and advanced metrics.

---

## How to Run the Project

### Repository Structure

The repository is organised into the following folders and files:

- **notebook**: Contains the Jupyter Notebook used for the analysis.
  - `task2_analysis.ipynb`: The main notebook detailing the entire analysis process, from crawling the dataset to generating insights.
  
- **data**: Contains all the datasets generated and used in the project.
  - `AAPL_stock_data.csv`: Historical stock data for Apple.
  - `AMZN_stock_data.csv`: Historical stock data for Amazon.
  - `TSLA_stock_data.csv`: Historical stock data for Tesla.
  - `BTC-USD_crypto_data.csv`: Historical cryptocurrency data for Bitcoin.
  - `ETH-USD_crypto_data.csv`: Historical cryptocurrency data for Ethereum.
  - `merged_stock_crypto_data_reduced.csv`: Merged dataset of all stocks and cryptocurrencies.
  - `cleaned_grouped_data.csv`: Dataset cleaned and grouped for analysis.
  - `final_cleaned_enriched_data.csv`: Fully enriched and processed dataset.
  - `grouped_data.csv`: Aggregated data for stocks and cryptocurrencies.
  - `reordered_cleaned_data.csv`: Intermediate dataset for exploratory analysis.

- **additional code**: Contains helper scripts or configuration files.
  - `requirements.txt`: File listing all Python libraries required for the project.

### Running the Jupyter Notebook
1. Open the Jupyter Notebook:
   ```bash
   jupyter notebook task2_analysis.ipynb
   ```
2. **Execute the cells sequentially to**:
   - Fetch stock and cryptocurrency data from Yahoo Finance.
   - Clean and process the datasets.
   - Generate visualisations and insights.
   - Review the output directly in the notebook.

3. Review the output directly in the notebook.

---
## Project Results and Outputs

The following outputs are generated as part of the project:

- **Cleaned Datasets**:
  - Merged datasets for stocks and cryptocurrencies, saved as CSV files in the `data` folder.
  - Includes calculated metrics such as daily returns and volatility.
  
- **Visualisations**:
  - Time-series plots comparing average daily returns for stocks and cryptocurrencies.
  - Boxplots and histograms illustrating volatility and trading volumes.
  - Scatter plots highlighting risk-return dynamics.

- **Key Insights**:
  - Cryptocurrencies demonstrate higher average returns but greater volatility compared to stocks.
  - Stocks exhibit steadier trading volumes and more predictable risk-return dynamics.

## Limitations

- **Dataset Scope**:
  - The analysis is limited to selected stocks and cryptocurrencies (Apple, Tesla, Amazon, Bitcoin, Ethereum) over the period January 1, 2020, to January 1, 2023.
  
- **Data Source Dependence**:
  - All data is sourced from Yahoo Finance. Any inaccuracies or missing data in the source could affect the analysis.

- **Simplified Metrics**:
  - Advanced financial metrics (e.g., Sharpe ratios, Value at Risk) were not included to maintain simplicity.
  
- **Assumptions**:
  - The analysis assumes consistent trading days across assets, which may not always hold true for stocks and cryptocurrencies.


## Future Work

This project can be extended in the following ways:

1. **Include Additional Assets**:
   - Analyse more stocks and cryptocurrencies to generalise findings.
   - Compare other asset classes, such as bonds or commodities.

2. **Advanced Metrics**:
   - Incorporate metrics like Sharpe ratios, drawdowns, or rolling correlations.

3. **Predictive Analytics**:
   - Use machine learning models to predict future trends in returns or volatility.

4. **Dynamic Visualisations**:
   - Create interactive dashboards for real-time data exploration.


## Acknowledgements

The following tools and resources were instrumental in the development of this project:

- **Yahoo Finance**: For providing the historical price data.
- **Python Libraries**: pandas, numpy, matplotlib, seaborn, yfinance.
- **Jupyter Notebook**: For creating a structured and interactive analysis.






