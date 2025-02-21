# Parket Technical Assessment

## Table Of Contents
- [Project Overview](#project-overview)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Installation Steps](#installation-steps)
  - [Database Setup](#database-setup)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Clients](#clients)
  - [Admin Users](#admin-users)
  - [Parket Users](#parket-users)

## Project Overview
A Django REST API for managing parking users across multiple clients. The system allows client administrators to manage their respective users through various endpoints including bulk operations.

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL
- pip (Python package manager)

### Installation Steps
1. Clone the repository
```bash
git clone <repository-url>
cd parket-technical-assessment
```

2. Create and activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
# On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

### Database Setup
1. Create PostgreSQL database (choose a method):

   Option A: Using psql (CLI):
   ```bash
   # Connect to PostgreSQL
   psql -U postgres

   # Create database
   CREATE DATABASE parketdb;

   # Verify database creation
   \l

   # Exit psql
   \q
   ```

   Option B: Using pgAdmin (GUI):
   1. Open pgAdmin
   2. Right-click on 'Databases' in the left sidebar
   3. Select 'Create > Database'
   4. Enter 'parketdb' as the name
   5. Click 'Save'

2. Configure database connection:
   Create a `.env` file in the project root:
   ```
   DB_NAME=parketdb
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=your_secret_key
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

### Running the Server Locally

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. The server will start at http://127.0.0.1:8000/
   - API endpoints will be available at http://127.0.0.1:8000/api/
   - Django admin interface at http://127.0.0.1:8000/admin/

## API Documentation

### Authentication
All endpoints except client and admin-user creation require basic authentication using client administrator credentials.
Include the authentication header:
```
Authorization: Basic <base64-encoded-credentials>
```
Where credentials are formatted as `username:password` and base64 encoded.

> [!TIP]
> It may be easier to use a tool like Postman to test the API endpoints.
> Postman will automatically encode the credentials for you and thus you only need to select "Basic Authentication" and provide the username and password values.

### Clients
#### Create Client
```bash
POST /api/clients/
Content-Type: application/json

{
    "name": "Client A"
}
```

### Admin Users
#### Create Admin User
```bash
POST /api/clients/admin-users/
Content-Type: application/json

{
    "username": "admin-a",
    "password": "securepass123",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User",
    "client_id": 1 # This must match an existing client ID
}
```

### Parket Users

#### List Parket Users
```bash
GET /api/parket-users/
```
Returns all parket users for clients you administer.

#### Create Parket User
```bash
POST /api/parket-users/
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "license_plate": "ABC123",
    "client_id": 1
}
```

#### Bulk Delete Users
Delete all users for a specific client:
```bash
DELETE /api/parket-users/client/{client-id}/bulk-delete/
```

#### Bulk Upload Users
Upload multiple users via CSV file:
```bash
POST /api/parket-users/client/{client-id}/bulk-upload/
Content-Type: multipart/form-data

file=example_users.csv
```

CSV file format:
```csv
first_name,last_name,email,license_plate
John,Doe,john@example.com,ABC123
Jane,Smith,jane@example.com,XYZ789
```

Note there is a example CSV file in the project root you can to test called: `example_users.csv`

Response Codes:
- 201: Users created successfully
- 400: Invalid request (missing fields, invalid CSV format)
- 404: Client not found or is unauthorized
