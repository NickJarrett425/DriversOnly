# DriversOnly.org

Founding Developers: Nicholas Jarrett, David Bradley, Neil Kuehn, and Dhruvisha Patel

## Project Overview
DriversOnly is a web application designed to incentivize and improve the on-road performance of truck drivers. Developed for the trucking industry, the system allows companies (sponsors) to reward drivers with points for good behavior and enables drivers to redeem these points for products in their sponsor's catalog. The system is built on Django for the backend and Bootstrap for the frontend, utilizing the iTunes API for product catalog information. This project is a proof of concept.

Other Technologies Used: Amazon RDS, Amazon EC2, Amazon SES, Amazon Route53, and Apache

## Installation and Development Instructions
### Local Setup
_Note: If using Unix or MacOS, replace python with python3 in each command._
1. Clone the repository: **`git clone https://github.com/NickJarrett425/DriversOnly`**
2. Navigate to the project directory.
3. Set up a virtual environment: **`python -m venv venv`**
4. Activate the virtual environment:
    - On Windows: **`venv\Scripts\activate`**
    - On Unix or MacOS: **`source venv/bin/activate`**
5. Install dependencies: **`pip install -r requirements.txt`**
6. Create and apply database migrations: **`python manage.py migrate`**
7. Run the development server: **`python manage.py runserver`**

### Working on the Project
1. Create a new branch for your feature/bug fix: **`git checkout -b [branch_name]`**
2. Make changes to the codebase.
3. Test your changes thoroughly.
4. Commit your changesL **`git commit -m "Your descriptive message"`**
5. Push the branch to the repository: **`git push origin [branch_name]`**
6. Create a pull request on GitHub.

## Bug Reporting and Contributions
Found a bug? Please submit an issue using the "Issues" tab above. If you want to contribute by fixing the bug or adding a new features, please submit a pull request referencing the issue you created.

## Demo Video
<p align="center">
[<img src="https://github.com/NickJarrett425/DriversOnly/blob/main/Website/static/Thumbnail.PNG" width="50%">](https://www.youtube.com/watch?v=AJJjYWOMbn4 "DriversOnly.org")
</p>
