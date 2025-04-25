# URL Shortener API: A FastAPI-based service for creating and managing shortened URLs

This project provides a robust URL shortening service built with FastAPI and PostgreSQL. It allows users to convert long URLs into short, manageable links and handles redirections from shortened URLs to their original destinations. The service offers a clean REST API interface with efficient database operations for URL management.

The application implements a simple yet powerful architecture that separates concerns between URL handling, database operations, and API endpoints. It features secure database connections through environment variables and provides fast redirections for shortened URLs. The service generates unique short codes using a combination of letters and digits, ensuring reliable and collision-resistant URL mapping.

## Repository Structure
```
.
├── app/                          # Main application directory
│   ├── db.py                    # Database connection management
│   ├── main.py                  # FastAPI application entry point and route definitions
│   ├── Req_Res_Schemas.py       # Pydantic models for request/response validation
│   └── sqlCrud.py              # Database operations for URL management
├── README.md                    # Project documentation
└── requirements.txt            # Python package dependencies
```

## Usage Instructions
### Prerequisites
- Python 3.7 or higher
- PostgreSQL database server
- pip (Python package manager)

Required environment variables:
```
DB_HOST=<your-db-host>
DB_PORT=<your-db-port>
DB_NAME=<your-db-name>
DB_USER=<your-db-username>
DB_PASSWORD=<your-db-password>
```

### Installation

You can run this project either using traditional Python setup or Docker.

#### Option 1: Traditional Setup

1. Clone the repository:
```bash
git clone https://github.com/VedantPhatangare/url_shortener_api.git
cd <repository-directory>
```

2. Create and activate a virtual environment:
```bash
# On macOS and Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the PostgreSQL database:
```sql
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    long_url TEXT NOT NULL,
    short_url VARCHAR(8) UNIQUE NOT NULL
);
```

#### Option 2: Docker Setup

1. Clone the repository:
```bash
git clone https://github.com/VedantPhatangare/url_shortener_api.git
cd <repository-directory>
```

2. Create a .env file with your database configuration:
```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_password
```

3. Start the services:
```bash
docker-compose up -d
```

### Quick Start

1. Start the server (if using traditional setup):
```bash
uvicorn app.main:app --reload
```

2. Create a shortened URL:
```bash
curl -X POST "http://localhost:8000/shorten" \
     -H "Content-Type: application/json" \
     -d '{"long_url": "https://example.com/very/long/url"}'
```

3. Use the shortened URL:
Simply visit `http://localhost:8000/<short_code>` in your browser.

### More Detailed Examples

1. Creating a shortened URL with Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/shorten",
    json={"long_url": "https://example.com/very/long/url"}
)
print(response.json())
# Output: {"shorten _url": "http://localhost:8000/ab12cd3f"}
```

2. Handling redirects programmatically:
```python
import requests

response = requests.get("http://localhost:8000/ab12cd3f", allow_redirects=False)
if response.status_code == 307:
    print(f"Redirecting to: {response.headers['Location']}")
```

### Testing with Postman

1. Set up a new Postman Collection:
   - Create a new collection named "URL Shortener API"
   - Set base URL variable to `http://localhost:8000`

2. Create URL Shortening Request:
```
Method: POST
URL: {{base_url}}/shorten
Headers: 
  Content-Type: application/json
Body (raw JSON):
{
    "long_url": "https://example.com/very/long/url"
}

Expected Response (200 OK):
{
    "shorten _url": "http://localhost:8000/ab12cd3f"
}
```

3. Test URL Redirection:
```
Method: GET
URL: {{base_url}}/ab12cd3f

Expected Response: 307 Temporary Redirect
Response Headers should include:
Location: https://example.com/very/long/url
```

4. Error Test Cases:
```
- Empty long_url (POST /shorten):
  Expected: 404 Not Found with "long_url required" message
- Invalid short code (GET /invalid):
  Expected: 404 Not Found with "URL not found" message
```

### Troubleshooting

1. Database Connection Issues
- Error: "Could not connect to PostgreSQL database"
  - Verify environment variables are set correctly
  - Ensure PostgreSQL service is running:
    ```bash
    # On Linux
    sudo service postgresql status
    
    # On macOS
    brew services list
    ```
  - Check database connectivity:
    ```bash
    psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME
    ```

2. API Errors
- 404 Error on URL redirect:
  - Verify the short code exists in the database
  - Check the URL format in the request
  - Enable debug logging:
    ```bash
    uvicorn app.main:app --reload --log-level debug
    ```

## Data Flow
The URL shortener processes URLs through a straightforward flow: receiving a long URL, generating a unique short code, storing the mapping, and redirecting users when they access the short URL.

```ascii
[Client] ----POST /shorten----> [FastAPI Server] ----Insert----> [PostgreSQL]
                                      |
                                   Generate
                                  Short Code
                                      |
[Client] <---Short URL Response---- [FastAPI Server]

[Client] ----GET /{code}-----> [FastAPI Server] ----Query----> [PostgreSQL]
                                      |
                                   Lookup
                                      |
[Client] <---307 Redirect----- [FastAPI Server]
```

Key component interactions:
1. FastAPI handles HTTP requests and response formatting
2. Pydantic models validate incoming request data
3. Database connection pool manages PostgreSQL connections
4. Short code generator ensures unique 8-character codes
5. PostgreSQL stores URL mappings with unique constraints
6. Environment variables secure database credentials
7. HTTP redirects (307) maintain original URL semantics