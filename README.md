# FastAPI Xero Integration

This project is a FastAPI application that integrates with Xero's OAuth2 authentication and API interaction.

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/Sujan167/Xero_OAuth.git
    cd Xero_OAuth
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a **.env** file based on the **.env-sample** file and fill in the required environment variables:
    ```sh
    cp .env-sample .env
    ```

5. Set up the application in Xero's Developer Portal:
    - Go to [Xero Developer Portal](https://developer.xero.com/myapps).
    - Click on "New App".
    - Fill in the required details such as app name, company or application URL, and redirect URI (e.g., `https://localhost:8000/auth/callback`).
    - After creating the app, you will get the `Client ID` and `Client Secret`. Add these to your **.env** file as `XERO_CLIENT_ID` and `XERO_CLIENT_SECRET`.

6. Generate self-signed certificates for development:
    **NOTE:** Since Xero OAuth requires the application to be secured (https), use a self-signed certificate in the development environment.
    ```sh
    mkdir -p ./certs
    openssl genpkey -algorithm RSA -out ./certs/key.pem -pkeyopt rsa_keygen_bits:2048
    openssl req -new -key ./certs/key.pem -out ./certs/csr.pem
    openssl x509 -req -days 365 -in ./certs/csr.pem -signkey ./certs/key.pem -out ./certs/cert.pem
    ```

7. Run the application:
    ```sh
    python main.py
    ```


## Endpoints

### Authentication

- **GET /auth/login**: Redirects the user to Xero's OAuth authorization page.
- **GET /auth/callback**: Handles the callback from Xero and exchanges the authorization code for an access token.
- **POST /auth/refresh**: Refreshes the access token using the refresh token stored in the cookies.

### Accounts

- **GET /account/chart-of-accounts**: Retrieves the Chart of Accounts from Xero and stores them in the database.

## Configuration

The application uses environment variables for configuration. These variables are defined in the **.env**file:

- `XERO_CLIENT_ID`: Your Xero client ID.
- `XERO_CLIENT_SECRET`: Your Xero client secret.
- `XERO_REDIRECT_URI`: The redirect URI for your Xero application.
- `DATABASE_URL`: The database connection URL.
- `ENVIRONMENT`: The environment in which the application is running (e.g., `DEV` or `PROD`).

## Example endpoint
- **https://sujanb.com.np/auth/login**: Redirects user to Xero's OAuth authorization page.
- **https://sujanb.com.np/account/chart-of-accounts**: Retrieves the Chart of Accounts from Xero and stores them in the database.

## Logging

The application logs information to both the console and a log file located at app/utils/app.log.

## License

This project is licensed under the MIT License.