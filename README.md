# Best Cars Dealerships - Full-Stack Capstone

Best Cars Dealerships is a Django and React web application for browsing dealerships, filtering them by state, viewing customer reviews, and posting reviews after authentication.

## Project name

**Best Cars Dealerships Full-Stack Developer Capstone**

## Technology

- Django and SQLite for authentication, car data, proxy APIs, and server-rendered static pages
- React for login, registration, dealership, dealer details, and review forms
- Node.js/Express and MongoDB integration with a local JSON-fixture fallback
- Docker and GitHub Actions workflow support

## Local setup

```powershell
cd server
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The application is available at `http://127.0.0.1:8000/`. The public dealership API is available at `/djangoapp/get_dealers`; authenticated users can post reviews at `/djangoapp/add_review`.

## Main pages

- `/about` - company mission and leadership
- `/contact` - contact information
- `/dealers` - dealership list and state filter
- `/dealer/<id>` - dealer details and reviews
- `/postreview/<id>` - authenticated review form
