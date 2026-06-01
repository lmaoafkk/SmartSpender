# SmartSpender Project Explanation Guide

## Big Picture

SmartSpender is a personal finance web application built with FastAPI. Its main purpose is to help users track income and expenses, manage monthly budgets, monitor recurring subscriptions, and view analytics about their spending habits.

A strong one-line explanation for this project is:

> SmartSpender is a layered FastAPI finance tracker where routers handle HTTP requests, repositories manage database access, services contain business logic, and Jinja templates plus JavaScript power the frontend.

The app supports:

- User registration and login
- Authentication with JWT tokens stored in cookies
- Transaction tracking
- Subscription and recurring payment tracking
- Monthly budget management
- Financial analytics and charts
- Admin and regular user handling

## Main Technologies Used

- FastAPI for backend routing and API development
- SQLModel for database models and database interaction
- Jinja2 for server-rendered HTML templates
- Bootstrap for UI styling and layout
- JavaScript for frontend interactivity
- Highcharts for analytics visualizations
- Pydantic Settings for environment-based configuration
- JWT for authentication
- `pwdlib` for password hashing

## Why These Technologies Were Chosen

### FastAPI

FastAPI is modern, fast, and easy to structure. It also works well for building APIs and supports dependency injection, validation, and clean routing.

### SQLModel

SQLModel combines ORM-style database models with Pydantic-like validation. This makes model definitions cleaner and easier to explain.

### Jinja2

Jinja2 makes it easy to generate HTML on the server side while still allowing JavaScript to add dynamic behavior afterward.

### Bootstrap

Bootstrap speeds up UI development and makes responsive design easier.

### JWT in Cookies

JWT provides lightweight authentication, and storing it in an HTTP-only cookie makes it more secure than exposing it directly to frontend JavaScript.

### Highcharts

Highcharts was used because the project includes analytics dashboards and category-based visual summaries.

## High-Level Architecture

The project follows a layered structure:

- Routers handle requests and responses
- Dependencies handle reusable authentication and database logic
- Models define database tables
- Schemas validate request and response data
- Repositories contain database queries
- Services contain business logic and calculations
- Templates render HTML pages
- Static files handle frontend CSS and JavaScript

This is a good design because it separates responsibilities clearly. It prevents business logic, database logic, and UI logic from being mixed together in one place.

## Project Structure Overview

Important files and folders:

- `main.py`
- `SmartSpender/app/main.py`
- `SmartSpender/app/config.py`
- `SmartSpender/app/database.py`
- `SmartSpender/app/dependencies/`
- `SmartSpender/app/models/`
- `SmartSpender/app/schemas/`
- `SmartSpender/app/repositories/`
- `SmartSpender/app/services/`
- `SmartSpender/app/routers/`
- `SmartSpender/app/templates/`
- `SmartSpender/app/static/`

## Entry Point Files

### `main.py`

This is the root entry file. It adjusts the Python path so the app inside the `SmartSpender` folder can be imported properly, then exposes the FastAPI app object.

Why it exists:

- It provides a simple root-level startup entry
- It makes deployment easier when the runtime expects a top-level app object

### `SmartSpender/app/main.py`

This is the real application entry point.

It does the following:

- Loads environment variables
- Defines a FastAPI lifespan function
- Creates database tables on startup
- Adds session middleware
- Includes routers
- Mounts static files
- Registers a custom 401 unauthorized handler
- Runs Uvicorn when executed directly

Why this file matters:

- It is the central bootstrap file for the whole app
- It wires together configuration, middleware, routers, and startup behavior

## Configuration

### `SmartSpender/app/config.py`

This file defines the `Settings` class and `get_settings()` helper.

What it does:

- Reads environment variables from `.env`
- Stores values like database URI, secret key, JWT algorithm, app host, and app port
- Uses `@lru_cache` so settings are created once and reused

Why this was chosen:

- Keeps secrets out of the code
- Makes deployment configurable
- Avoids hardcoding environment-specific values

## Database Setup

### `SmartSpender/app/database.py`

This file creates the SQLModel database engine and manages sessions.

