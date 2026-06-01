# SmartSpender Final Submission System Design

## What This File Covers
This file is the final-reference version for the SmartSpender system design section.

Use it for:
- the System Design slide in the presentation
- the System Design section in the report
- the diagram labels and arrow text in PowerPoint or draw.io
- the presenter notes for the recorded video

---

## 1. Final Slide Title
SmartSpender System Design

## 2. Final One-Slide Description
SmartSpender uses a client-server architecture. Users interact with the system through a web browser, while a FastAPI application deployed on Render handles authentication, transaction management, budget tracking, and analytics. The application uses Jinja2 templates, JavaScript, Bootstrap, and Highcharts on the frontend, and stores data in a relational SQLite database through SQLModel.

## 3. Final Diagram Boxes

### Box 1
Heading:
User Browser

Body:
- Desktop or mobile web browser
- Sends requests to the application
- Displays the dashboard, transactions, budgets, recurring payments, and analytics pages

### Box 2
Heading:
SmartSpender Web App

Body:
- FastAPI application
- Hosted on Render
- Handles page routing and API requests
- Manages authentication and finance features

### Box 3
Heading:
Frontend Layer

Body:
- Jinja2 templates
- Bootstrap
- JavaScript
- Highcharts visualizations

### Box 4
Heading:
Backend Layer

Body:
- Auth routes
- Finance routes
- ReportService
- TransactionRepository
- BudgetRepository

### Box 5
Heading:
Database Layer

Body:
- SQLite database
- SQLModel ORM
- Persistent storage for application data

### Box 6
Heading:
Core Models

Body:
- User
- Transaction
- Budget

---

## 4. Final Arrow Labels

### Arrow A
From:
User Browser

To:
SmartSpender Web App

Text:
HTTPS Requests / Responses

### Arrow B
From:
SmartSpender Web App

To:
Frontend Layer

Text:
Renders HTML Templates and Charts

### Arrow C
From:
SmartSpender Web App

To:
Backend Layer

Text:
Processes Authentication and Business Logic

### Arrow D
From:
Backend Layer

To:
Database Layer

Text:
CRUD Operations via SQLModel

### Arrow E
From:
Database Layer

To:
Core Models

Text:
Stores User, Transaction, and Budget Data

---

## 5. Final Recommended Diagram Layout

Use this exact visual order on the slide:

Top row:
- User Browser
- SmartSpender Web App
- Database Layer

Bottom row:
- Frontend Layer under SmartSpender Web App
- Backend Layer under SmartSpender Web App
- Core Models under Database Layer

## 6. Final Diagram Structure

```text
[ User Browser ]
        |
        | HTTPS Requests / Responses
        v
[ SmartSpender Web App ]
      /           \
     /             \
    v               v
[ Frontend Layer ] [ Backend Layer ]
                          |
                          | CRUD Operations via SQLModel
                          v
                   [ Database Layer ]
                          |
                          | Stores User, Transaction, and Budget Data
                          v
                      [ Core Models ]
```

---

## 7. Exact PowerPoint Box Text To Paste

### User Browser
Desktop or mobile web browser
Displays pages and sends requests

### SmartSpender Web App
FastAPI application
Hosted on Render
Handles routes, authentication, and finance features

### Frontend Layer
Jinja2 templates
Bootstrap
JavaScript
Highcharts

### Backend Layer
Auth routes
Finance routes
ReportService
Repositories

### Database Layer
SQLite database
SQLModel ORM
Persistent data storage

### Core Models
User
Transaction
Budget

---

## 8. Exact Arrow Text To Paste

- User Browser -> SmartSpender Web App
HTTPS Requests / Responses

- SmartSpender Web App -> Frontend Layer
Renders HTML Templates and Charts

- SmartSpender Web App -> Backend Layer
Processes Authentication and Business Logic

- Backend Layer -> Database Layer
CRUD Operations via SQLModel

- Database Layer -> Core Models
Stores User, Transaction, and Budget Data

---

## 9. Final Presenter Script For The Video
This system uses a client-server architecture. The user interacts with SmartSpender through a desktop or mobile web browser. Requests are sent over HTTPS to the SmartSpender web application, which is built with FastAPI and deployed on Render. The frontend layer uses Jinja2 templates, Bootstrap, JavaScript, and Highcharts to present the interface and visual analytics. The backend layer handles authentication, transaction management, budget tracking, and report generation. Data is stored in a SQLite database through SQLModel, with the main models being User, Transaction, and Budget.

---

## 10. Final Report Paragraph Version
SmartSpender follows a client-server architecture. Users access the application through a web browser, which communicates with a FastAPI web application hosted on Render. The frontend is built using Jinja2 templates, Bootstrap, JavaScript, and Highcharts to provide an interactive user interface for dashboards, transactions, budgeting, recurring payments, and analytics. The backend layer is responsible for routing, authentication, business logic, and report generation through services and repositories. Data is stored in a SQLite relational database using SQLModel, with the main entities being User, Transaction, and Budget.

---

## 11. Short Report Version
SmartSpender uses a client-server architecture where a browser communicates with a FastAPI application deployed on Render. The frontend uses Jinja2 templates, Bootstrap, JavaScript, and Highcharts, while the backend manages authentication, financial processing, and reporting. Application data is stored in SQLite using SQLModel.

---

## 12. What To Put On The Actual Slide
Your final System Design slide should contain:
- Title: SmartSpender System Design
- One short description sentence or paragraph
- One clear architecture diagram
- Hosting label: Render
- Database label: SQLite with SQLModel

Keep the slide visual and simple. Do not overcrowd it with long explanations.

---

## 13. What Not To Put On The Slide
Do not include:
- lecture definitions of system design
- unrelated case studies
- cloud patterns that your project does not use
- references list
- long paragraphs
- implementation details that belong in code, not in the diagram

---

## 14. Submission Checklist For This Section
Before submitting, confirm that your system design includes:
- SmartSpender title
- browser/client
- FastAPI app
- Render hosting
- frontend technologies
- backend processing
- SQLite database
- SQLModel
- User, Transaction, and Budget models

If all of those appear, your system design section is presentation-ready and report-ready.
