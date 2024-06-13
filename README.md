# 100DaysCommitLog

## Overview
A fun commit logger so you and your friends can track your #100DaysofCode progress together. Using Fast API to collect data and return graphs and counters.

## Installation
### Prerequisites
Ensure you have Poetry and Python installed on your system.

### Steps

1. Clone Repository:
    ```bash
    git clone https://github.com/bruna-calistrate/study-buddy-llm.git
    ```

2. Install Poetry:
    ```bash
    pip install poetry
    ```
3. Install dependencies:
   ```bash
   poetry install
   ```

4. Enter virtual environment:
   ```bash
   poetry shell
   ```

5. Run the Fast API app:
   ```bash
   uvicorn app.main:create_app
   ```

## Environment Variables

To run this project you will need a [GitHub Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token). 