Main functions:

- `create_db_and_tables()`: creates all database tables
- `drop_all()`: drops all database tables
- `get_session()`: provides a database session for request handling
- `get_cli_session()`: provides a session for CLI usage

Why this design was chosen:

- Centralizes database setup
- Makes sessions reusable through dependency injection
- Keeps DB code out of routers

## Dependencies

### `SmartSpender/app/dependencies/session.py`

Defines `SessionDep`, which injects a database session into route functions.

Why:

- Avoids repeating session creation in every route
- Makes route code cleaner

### `SmartSpender/app/dependencies/auth.py`

This file handles authentication-related reusable logic.

Main functions:

- `get_current_user()`: reads the JWT token from the cookie, decodes it, and loads the user from the database
- `is_logged_in()`: returns whether the current request is authenticated
- `is_admin()`: checks if the user role is admin
- `is_admin_dep()`: enforces admin-only access

Reusable dependency aliases:

- `IsUserLoggedIn`
- `AuthDep`
- `AdminDep`

Why this was chosen:

- Prevents auth logic from being duplicated in multiple routes
- Makes protected routes easier to read
- Keeps role-checking consistent

## Security Utilities

### `SmartSpender/app/utilities/security.py`

This file manages password hashing and JWT token generation.

Main functions:

- `encrypt_password(password)`: hashes a password
- `verify_password(plaintext_password, encrypted_password)`: checks if a plain password matches a stored hash
- `create_access_token(data, expires_delta)`: creates a JWT token with expiration

Why this was chosen:

- Passwords should never be stored in plain text
- JWT tokens are useful for lightweight stateless authentication

## Flash Messages

### `SmartSpender/app/utilities/flash.py`

This file stores temporary feedback messages in the session, such as success or error messages.

Main functions:

- `flash(request, message, type)`: stores a message in session
- `get_flashed_messages(request)`: retrieves and removes stored messages

Why:

- Useful for registration/login feedback
- Works well with server-rendered pages

## Pagination Utility

### `SmartSpender/app/utilities/pagination.py`

This defines a `Pagination` helper object with page navigation properties.

It supports:

- previous page detection
- next page detection
- page iteration

Why:

- Keeps pagination behavior reusable instead of writing it repeatedly

## Models

### `SmartSpender/app/models/user.py`

Defines the `User` table.

Fields:

- `id`
- `username`
- `email`
- `password`
- `role`
- `salary`

What it represents:

- A user account with login credentials and salary information

Why `salary` is here:

- Salary is user-level profile data and is used in financial summary calculations

### `SmartSpender/app/models/transaction.py`

Defines the `Transaction` table and related enums.

Enums:

- `TransactionType`: `income`, `expense`
- `TransactionCategory`: food, transport, entertainment, shopping, bills, health, subscription, other

Fields:

- `id`
- `name`
- `amount`
- `type`
- `category`
- `is_subscription`
- `is_recurring`
- `next_billing_date`
- `date`
- `created_at`
- `user_id`

Why these fields were chosen:

- They support both standard transactions and recurring subscription-style entries
- `user_id` links transactions to the user who owns them

### `SmartSpender/app/models/budget.py`

Defines the `Budget` table and `BudgetCategory` enum.

Fields:

- `id`
- `category`
- `monthly_limit`
- `month_year`
- `user_id`

Why `month_year` exists:

- Budgets are monthly, so the project needs a way to distinguish April budgets from May budgets

## Schemas

Schemas are used to validate data coming into or out of the API.

### `SmartSpender/app/schemas/user.py`

Defines:

- `UserUpdate`
- `AdminCreate`
- `RegularUserCreate`
- `UserResponse`
- `SignupRequest`

Why:

- Separates database models from public-facing request/response data

### `SmartSpender/app/schemas/auth.py`

Defines:

- `SigninRequest`
- `SignupRequest`

Why:

- Clarifies what data is required for auth-related actions

### `SmartSpender/app/schemas/transaction.py`

Defines:

- `TransactionCreate`
- `TransactionResponse`
- `TransactionUpdate`

