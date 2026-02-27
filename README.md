# Todo List App

A RESTful API backend for a Todo application built with FastAPI and PostgreSQL.

## Features

User authentication with signup and signin

Passwords are securely hashed using bcrypt

JWT token based authentication

Full CRUD operations for todos (Create, Read, Update, Delete)

Each user can only access and manage their own todos

Database managed with SQLModel and PostgreSQL

# Get Started

## Prerequisties

We need PostGresSQL Database for this project

## Setting Up the Environment

First create .env file in the root of the project and add PostGresSQL database URL

```
DATABASE_URL=your-db-connection-string
```

## Create and Activate your Virtual Enironment

```
python -m venv .venv
.venv\Scripts\activate
```

## Install Dependencies

```
pip install -r requirements.txt
```

## Run the Server

```
uvicron main:app --reload
```
