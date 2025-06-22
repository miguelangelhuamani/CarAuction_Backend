# 🛠️ Plan B – Car Auction Platform (Backend)

**Backend API** for **Plan B**, a modern car auction platform where users can browse vehicle listings, place bids, rate auctions, leave comments, and manage their profiles. Built with **Django REST Framework**, this backend exposes RESTful endpoints for all the platform's functionality.

This is the backend half of a full-stack application, and it provides RESTful APIs for authentication, auction management, bidding, comments, and users functionality. The frontend, developed with React/Next.js, is available in my other [repository](https://github.com/miguelangelhuamani/CarAuction_Frontend.git) and interacts with this backend to deliver a seamless auction experience.

## 💡 Features

- 🔐 JWT authentication with user registration and login
- 🚗 Create, edit, and delete auctions 
- 💸 Bid system for real-time auction participation
- 💬 Comment and rating functionality
- 🧑 Profile management and user-specific actions
- 📄 Auto-generated OpenAPI documentation with Swagger (drf-spectacular)

---

## ⚙️ Tech Stack

- **Python 3.10+**
- **Django REST Framework**
- **SimpleJWT** for secure token-based auth
- **SQLite** (easy dev) or **PostgreSQL** (production-ready)
- **drf-spectacular** for API schema and Swagger UI

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/miguelangelhuamani/CarAuction_Backend.git
cd PlanB_Backend
cd planBackend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a .env file and add:

```bash
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```
If using PostgreSQL, configure the DB accordingly.

### 5. Apply migrations and create a superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```
The API will be available at:
```bash
http://localhost:8000/api/
```

## 🖥️ Frontend Client (IMPORTANT)

This backend is designed to work with the CarAuction_Frontend project, which provides the user interface for the platform. Make sure the frontend is running locally and configured to point to this backend’s API base URL. All interaction with the backend (such as creating auctions or placing bids) is performed through the frontend interface.

Instructions for running the frontend are provided in its README [here](https://github.com/miguelangelhuamani/CarAuction_Frontend.git).


## 📄 API Documentation
Thanks to drf-spectacular, Swagger UI is automatically available at:

```bash
http://localhost:8000/api/schema/swagger-ui/
```

You can also access the raw schema:
```bash
http://localhost:8000/api/schema/
```