# ProPortion — Metric Recipe Scaler

ProPortion is a sleek, dark-themed utility built with PySide6 and Python to scale recipe ingredients using metric weights (**g**) and volumes (**ml**). It automatically saves your custom recipes to a local database.

## Features
* 📐 **Proportional Scaling:** Instantly recalculates ingredient amounts as you change target serving counts.
* 🔢 **Whole-Number Precision:** Display values automatically round to clean, crisp integers.
* 📦 **Local JSON Storage:** Saves your collection instantly to a `recipes.json` file.
* 🗑 **One-Click Cleanup:** Quickly remove recipes directly from the main view dropdown row.
* ➕ **Clean Ingredient Entry:** Dedicated input fields make adding new recipes effortless.

---

## Installation & Setup

This project uses **uv** for blazing-fast virtual environment tracking and project sync.

### 1. Synchronize the Environment
Open your terminal in the project's root folder (`pro_portion/`) and run:
```bash
uv sync
