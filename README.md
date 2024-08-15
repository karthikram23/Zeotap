# Zeotap

## Rule Engine with AST

This project is a 3-tier rule engine application that leverages an Abstract Syntax Tree (AST) for managing and evaluating conditional rules. The system allows dynamic creation, combination, and modification of rules to assess user eligibility based on attributes such as age, department, income, and spending.

### Features:

Rule Management: Create, evaluate, combine, and modify rules.
User Authentication: Secure user login and registration with Flask-Login.
Web Interface: Intuitive interface for interacting with the rule engine.
Attribute Management: Add and manage attributes for rules.


### Setup
1. Clone the Repository:

git clone <repository_url>
cd <repository_folder>


2. Install Dependencies:
   
pip install -r requirements.txt

3. Initialize the Database:

flask db init
flask db migrate
flask db upgrade

Run the Application:

flask run


### Usage:

Register or Log In: Access the rule engine through the web interface.
Create Rules: Define new rules based on user attributes.
Evaluate Rules: Test rules against provided user data.
Combine Rules: Merge multiple rules into a single rule.
Modify Rules: Adjust existing rules through the interface.
Add Attributes: Expand the attribute catalog to accommodate new rule conditions.


### Security Considerations:
Authentication: Secure login with password hashing.
CSRF Protection: Enabled for all form submissions.
Input Validation: Server-side validation to ensure data integrity.

### Performance Considerations:
Optimized Parsing: Rules are stored as strings and parsed into ASTs on demand.
Efficient Queries: SQLAlchemy optimizations to reduce query overhead.
