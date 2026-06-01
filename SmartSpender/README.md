# SmartSpender - Finance Tracker

A FastAPI web application for personal finance management, featuring transaction tracking, budgeting, analytics, and user authentication.

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

## Email Budget Alerts

SmartSpender can email users when a new expense makes them close to or over a category budget. The alert is sent to the signed-in user's account email address.

For Render Free, use Brevo's API because outbound SMTP ports are blocked. Add Brevo settings to `.env` or Render environment variables:

```env
BREVO_API_KEY=your_brevo_api_key
BREVO_SENDER_EMAIL=your_verified_sender_email
BREVO_SENDER_NAME=SmartSpender
```

`BREVO_SENDER_EMAIL` must be a sender verified in Brevo.

Resend API is also supported as a fallback:

```env
RESEND_API_KEY=re_your_api_key
RESEND_FROM_EMAIL=SmartSpender <noreply@yourdomain.com>
```

`RESEND_FROM_EMAIL` must use a domain verified in Resend when sending to real users.

For local Gmail SMTP testing, you can use these settings instead:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_FROM_NAME=SmartSpender
SMTP_USE_TLS=true
```

For Gmail, use an app password instead of your normal Google password. Gmail requires the real sender email to be your Gmail account or another address you have verified in Gmail, so `SMTP_FROM_NAME` is the safe way to show `SmartSpender` as the sender name. If Brevo, Resend, and SMTP are all configured, SmartSpender uses Brevo first. The email is sent only when a transaction triggers a budget alert.
