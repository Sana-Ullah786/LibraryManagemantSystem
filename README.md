# LibraryManagemantSystem

Folio3 Backend Project in FastAPI.

## Redis Setup for Windows

Redis is not officially supported by Windows, but there is a workaround using which it can be installed.
Follow the steps on this link: https://riptutorial.com/redis/example/29962/installing-and-running-redis-server-on-windows

You will have to run the redis-server.exe file before running this project. The REDIS_HOST and/or REDIS_PORT are to be updated in the env file if they are different.


README:
 Software Requirements

Python3.11.1
JavaScript
Node Js
Typescript
FastApi
Uvicorn
Redis
CircleCI
Installation:
Frontend Software

This repository contains the frontend software for the project. It is responsible for the user interface and interaction with the backend.

Installation

1. Clone the repository:
shell or terminal/Command Prompt
 git clone https://github.com/ahsan-kamal-sdq/LibraryManagementSystem.git
2.Install the dependency:
npm install


Usage
To start the frontend software, run the following command:
In Terminal : 
npm start

This will start the development server and launch the application in your default browser. Any changes made to the source code will automatically trigger a hot reload.

Folder Structure
The repository has the following folder structure:
src: Contains the source code files.
components: Contains reusable UI components.
contexts: Contains the context files for managing application state.
pages: Contains the main page components.
services: Contains the service files for making API requests.
styles: Contains global styles and CSS files.
utils: Contains utility/helper functions.
public: Contains static assets such as images and favicon.
Assets : Contains background Image and other assets.

Contributing
If you'd like to contribute to the project, please follow these steps:
Fork the repository.
Create a new branch for your feature/bug fix.
Make your changes and commit them.
Push your changes to your forked repository.
Submit a pull request.
Please ensure that your code follows the established coding style and conventions. Also, make sure to write unit tests for your code changes.
License
This project is licensed under the MIT License.

Backend Software

Table of Contents
Installation
Requirements
Setup Virtual Environment
Install Dependencies
Database Configuration
Running the Application
API Documentation
Testing
Continuous Integration and Deployment
Contributing
License
Installation
Before proceeding with the installation, ensure you have the following requirements:
Python 3.11+
Redis (for caching, optional)
Setup Virtual Environment
It is recommended to use a virtual environment to keep the project dependencies isolated. Follow these steps to set up a virtual environment:
Create a new virtual environment using venv:
python3 -m venv venv
Activate the virtual environment:

For Linux/Mac:
source venv/bin/activate

For Windows:
venv\Scripts\activate

Install Dependencies
To install the project dependencies, use the following steps:

Install Pipenv (if not already installed):
pip install pipenv

Install the project dependencies from the Pipfile:
pipenv install

Database Configuration
Configure the database settings in the .env file or through environment variables. Modify the following variables according to your setup:
DATABASE_URL=postgresql://username:password@host:port/database_name
SQLALCHEMY_DATABASE_URL_TEST="sqlite:///test.db"
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
JWT_SECRET_KEY = "<YOUR_JWT_KEY>"
JWT_ALGORITHM = "<ANY ALGORITHM>"
JWT_EXPIRE_TIME_IN_MINUTES = 180
# Refresh token expire time == 5 days.
JWT_REFRESH_EXPIRE_TIME_IN_MINUTES = 7200

Running the Application
To run the application locally, follow these steps:

Activate the virtual environment (if not already activated):

For Linux/Mac:
source venv/bin/activate
For Windows:
venv\Scripts\activate

Start the FastAPI server:
uvicorn app.main:app --reload
The application will be accessible at http://localhost:8000.