Why:

- Ensures transaction API data is properly validated before use

### `SmartSpender/app/schemas/budget.py`

Defines:

- `BudgetCreate`
- `BudgetResponse`
- `BudgetUpdate`

Why:

- Keeps budget API input/output structured and predictable

### `SmartSpender/app/schemas/report.py`

Defines response models for analytics data:

- `SummaryResponse`
- `CategoryBreakdownResponse`
- `MonthlyTrendResponse`
- `BudgetStatusResponse`

Why:

- Makes report outputs easier to document and understand

## Repositories

Repositories are responsible for database operations.

### `SmartSpender/app/repositories/user.py`

This file defines `UserRepository`.

Main methods:

- `create()`
- `search_users()`
- `get_by_username()`
- `get_by_email()`
- `get_by_id()`
- `get_all_users()`
- `update_user()`
- `delete_user()`

Why this repository exists:

- It centralizes all user-related database access
- It keeps routers and services from writing raw queries directly

### `SmartSpender/app/repositories/transaction_repository.py`

Defines `TransactionRepository`.

Main methods:

- `get_all(user_id)`
- `get_by_id(transaction_id, user_id)`
- `create(transaction)`
- `update(transaction)`
- `delete(transaction)`
- `get_by_month(user_id, year, month)`
- `get_by_date_range(user_id, start_date, end_date)`
- `get_by_type(user_id, transaction_type)`
- `get_by_category(user_id, category)`
- `get_subscriptions(user_id)`
- `get_income_total(user_id)`
- `get_expense_total(user_id)`

Why this repository exists:

- It keeps all transaction query logic in one place
- It simplifies analytics and transaction route handling

### `SmartSpender/app/repositories/budget_repository.py`

Defines `BudgetRepository`.

Main methods:

- `get_all(user_id, month_year=None)`
- `get_by_category(user_id, category, month_year)`
- `create_or_update(budget)`
- `delete(budget_id, user_id)`

Why this repository exists:

- It makes budget logic reusable
- It supports the “update if already exists, otherwise create” behavior

## Services

Services contain business logic.

### `SmartSpender/app/services/auth_service.py`

Defines `AuthService`.

Main methods:

- `_get_or_create_hardcoded_admin()`
- `authenticate_user(username, password)`
- `register_user(username, email, password)`

What it does:

- Registers users with hashed passwords
- Authenticates users
- Creates JWT tokens
- Supports a hardcoded admin user named `bob`

Important note you should know:

The hardcoded admin account exists mainly for demo or assessment purposes. It is convenient for testing, but it would not be ideal for production.

### `SmartSpender/app/services/user_service.py`

Defines `UserService`.

Main method:

- `get_all_users()`

This is a thin service layer over user retrieval.

### `SmartSpender/app/services/report_service.py`

Defines `ReportService`.

Main methods:

- `get_summary(user_id, salary, month_year=None)`
- `get_category_breakdown(user_id)`
- `get_monthly_trends(user_id, months=6)`
- `get_budget_status(user_id, month_year=None)`
- `get_subscription_total(user_id)`

What each one does:

#### `get_summary()`

Calculates:

- total income
- total expenses
- net savings
- burn rate
- salary

Why:

- This powers the dashboard summary cards

#### `get_category_breakdown()`

Groups expenses by category and calculates percentages.

Why:

- This powers the category breakdown chart

#### `get_monthly_trends()`

Builds month-by-month totals for income and expenses.

Why:

- This supports trend analysis over time

#### `get_budget_status()`

Compares monthly spending against monthly budgets for each category.

Why:

- This helps users see whether they are on track or over budget

#### `get_subscription_total()`

Adds up recurring subscription costs.

Why:

- This helps track recurring expenses separately

## Routers

Routers define the web pages and API endpoints.

### `SmartSpender/app/routers/__init__.py`

This file:

- sets up Jinja templates
- configures static files
- creates the main `router`
- creates the `api_router`
- imports route modules

Why:

- It centralizes router setup and template configuration

### `SmartSpender/app/routers/index.py`

Routes:

