# Interactive Treemap Using Plotly.js

## Table of Contents
- [Tech Stack](#tech-stack)
- [Repository Setup](#repository-setup)
- [Running the App Locally](#running-the-app-locally)
- [Code Explanation](#code-explanation)

## Tech Stack
- Flask
- Plotly.js (for charts)

## Repository Setup
Clone the repository using:

```bash
git clone https://github.com/fr4nc1sj0hn/treemap-plotly.git
```

To rename the main folder, simply rename the directory after cloning.

To push your changes to a new repository:

```bash
git remote remove origin
git remote add <your-repo-url>
git add *
git commit -m "Initial Commit"
git push origin main
```


## Running the App Locally
Before running the app, create a `.env` file and specify the same environment variables from the app service configuration.

To run the app:

- Create a virtual environment:
```bash
python -m venv .venv
.venv\scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the Flask app:
```bash
flask run #or python app.py
```

## Code Explanation - `chart.html`

### 1. Template Structure
The HTML template defines a basic webpage layout with Plotly.js and jQuery included via CDNs. This page has two main containers:

- **Treemap Chart** (on the left) displays an interactive treemap that represents expense categories.
- **Line Chart** (on the right) dynamically updates based on treemap selections, showing trends over time for specific categories.

### 2. Data Fetching Functions
Two main functions use AJAX to fetch data from Flask API endpoints:

- `getTreemapData()` fetches data for the treemap, with each node representing a category or subcategory of expenses.

- `getExpenseHistory(breakdown, mode)` retrieves historical expense data based on the selected category or subcategory. The `breakdown` parameter specifies the selected item, while `mode` differentiates between the "All," "category," or "subcategory" views.

### 3. Treemap Creation (`createExpenseTreemap(data)`)
This function creates the treemap using the provided data:

- `values`, `labels`, and `parents` arrays are generated from the data for Plotly’s treemap structure.

- **Color Scale**: The treemapcolorway: globalColorScale line uses a global color scale, ensuring that color schemes remain consistent across the app and any additional charts if needed.

- Configures color and layout to ensure a responsive chart with smooth transitions.

- The chart responds to user clicks, which trigger the **Line Chart** update.

The `plotly_click` event listener captures the clicked node's details, determining if the click is on a main category or a subcategory:

- **Top-Level Clicks**: Displays all data if the click is on the main "All" category.

- **Category and Subcategory Clicks**: Updates `selectedCategory` and `mode` for the specific level, then fetches historical data to update the Line Chart.

### 4. Line Chart Creation (`createExpenseLineChart(data, label)`)
The line chart displays expense trends for the selected category over time:

- The data arrays `x` and `y` are populated with `BudgetMonth` and `TotalExpenses`.

- Configures a smooth area plot with hover information for interactive exploration of expense trends.

- Layout settings control colors, margins, and axis formats, creating a consistent look with the treemap.

### 5. Initial Chart Loading
On page load:

- `getTreemapData()` is called to render the initial treemap.
- `getExpenseHistory("All", "All")` fetches all available expense history for display in the initial line chart.

## Code Explanation - `app.py`

### Routes

#### `/api/expense-summary`

This route serves the data for the treemap chart by reading expense-summary.json. This file contains summarized expense data, allowing the frontend to construct a visual representation of expense categories and subcategories.

#### `/api/expense-history`

This route provides data for the expense trend line chart. It filters historical expense data based on query parameters:

- **Category Mode (`mode == "category"`)**: Filters expenses for a specific category, aggregates monthly totals, and returns them in JSON format.

- **Subcategory Mode (`mode == "subcategory"`)**: Filters expenses for a specific subcategory without further aggregation.

- **All Mode**: Aggregates and returns the total monthly expenses across all categories.
This modular structure supports dynamic filtering and display of data when users interact with the treemap.

#### /chart (Chart Page): 
Renders `chart.html`


You can replace the json files with actual database calls, etc. For example here is a sample implementation using a Stored Procedure call against an azure sql database.

```python
def get_expense_treemap(user,category,year):
    with connection.cursor() as cursor:
        query = "EXEC [schema].[sp_GetExpenseBreakdown] @Year=%s, @Category=%s, @User=%s,@Top=%s"
        cursor.execute(query, [year, category, user, 50])

        columns = [col[0] for col in cursor.description]
        data_from_db = [dict(zip(columns, row)) for row in cursor.fetchall()]

    # Convert the result into a DataFrame
    df = pd.DataFrame(data_from_db)
    return df
```

and then you'll have to modify `createExpenseTreemap` like this:
```javascript
function createExpenseTreemap(data) {
  const df = JSON.parse(data); // instead of const df = data

  //same logic
}
```

