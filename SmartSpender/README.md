# FastAPIStarter - SmartSpender Finance Tracker

A FastAPI template for info2602 students based on the [fullstack fastapi template](https://github.com/fastapi/full-stack-fastapi-template) with a few modifications to make it a layered architecture that combines the best of MVC and service repository pattern. This codebase is structured to reduce the repeatibility of code [(the DRY principle)](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) as it was demonstrated in class that code is usually repeated when implementing functionality for a CLI app, a headless API, and a fullstack app. When writing software at scale, deduplicating code is important as it makes the codebase easier to maintain, test and scale.

## 🎯 Features

- ✅ **Full Transaction Tracking** - Record income and expense transactions with categories
- ✅ **Budget Management** - Set monthly budgets by category and track spending
- ✅ **Analytics & Reports** - View spending trends, category breakdown, and monthly comparisons
- ✅ **Subscription Tracking** - Monitor recurring expenses and billing dates
- ✅ **JWT Authentication** - Secure login with JWT tokens and HttpOnly cookies
- ✅ **Role-Based Access Control** - Admin dashboard with user management
- ✅ **Responsive UI** - Mobile-optimized dark theme with Bootstrap 5
- ✅ **Highcharts Integration** - Beautiful data visualizations with pie charts and analytics
- ✅ **REST API** - Complete API endpoints for all functionality
- ✅ **Production Ready** - Dockerized, configurable, and scalable architecture

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or conda

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FastAPIStarter-main
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

4. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your database URL and secret key
   ```

5. **Run the application**
   ```bash
   python -m app.main
   # Application runs on http://localhost:8000
   ```

6. **Access the app**
   - Frontend: http://localhost:8000
   - Register a new account or login
   - Dashboard: View transaction summary
   - Analytics: Detailed spending reports with charts

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register new user account |
| POST | `/login` | Login and create JWT token |
| POST | `/logout` | Logout and clear token |

### Finance - Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/finance/api/transactions` | Get all transactions for user |
| POST | `/finance/api/transactions` | Create new transaction |
| DELETE | `/finance/api/transactions/{id}` | Delete transaction |

### Finance - Reports & Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/finance/api/reports/summary` | Monthly income, expenses, savings |
| GET | `/finance/api/reports/category-breakdown` | Spending by category |
| GET | `/finance/api/reports/monthly-trends` | 6-month trend analysis |
| GET | `/finance/api/reports/budget-status` | Budget vs actual spending |

### Finance - Budgets
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/finance/api/budgets` | Create or update budget |
| GET | `/finance/api/reports/budget-status` | View budget status |

### User Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/finance/api/user/salary` | Update monthly salary |

### Pages
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/finance/dashboard` | Main dashboard |
| GET | `/finance/transactions` | Transactions list |
| GET | `/finance/budget` | Budget management |
| GET | `/finance/analytics` | Analytics & reports |
| GET | `/admin` | Admin dashboard |

#### Example API Request

**Get Summary Report:**
```bash
curl -X GET http://localhost:8000/finance/api/reports/summary \
  -H "Cookie: access_token=<your_jwt_token>"
```

**Response:**
```json
{
  "total_income": 5000.00,
  "total_expenses": 2500.00,
  "net_savings": 2500.00,
  "savings_rate": 50.0,
  "burn_rate": 50.0
}
```

**Create Transaction:**
```bash
curl -X POST http://localhost:8000/finance/api/transactions \
  -H "Content-Type: application/json" \
  -H "Cookie: access_token=<your_jwt_token>" \
  -d '{
    "name": "Groceries",
    "amount": 85.50,
    "type": "expense",
    "category": "food",
    "is_subscription": false,
    "is_recurring": false,
    "date": "2026-04-06"
  }'
```

---

## 🏗️ What is the Model View Controller (MVC) pattern?

The MVC pattern is a code pattern that is used to organise the modules of a project and when applied to a project, it usually works as follows:

- **Models** are your SQLModel/SQLAlchemy classes (The classes that become database tables)
- **Controllers** are utility functions used to mutate models and/or perform business logic
- **Views** bind controllers to http routes passing along any user parameters from the request to the controller


## What is the Service repository pattern?

The Service Repository pattern is designed to keep business logic separate from the data access and it aims to separate the codebase into distinct layers.

- **The Repository Layer** acts as a mediator between the application and the data source (the database, files, etc)
- **The Service Layer** sits between the controller and the repository and this is where business logic lives.


The job of the **repository layer** is to handle ***CRUD*** operations on a model. It doesn't care about the rules at the business logic layer, it's only concerned about how to get and manipulate data. 

The job of the **service layer** is to handle the **RULES** of the application. This is where the business logic comes in such as checking to see if a user's authorized to access the data.

## App Structure

This app is structuresd as follows

<pre>
FastAPIStarter
|-- app
|    |- api
|    |- dependencies
|    |- models
|    |- repositories
|    |- schemas
|    |- services
|    |- static
|    |- templates
|    |- utilities
|    |- views
|-- tests/
|-- env.example
|-- pyptoject.toml
|-- README.md
</pre>

#### App Structure info

##### Main folders
`app` This folder contains all of our application code.

`tests` This contains the tests (unit tests, integration tests, etc) for the application.

##### Folders inside App
`api` This folder contains the endpoints (route fucntions) of our app.

`dependencies` This folder contains the functions that we'd usually use for dependency injection e.g. getting the information of the user who's performing the request, getting a reference to the database, etc

`models` This folder contains the Pydantic / SQLModel / SQLAlchemy models that eventually become database tables. Note that the files in here are strictly those that become database tables. The other models used for request and response validation go in the `schemas` folder

`repositories` files in this folder are used to query the datastore, which depending on the app can be a file, database, another api, etc. Usually though, it's our database.

`services` The business logic of the application lives here.

`schemas` files in this folder specify pydantic / sqlmodel classes that are used for data validation only and *NOT* models that become database tables.

`utilities` This contain generic helper functions

`static` this contains folders that contain css, js, img and other assets we may need when this app is responsible for rendering of the frontend UI>

`templates` this contains our jinja2 templates

`views` this contains the route functions used for when this app is responsible for rendering the frontnend UI

> Note that the file env.example provides a default set of configuration values for this application. you **MUST** create a copy of this file named `.env` before launching the app. The preconfigured environment allows a user to have an app that uses a sqlite database for a datastore as well as some other default configurations. The values in this should ideally be modified for production. For more possible variables, check out the `config.py` file


## Using this in production


If you so ever choose to use this template for your own projects, please consider the following:

1. You **WILL** need to modify the default configuration to 
    - Use a database that's more suitable for production. 
    - Change the default secret
    - Change the default environment
2. You may need to tweak additional settings in the `config.py` file for scalability
3. You'd need to look into a database migration / upgrade tool like alembic
4. You may want to dockerize the application for easier deployment
5. You may want to switch from storing cookies in localstorage to only cookies depending on your security needs.