- `GET /`: shows landing page
- `GET /app`: redirects based on login/admin status

Why:

- This file controls the initial user entry flow

### `SmartSpender/app/routers/login.py`

Routes:

- `GET /login`: renders login page
- `POST /login`: authenticates user and sets auth cookie

Why:

- Keeps login behavior separate and focused

### `SmartSpender/app/routers/register.py`

Routes:

- `GET /register`: renders register page
- `POST /register`: creates a new user

Why:

- Keeps registration logic separate from login logic

### `SmartSpender/app/routers/logout.py`

Route:

- `GET /logout`: removes the access token cookie and redirects

Why:

- Allows users to end their session cleanly

### `SmartSpender/app/routers/admin_home.py`

Route:

- `GET /admin`: shows admin dashboard page

Why:

- Restricts admin content using the `AdminDep` dependency

### `SmartSpender/app/routers/user_home.py`

Route:

- `GET /app`: shows authenticated user home page

Why:

- Provides a general logged-in home experience

### `SmartSpender/app/routers/users.py`

Route:

- `GET /api/users`: returns all users

Why:

- Exposes user listing through the API

### `SmartSpender/app/routers/finance.py`

This is the most important router in the project because it handles the finance features.

Page routes:

- `/finance/dashboard`
- `/finance/transactions`
- `/finance/recurring`
- `/finance/budget`
- `/finance/analytics`

API routes:

- `GET /finance/api/transactions`
- `POST /finance/api/transactions`
- `DELETE /finance/api/transactions/{transaction_id}`
- `GET /finance/api/reports/summary`
- `GET /finance/api/reports/category-breakdown`
- `GET /finance/api/reports/monthly-trends`
- `GET /finance/api/reports/budget-status`
- `POST /finance/api/budgets`
- `DELETE /finance/api/budgets/{budget_id}`
- `PUT /finance/api/user/salary`
- `POST /finance/api/user/refresh`

What this router does:

- renders finance pages
- creates and deletes transactions
- creates and deletes budgets
- updates salary
- returns reporting data for analytics
- clears all finance data for the current user

Why this design works:

- It keeps all finance-related features grouped together in one module
- It separates page rendering routes from JSON API routes while keeping them in the same feature area

## Templates

Templates handle the HTML structure of the app.

### `SmartSpender/app/templates/base.html`

This is the global base template.

It provides:

- page head setup
- Bootstrap
- app-wide CSS
- a toast container

Why:

- Creates one shared structure for all pages

### `SmartSpender/app/templates/authenticated-base.html`

This is the shared layout for logged-in users.

It provides:

- sidebar navigation
- responsive mobile sidebar behavior
- flash message support
- shared finance JavaScript loading

Why:

- Prevents duplication across dashboard, transactions, budget, recurring, and analytics pages

### `SmartSpender/app/templates/landing_standalone.html`

This is the public landing page.

It includes:

- a styled landing screen
- sign in and register panel
- JavaScript to open login/register forms dynamically

Why:

- Gives the project a polished public entry experience

### `SmartSpender/app/templates/login.html`

Acts as a redirecting page back to the landing page.

### `SmartSpender/app/templates/register.html`

Also acts as a redirecting page back to the landing page.

Why these exist:

- They support route structure while using the landing page as the real auth UI entry

### Finance Templates

#### `dashboard.html`

Shows:

- salary
- total income
- total expenses
- net savings
- recent transactions
- active subscriptions

#### `transactions.html`

Shows:

- all transactions in a table
- modal for adding a transaction

#### `recurring.html`

Shows:

- recurring subscriptions
- modal for adding subscription entries

#### `budget.html`

Shows:

- monthly budget cards
- progress bars
- delete interaction for budget items

#### `analytics.html`

Shows:

- expense summary
- category breakdown
- savings information
- recent expenditure table
- charts using Highcharts

## Frontend JavaScript

### `SmartSpender/app/static/js/finance.js`

This is the main shared frontend script for finance features.

Main responsibilities:

