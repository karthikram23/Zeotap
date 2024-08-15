# Zeotap Application 1

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

1. Register or Log In: Access the rule engine through the web interface.
2. Create Rules: Define new rules based on user attributes.
3. Evaluate Rules: Test rules against provided user data.
4. Combine Rules: Merge multiple rules into a single rule.
5. Modify Rules: Adjust existing rules through the interface.
6. Add Attributes: Expand the attribute catalog to accommodate new rule conditions.


### Security Considerations:

1. Authentication: Secure login with password hashing.
2. CSRF Protection: Enabled for all form submissions.
3. Input Validation: Server-side validation to ensure data integrity.


