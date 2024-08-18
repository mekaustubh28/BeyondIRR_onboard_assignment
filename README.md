# BeyondIRR Asset Management

## Summary
Built over Django Rest Framework, web application designed to manage user transactions and provide financial summaries. The application supports JWT authentication for secure access to various API endpoints.

**Note:** dont use docker method for building the project prefer local method as there is some issue with docker not creating superuser in the project. I have created it for the browine points :)
## Installation

### Method 1: (setup entire project)
You will see Dockerfile inside the code. Please run code using this method as there is some issue setting project with database and docker container. Please use Method 1 only.
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
Before Testing make sure to place file `template.xlsx` and `missing_values.xlsx` excel file at same level of 
`manage.py`.\
[Download](https://github.com/BeyondIRR/sample-assignment/blob/main/template.xlsx) `template.xlsx`.\
Copy Paste `template.xlsx` and remove some of the entries from it to create `missing_values.xlsx`.\
Run Tests using 
```bash
python manage.py test
```
If you want to have high code coverage to ensure that most of your code is tested. Use tools like `pytest-cov` or `coverage.py` to measure and report code coverage.

Make sure to have require dependencies `pytest-django`, `pytest-cov`, `pytest`
```bash
pip install pytest pytest-django pytest-cov
```
Run High Converage Testing
```bash
DJANGO_SETTINGS_MODULE=beyondIRR.settings pytest assets/tests.py --cov=assets --cov-report=html --cov-report=term-missing
```
```bash
DJANGO_SETTINGS_MODULE=beyondIRR.settings pytest transaction/tests.py --cov=transaction --cov-report=html --cov-report=term-missing
```


## References
Here are most of the Links I referred to for my guidance.
1. https://chatgpt.com/share/00116e0a-eaa9-4b45-8887-8562df01e08a (How to configure Swagger with DRF)
2. https://www.amfiindia.com/locate-your-nearest-mutual-fund-distributor-details (arn_number validation)
3. https://www.django-rest-framework.org/ (How to configure DRF)
4. https://docs.djangoproject.com/en/5.0/topics/testing/tools/ (How to write unit tests in django)
5. https://www.django-rest-framework.org/#example (Create a serializer for model)
6. https://pytest-cov.readthedocs.io/en/latest/config.html (High End Test converage reference).
7. https://dockertraining.readthedocs.io/en/latest/django/ (Dockerization of the project)

# Thank you for reading so far.