- API helper calls
- confirmation modal handling
- refreshing all user finance data
- updating salary
- saving transactions
- saving subscriptions
- deleting transactions
- saving budgets
- deleting budgets
- opening Bootstrap modals

Why this was chosen:

- Keeps common finance interactions in one shared script
- Allows pages to call reusable functions instead of repeating the same logic everywhere

### `SmartSpender/app/static/js/app.js`

This file fetches and displays user data from `/api/users`.

Its role is smaller, but it demonstrates frontend API consumption.

## Typical Request Flow You Can Explain

Here is a simple example of how adding a transaction works:

1. The user opens the dashboard or transactions page.
2. The page loads and displays a modal form for new transactions.
3. JavaScript collects form input.
4. JavaScript sends a `POST` request to `/finance/api/transactions`.
5. FastAPI validates the request body using `TransactionCreate`.
6. The router creates a `Transaction` model object.
7. `TransactionRepository.create()` saves it to the database.
8. The API returns JSON.
9. The frontend reloads the relevant table or dashboard data.

This is a great example to use if someone asks how backend and frontend interact.

## Authentication Flow You Can Explain

1. User enters username/email and password.
2. Login route calls `AuthService.authenticate_user()`.
3. Password is checked using hashed password verification.
4. If valid, a JWT token is created.
5. The token is stored in an HTTP-only cookie named `access_token`.
6. Future requests automatically include that cookie.
7. `get_current_user()` decodes the token and loads the user from the database.

Why this is good:

- it is simple
- it avoids storing plain-text passwords
- it allows protected routes to identify the current user

## Why Layering Was a Good Design Choice

If someone asks why the project was structured this way, a strong answer is:

> I separated the application into routers, repositories, services, models, schemas, and templates so that each part had a clear responsibility. This makes the project easier to debug, maintain, explain, and extend in the future.

## Good Answers To Common Questions

### Why did you use FastAPI?

Because it is fast, modern, and makes it easy to build both web routes and JSON APIs with validation and dependency injection.

### Why did you use SQLModel?

Because it makes model definitions cleaner and combines database modeling with validation-friendly patterns.

### Why did you use repositories and services?

Repositories isolate database access, while services isolate business rules and calculations. This keeps route functions simpler and makes the code more modular.

### Why did you use enums for categories and transaction types?

Enums reduce invalid data and keep categories consistent throughout the application.

### Why did you use JWT in cookies?

JWT gives lightweight authentication, and HTTP-only cookies improve security by preventing normal frontend JavaScript from reading the token directly.

### Why did you use Jinja templates and JavaScript together?

Jinja is useful for initial page rendering, and JavaScript adds dynamic behavior like modals, async requests, table updates, and chart loading.

### Why is salary stored on the user model?

Because salary is part of the user’s financial profile and is used in summary calculations like total income and net savings.

### Why did you include a hardcoded admin?

It was likely added for demonstration or assessment convenience so an evaluator can log in as an admin quickly without doing additional setup.

## Limitations and Honest Improvements

If someone asks what could be improved, these are good honest answers:

- The hardcoded admin account should be replaced with a proper admin creation strategy in production.
- Some frontend logic is duplicated between shared JavaScript and page-level scripts.
- Some report methods accept a month parameter but do not fully filter by it yet.
- The app could use more automated tests for important flows.
- Some imports and files could be cleaned up further.

These are good answers because they show you understand both the strengths and the weaknesses of the project.

## Short Presentation Summary

If you need a short verbal summary, use this:

> SmartSpender is a layered FastAPI web application for personal finance management. It supports authentication, transaction tracking, budgeting, subscription monitoring, and analytics. I structured it using routers, repositories, services, models, schemas, templates, and shared frontend scripts so the code stays organized and easy to maintain. I used SQLModel for database interaction, JWT cookies for authentication, Jinja for rendering pages, and Highcharts for data visualization.

## Final Study Tip

When explaining this project, do not try to memorize every line of code. Focus on these five things:

- what the app does
- how a request flows through the system
- why the code is split into layers
- why each major technology was chosen
- what you would improve next

If you can confidently explain those five things, you will already sound like someone who understands the project well.
