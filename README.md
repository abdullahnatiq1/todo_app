# Todo List App

My Todo List App is build in FastAPI helps the user to store there tasks with tokenization

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
