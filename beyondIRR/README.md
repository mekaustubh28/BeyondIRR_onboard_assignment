# BeyondIRR Asset Management

## Summary
Built over Django Rest Framework, web application designed to manage user transactions and provide financial summaries. The application supports JWT authentication for secure access to various API endpoints.

## Installation
Please follow any of the 2 methods either setup entire project or built docker image.
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

### Method 2: (build docker image) (Please dont use this method prefer method 1.)
**NOTE**: No process is running at port `8000` Dont use docker to build image for this project. image will be build works completely fine but can't create superuser. still figuring out the issue. So use method 1 for all the functions like logs, allusers etc.
1. make sure you are at level of `Dockerfile`.
2. build your image.
    1. this will step a working directory `/app`.
    2. generate a public and private key file.
    3. install all the dependencies.
    4. make all the migrations and migrate.
    5. Expose the app to port `8000`.
```bash
docker build -t beyondirr .
```
3. Make the migrations.
    1. you will be inside /app of the image.(ls to see all the files.)
```bash
docker run -it beyondirr /bin/bash
python manage.py makemigrations && python manage.py migrate
```
4. create superuser.
```bash
python manage.py createsuperuser
```
5. While running `python manage.py createsuperuser` you will be promoted for Email, First Name, ARN_number(it will not be verified enter any), Password.
6. After creating superuser close the container bash with `Ctrl+D`.
7. Run the container.
```bash
docker run -p 8000:8000 beyondirr
```
Your application will be available at http://localhost:8000/. If everything goes well.
If it fail try stopping any container running at 8000.



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
