# Flask API with Supabase - User, Links, and Categories

This project is a RESTful API built using Flask and Supabase for managing users, links, and categories.

## Features
- User registration, login, profile management, and JWT-based authentication.
- Listing, adding, modifying, and deleting links.
- Listing, adding, modifying, and associating categories with links.


## Prerequisites
- Python 3.11
- Flask
- Supabase account and setup

## Endpoints

API documentation is at "/swagger-ui" endpoint

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
   
3. To run server:
    ```bash
   flask run
    ```






