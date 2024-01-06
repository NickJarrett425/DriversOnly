# DriversOnly

## Project Overview
DriversOnly is a web application designed to incentivize and improve the on-road performance of truck drivers. Developed for the trucking industry, the system allows companies (sponsors) to reward drivers with points for good behavior and enables drivers to redeem these points for products in their sponsor's catalog. The system is built on Django for the backend and Bootstrap for the frontend, utilizing the iTunes API for product catalog information.

## Installation and Development Instructions
### Local Setup
_Preface: If using Unix or MacOS, replace python with python3 in each command._
1. Clone the repository: **`git clone https://github.com/NickJarrett425/DriversOnly`**
2. Navigate to the project directory.
3. Set up a virtual environment: **`python -m venv venv`**
4. Activate the virtual environment:
⠀⠀• On Windows: **`venv\Scripts\activate`**
⠀⠀• On Unix or MacOS: **`source venv/bin/activate`**
5. Install dependencies: **'pip install -r requirements.txt`**
6. Create and apply database migrations: **`python manage.py migrate`**
7. Run the development server: **'python manage.py runserver`**
