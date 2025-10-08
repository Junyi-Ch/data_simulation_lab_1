# Data Simulation Lab 1

Welcome to the first data simulation lab for Psych 201a! This lab introduces you to statistical distributions and data simulation techniques commonly used in psychological research.

## Lab Goals

- **Understand distributions**: Learn how normal, binomial, and lognormal distributions describe behavioral data (accuracy, RTs, individual variability)
- **Practice simulation**: Generate and visualize synthetic datasets using tidyverse functions  
- **Reproducible reports**: Learn how to write reproducible lab reports with inline statistics in Quarto

## One Time Setup

### 1. Prerequisites

Make sure you have the following installed:
- [Homebrew](https://brew.sh) (macOS package manager)
- [Git](https://git-scm.com/) and [GitHub CLI](https://cli.github.com/)
- [Pixi](https://pixi.sh/) (package manager for R and Python)

### 2. Install Pixi

```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

### 3. Clone this Repository

```bash
git clone https://github.com/psyc-201/data_simulation_lab_1.git
cd data_simulation_lab_1
```

## Getting Started

### 1. Install Dependencies

```bash
pixi install
```

### 2. Setup R & Python Kernels

```bash
pixi run setup
```

### 3. Open in VS Code

1. Open VS Code and use the account icon to login to your GitHub account
2. Open the folder you cloned: File > Open
3. Accept any pop-ups to configure VS Code with necessary extensions

### 4. Start Working

- **R Console**: `pixi run r`
- **Live Preview**: `pixi run render`
- **Preview specific file**: `pixi run preview filename.qmd`

## Lab Structure

This lab includes multiple versions to support different learning styles:

| File                                       | Description                                       |
| ------------------------------------------ | ------------------------------------------------- |
| `code/index.qmd`                           | Introduction and overview                         |
| `code/distributions-lab.qmd`               | Complete lab with full instructions               |
| `code/distributions-lab-intermediate.qmd`  | Scaffolded version with placeholders to fill in   |
| `code/distributions-lab-withsolutions.qmd` | Complete solutions for reference                  |
| `code/distributions_lab.py`                | Python implementation using pandas and matplotlib |
| `code/distributions_lab_withsolutions.py`  | Python solutions                                  |

## Working with the Lab

### R/Quarto Workflow

1. Open `code/distributions-lab-intermediate.qmd` in VS Code
2. Use the command palette (`cmd+shift+p`) to search: "Terminal: Create New Terminal"
3. Start the R console: `pixi run r`
4. Fill in the `___` placeholders in the intermediate version
5. Use "Run cell" buttons to execute code chunks

### Python Workflow

1. Open `code/distributions_lab.py` in VS Code
2. Use the command palette to search: "Jupyter: Create Interactive Window"
3. Use "Run cell" buttons to execute code

### Converting Between Formats

- Convert `.qmd` to `.ipynb`: `pixi run convert filename.qmd`
- Convert `.ipynb` to `.qmd`: `pixi run convert filename.ipynb`

## Adding/Removing Libraries

Use these commands to manage packages (they auto-update `pixi.toml`):

- **Python**: `pixi add package` or `pixi add --pypi package`
- **R**: `pixi add r-package`
- **Remove**: `pixi remove package` or `pixi remove r-package`

## Key Topics Covered

- **Normal distributions**: Simulating continuous data
- **Binomial distributions**: Modeling accuracy and binary outcomes  
- **Lognormal distributions**: Simulating reaction times
- **Multi-participant experiments**: Individual differences and group-level analysis
- **Data visualization**: Creating publication-ready plots

## Troubleshooting

### Common Issues

1. **R not found**: Make sure you're using `pixi run r` not just `r`
2. **Package not found**: Use `pixi add` instead of `install.packages()` or `pip install`
3. **Render errors**: The intermediate version cannot be rendered due to placeholder syntax - fill in the `___` placeholders first

### Reset Environment

If anything goes wrong, you can safely reset:

```bash
rm -rf .pixi/ pixi.lock
pixi install
pixi run setup
```

## Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [Tidyverse Documentation](https://www.tidyverse.org/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Pixi Documentation](https://pixi.sh/latest/)

## Important Notes

**Always prefer using `pixi add` and `pixi remove` instead of `install.packages()` in R or `pip install` / `conda install` in Python**

This will save you from many unexpected headaches and ensure reproducible environments!

---

*Happy coding! 🎉*
