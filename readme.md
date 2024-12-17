School Management System API
A School Management System built with Django REST Framework (DRF), providing robust features for managing users, library records, Student fees, staff and role-based access control (RBAC). The project leverages Django's authentication system to secure operations and ensure streamlined access for different user roles.

Features
🔑 Role-Based Access Control (RBAC)
The system implements RBAC, where users are divided into specific roles with defined permissions:

Superuser: Has full access to all features, data, and users.
Staff: General staff responsible for administrative tasks such as managing student fees records and and viewing library history.
Librarian: Manages library resources and borrowing history.

📚 Library Management
The Librarian role can manage the library operations:
Add, edit, and delete book details.
Manage library resources (books, borrowing dates, status, which student borrowed the book and return dates).
Maintain a library history, tracking which books are borrowed, when, and by whom (using student_id).

💳 Fees Management
Students' fee details can be saved into the system.
Track and manage due payments for students.

🔐 Authentication
Integrated Django's authentication system for user login, password management, and security.
RBAC ensures users can only access operations relevant to their role.


Technologies Used
Django REST Framework: For building RESTful APIs.
Django Authentication: Secure login and user management.
RBAC: Role-based access control for defining permissions.
SQLite/PostgreSQL: Database for storing all records.
JSON: For API data exchange.
Phonenumbers: for validating user's phone number