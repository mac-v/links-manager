# Flask API with Supabase - User, Links, and Categories

This project is a RESTful API built using Flask and Supabase for managing users, links, and categories. The application allows you to create users, add links to users, organize links by categories, and manage both links and categories.

## Features
- User registration, login, and JWT-based authentication.
- CRUD operations for links and categories.

## Prerequisites
- Python 3.x
- Flask
- Supabase account and setup

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repository-url.git
    cd your-repository-directory
    ```

2. Install dependencies:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Set up your Supabase project and configure your environment variables. Add the following to a `.env` file:
    ```bash
    DATABASE_URL=<your-database-url>
    SUPABASE_URL=<your-supabase-url>
    SUPABASE_KEY=<your-supabase-key>
    JWT_SECRET_KEY=<your-jwt-key>
    ```


4. **Automatic Table Creation**:
   Set up flask enviroment variables. Add the following to a `.flaskenv` file:
   ```bash
    FLASK_APP=links_manager.py
    FLASK_DEBUG=1
    FLASK_ENVIROMENT=development
    CREATE_DB=true
   ```
5. **Automatic Table Creation**:
   The application will automatically create the required tables.

   To run app:
   ```bash
   flask run
   ```

## Endpoints

### Authentication

- **Register user**
  - **URL:** `/register`
  - **Method:** `POST`
  - **Description:** Register a new user.

- **Login user**
  - **URL:** `/login`
  - **Method:** `POST`
  - **Description:** Login user and receive a JWT token.

- **Delete user**
  - **URL:** `/users/<uuid:user_id>`
  - **Method:** `DELETE`
  - **Description:** Delete the specified user (JWT required).

### Links

- **Get user links**
  - **URL:** `/users/<uuid:user_id>/links`
  - **Method:** `GET`
  - **Description:** Retrieve all links associated with the specified user.

- **Modify link**
  - **URL:** `/users/<uuid:user_id>/links/<uuid:link_id>`
  - **Method:** `PUT`
  - **Description:** Modify an existing user link.

- **Delete link**
  - **URL:** `/users/<uuid:user_id>/links/<uuid:link_id>`
  - **Method:** `DELETE`
  - **Description:** Delete an existing user link.

### Categories

- **Add category**
  - **URL:** `/categories`
  - **Method:** `POST`
  - **Description:** Add a new category.

- **Add link to category**
  - **URL:** `/users/<uuid:user_id>/links/<uuid:link_id>/category/<uuid:category_id>`
  - **Method:** `PUT`
  - **Description:** Assign a category to a link.

- **Delete category**
  - **URL:** `/categories/<uuid:category_id>`
  - **Method:** `DELETE`
  - **Description:** Delete a category (the `category_id` in associated links will be set to `NULL`).
