# Project Title

## Introduction
This project, a technical challenge by Savannah Informatics, is a Django API designed to manage orders, interact with a PostgreSQL database, and integrate with Africa's Talking for sending order confirmation messages to customers. The authentication system is powered by Django Allauth, and the entire application is containerized using Docker Compose. The deployment workflow includes CI/CD through a configured pipeline, with the final deployment hosted on Render.

## Objectives
1. **Order Management:** Create a Django API for efficient order management, ensuring seamless interactions with the PostgreSQL database.

2. **Africa's Talking Integration:** Utilize Africa's Talking to send timely and personalized order confirmation messages to customers upon successful order placement.

3. **Authentication:** Implement Django Allauth for a robust and secure authentication system, enhancing user management within the application.

4. **Containerization:** Employ Docker Compose to containerize the application, simplifying deployment and ensuring consistent environments across different systems.

5. **CI/CD Workflow:** Establish a Continuous Integration/Continuous Deployment (CI/CD) pipeline to automate testing, build, and deployment processes for efficient development and delivery.

6. **Render Deployment:** Deploy the application on Render, taking advantage of its scalable infrastructure and ease of use.

## Project Structure
- **`/app`:** Contains the Django application code.
- **`/docker-compose.yml`:** Docker Compose configuration file for containerization.
- **`.github/workflows`:** CI/CD workflows for automated testing and deployment.

## Getting Started
To run the application locally or deploy it on Render, follow the steps outlined in the [**Installation Guide**](#installation-guide) below.

## Installation Guide
1. Clone the repository:
    ```bash
    git clone https://github.com/<your-username>/<your-repo>.git
    ```

2. Navigate to the project directory:
    ```bash
    cd <your-repo>
    ```

3. Copy the example environment variables file and customize it:
    ```bash
    cp .env.example .env
    ```

4. Modify the `.env` file with your API keys, database configurations, and other necessary settings.

5. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

6. Access the Django API at `http://localhost:8000` in your web browser.

## CI/CD Workflow
The project is configured with a CI/CD workflow using GitHub Actions. On each push to the main branch, the workflow will trigger automated testing and deployment to Render. View the workflow details in the [**Actions tab**](../../actions) of the repository.

## Django API Views and URL Patterns
### `urls.py`
```python
<Replace with your urls.py code>
