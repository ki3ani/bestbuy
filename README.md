# Best Buy

## Introduction
This project is a Django DRF  API designed to manage orders, interact with a PostgreSQL database, and integrate with Africa's Talking for sending order confirmation messages to customers. The authentication system is powered by Django Allauth, and the entire application is containerized using Docker Compose. The deployment workflow includes CI/CD through a configured pipeline, with the final deployment hosted on Render.

## Objectives
1. **Order Management:** Create a Django API for efficient order management, ensuring seamless interactions with the PostgreSQL database.

2. **Africa's Talking Integration:** Utilize Africa's Talking to send timely and personalized order confirmation messages to customers upon successful order placement.

3. **Authentication:** Implement Django Allauth for a robust and secure authentication system, enhancing user management within the application.

4. **Containerization:** Employ Docker Compose to containerize the application, simplifying deployment and ensuring consistent environments across different systems.

5. **CI/CD Workflow:** Establish a Continuous Integration/Continuous Deployment (CI/CD) pipeline to automate testing, build, and deployment processes for efficient development and delivery.

6. **Render Deployment:** Deploy the application on Render, taking advantage of its scalable infrastructure and ease of use.

## Functional Requirements
1. **Home Page:**
   - Upon visiting the page, users are redirected to the home page.
   - The home page displays all items available for sale.

     ### Home Page - View Items for Sale

     **Endpoint:** [https://bestbuy-bqey.onrender.com/](https://bestbuy-bqey.onrender.com/)

     **Method:** GET

     **Description:**
     - This endpoint represents the home page of the application where users can view items available for sale.
     - When users visit this endpoint, they receive a list of items along with their details.

     **Sample Response:**
     ```json
     [
         {
             "id": 1,
             "name": "Iphone 15",
             "price": "1350.00",
             "description": "a nice iPhone for school",
             "in_stock": true
         },
         {
             "id": 2,
             "name": "Pizza",
             "price": "5.00",
             "description": "Hawaiian",
             "in_stock": true
         },
         {
             "id": 3,
             "name": "Sedan",
             "price": "45000.00",
             "description": "a gently used sedan",
             "in_stock": true
         }
     ]
     ```

2. **Authentication:**
   - Users must sign in or register to make an order.
   - Customer registration is required for placing orders.
  
      ### Registration and Login

   **User Registration**

   - To register a new account, users can visit the signup page.
   - The registration form includes fields for email, password, and phone number.

   **Endpoint:** [https://bestbuy-bqey.onrender.com/accounts/signup/](https://bestbuy-bqey.onrender.com/accounts/signup/)

   **Method:** POST

   **Request:**
   - Headers:
     - Content-Type: application/json
     - CSRF-Token: `<your_csrf_token>` <!-- Placeholder for CSRF token -->
   - Body:
     ```json
     {
         "email": "user@example.com",
         "password1": "your_password",
         "password2": "your_password",
         "phone_number": "your_phone_number" <!-- Placeholder for phone number -->
     }
     ```

   **Response:**
   - Successful Registration:
     ```json
     {
         "message": "Registration successful. Please check your email for verification."
     }
     ```
   - Failed Registration:
     ```json
     {
         "error": "Registration failed. Please check your input and try again."
     }
     ```

   **User Login**

   - To log in, users can visit the login page.
   - The login form includes fields for email and password.

   **Endpoint:** [https://bestbuy-bqey.onrender.com/accounts/login/](https://bestbuy-bqey.onrender.com/accounts/login/)

   **Method:** POST

   **Request:**
   - Headers:
     - Content-Type: application/json
     - CSRF-Token: `<your_csrf_token>` <!-- Placeholder for CSRF token -->
   - Body:
     ```json
     {
         "email": "user@example.com",
         "password": "your_password"
     }
     ```

   **Response:**
   - Successful Login:
     ```json
     {
         "message": "Login successful. Welcome back, user!"
     }
     ```
   - Failed Login:
     ```json
     {
         "error": "Login failed. Please check your credentials and try again."
     }
     ```

   **Third-Party Authentication**

   - Users can also register or log in using third-party services like Google.

  - ![Google Login](/cleanstore/pics/google.png)



3. **Order Placement:**
   - After signing in, customers can browse items and place orders.
     
  
      **Order Placement**

   **Place Order**

   - Authenticated users can place orders for items.
   - The order placement form includes the item details and quantity.

   **Endpoint:** [https://bestbuy-bqey.onrender.com/orders/](https://bestbuy-bqey.onrender.com/orders/)

   **Method:** POST

   **Request:**
   - Headers:
     - Authorization: Bearer `<your_access_token>` <!-- Placeholder for access token -->
     - Content-Type: application/json
     - CSRF-Token: `<your_csrf_token>` <!-- Placeholder for CSRF token -->
   - Body:
     ```json
     {
         "item_id": 1,
         "quantity": 2
     }
     ```

   **Response:**
   - Successful Order Placement:
     ```json
     {
         "message": "Order placed successfully. Confirmation sent via text message."
     }
     ```
   - Failed Order Placement:
     ```json
     {
         "error": "Order placement failed. Please check your input and try again."
     }
     ```

   **View Orders**

   - Authenticated users can view a list of their placed orders.

   **Endpoint:** [https://bestbuy-bqey.onrender.com/orders/](https://bestbuy-bqey.onrender.com/orders/)

   **Method:** GET

   **Response:**
   ```json
   [
       {
           "order_id": 1,
           "item_name": "Iphone 15",
           "quantity": 2,
           "total_price": "2700.00",
           "status": "Processing"
       },
       {
           "order_id": 2,
           "item_name": "Pizza",
           "quantity": 1,
           "total_price": "5.00",
           "status": "Delivered"
       }
   ]


4. **Order Confirmation:**
   - Upon order placement, an order confirmation is sent via text (using Africa's Talking) to the customer.
   - ![Message](/cleanstore/pics/messo.jpeg)
  
5. **Admin Privileges:**
   - Only administrators can create items for sale.
   - Admins have exclusive rights to manage and add new items.

  
   ### Continuous Integration (CI)

This project uses GitHub Actions for Continuous Integration. The CI workflow consists of two jobs: `test` and `build-and-push-docker`. Here's an explanation of each job:

#### Job: `test`

- **Trigger:** This job runs on every push to the `main` branch.
- **Environment Setup:**
  - It runs on an `ubuntu-latest` machine.
  - Configures a PostgreSQL service container with specified environment variables and health check options.
  - Sets environment variables required for the Django application (e.g., Africa's Talking API key, username, and database host).
- **Steps:**
  - Checks out the repository.
  - Sets up Python 3.10.
  - Installs Python dependencies listed in `requirements.txt`.
  - Waits for the PostgreSQL service to be ready using a loop with `pg_isready`.
  - Applies Django migrations.
  - Runs Django tests using `python manage.py test`.

#### Job: `build-and-push-docker`

- **Dependencies:** This job depends on the successful completion of the `test` job.
- **Trigger:** It also runs on every push to the `main` branch.
- **Steps:**
  - Checks out the repository.
  - Logs in to Docker Hub using credentials from secrets.
  - Builds and pushes Docker images (`web` and `nginx`) using Docker Compose. The environment variable `DJANGO_SETTINGS_MODULE` is set to specify the development settings for Django.

This workflow ensures that tests pass and, if successful, builds and pushes Docker images to Docker Hub. The separation of `test` and `build-and-push-docker` allows for controlled and efficient CI/CD.
  

