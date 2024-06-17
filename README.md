# Todo App

A web application using Flask as the backend framework and MongoDB
as the database. The application should allow users to manage a collection of ToDos, with JWT token validation using middleware.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Docker
- Docker Compose

### Running the Application

To run the application locally using Docker Compose:

#### 1. Clone the repository:
```bash
  git clone https://github.com/paramteraiya/ToDos-python
  cd ToDos-python
```

#### 2. Build and start containers:
```bash
  docker-compose up -d --build
```

#### 3. Access the application:
- The Flask application will be accessible at `http://localhost:5000`
- MongoDB will be running on `mongodb://localhost:27017`


## Importing Postman Collection
To test the API endpoints, you can import the provided Postman collection:
## API Endpoint Order
1. **Register a new user**
   - Endpoint: `/auth/register`
   - Payload: `{ "email": "your_email@example.com", "password": "your_password" }`
   - Method: `POST`

2. **Authenticate and obtain a JWT token**
   - Endpoint: `/auth/login`
   - Payload: `{ "email": "your_email@example.com", "password": "your_password" }`
   - Method: `POST`
   - The response will contain a JWT token, which should be included in the `Authorization` header for subsequent requests.

3. **Create a new ToDo item**
   - Endpoint: `/items`
   - Payload: `{ "name": "ToDo Title", "description": "ToDo Description" }`
   - Method: `POST`
   - Include the JWT token in the `Authorization` header: `Bearer <your_jwt_token>`

4. **Retrieve all ToDo items**
   - Endpoint: `/items`
   - Method: `GET`
   - Include the JWT token in the `Authorization` header: `Bearer <your_jwt_token>`

5. **Update a ToDo item**
   - Endpoint: `/items/<todo_id>`
   - Payload: `{ "name": "Updated ToDo Title", "description": "Updated ToDo Description" }`
   - Method: `PUT`
   - Include the JWT token in the `Authorization` header: `Bearer <your_jwt_token>`

6. **Delete a ToDo item**
   - Endpoint: `/items/<todo_id>`
   - Method: `DELETE`
   - Include the JWT token in the `Authorization` header: `Bearer <your_jwt_token>`