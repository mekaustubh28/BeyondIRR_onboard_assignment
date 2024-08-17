# BeyondIRR Asset Management

## Summary
Built over Django Rest Framework, web application designed to manage user transactions and provide financial summaries. The application supports JWT authentication for secure access to various API endpoints.

## Installation

### Method 1: (setup entire project)
1. clone repository
```bash
git clone https://github.com/mekaustubh28/BeyondIRR_onboard_assignment
cd BeyondIRR_onboard_assignment
```
3. create virtual environment and activate it.
```bash
python -m venv venv
source venv/bin/activate
```
2. install dependencies
```bash
pip install -r requirements.txt
cd beyondIRR
```
3. create private key and public key for RS256 encryption and decryption and generation of JWT token.\
make sure pem files are at same level as manage.py ie they are at BASE DIRECTORY of project.
```bash
openssl genpkey -algorithm RSA -out private_key.pem 
openssl rsa -pubout -in private_key.pem -out public_key.pem
```
4. run migrations for database.
```bash
python manage.py makemigrations
python manage.py migrate
```
5. create superuser. Enter Email, First Name, ARN_Number(it will not verify for superuser), Password.
```bash
python manage.py createsuperuser
```
6. Collect Static files
```bash
python manage.py collectstatic
```
7. Run the Development Server
```bash
python manage.py runserver
```

Your application will be available at http://localhost:8000/.

## Endpoints
To Try Endpoints head to http://localhost:8000/swagger/
Extensive Documentation of all the Endpoints is given at swagger-ui for the project.

### Steps to use endpoints.
1. head to `/signup/` create New User if not created already with all the parameters.
2. head to `/login/` Login User using email and password generate JWT token.
3. use JWT Bearer Token to use other necessary endpoints.

## Testing
Run Tests using 
```bash
python manage.py test
```
