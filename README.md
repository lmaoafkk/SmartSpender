# SmartSpender - Finance Tracker

A FastAPI web application for personal finance management, featuring transaction tracking, budgeting, analytics, and user authentication.

##Accees the site by going to https://smartspender-3bft.onrender.com/

## Features

- Transaction tracking (income/expenses)
- Budget management
- Financial analytics and reports
- User authentication and admin dashboard
- Responsive web UI with charts
- REST API for all features

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SmartSpender
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

4. **Run the application**
   ```bash
   python -m app.main
   ```

5. **Open in browser**
   - Go to http://localhost:8000
   - Register an account and start tracking finances

## Project Structure

- `app/` - Main application code
  - `routers/` - API endpoints
  - `models/` - Database models
  - `services/` - Business logic
  - `templates/` - HTML templates
  - `static/` - CSS, JS, images
- `pyproject.toml` - Dependencies
- `.env` - Configuration

## Production

For production use, update `.env` with secure secrets and consider using a production database. See `config.py` for options.
