# **vulnMDB: Vulnerable Movie Database Web App**
The *vulnMDB* (`Vulnerable Movie Database Web App`) is a intentionally insecure WebApp and REST API built using **Flask**. It provides functions like movie reviews, rating, searches, etc while intentionally including security vulnerabilities in them.

## **Features**
- Exposes movie-related information (titles, cast, ratings, etc)
- Intentionally vulnerable to **SQL Injection, XSS, IDOR and CORS issues**
- OpenAPI documentation available for API reference
- Designed for security testing using tools like **ZAP, Burp Suite and RapiDAST**

---

## **Setup Instructions**

### **1. Clone repository**
```sh
git clone https://github.com/Yadnyawalkya/vulnMDB.git
cd vulnMDB
```

### **2. Install dependencies**
```sh
pip install -r requirements.txt
```

### **3. Run the app**
```sh
python app.py
```
By default, the API is available at `http://localhost:5000`; and OpenAPI specification can be accessed at `http://localhost:5000/openapi.json`.

---

## **API Endpoints**
| Endpoint | Method | Description |
|----------|--------|------------|
| `/api/movies` | `GET` | Get a list of all movies |
| `/api/movies/<id>` | `GET` | Get details of a specific movie |
| `/api/movies/add` | `POST` | Add a new movie (**Vulnerable to SQL Injection**) |
| `/api/movies/search?query=<script>alert('XSS')</script>` | `GET` | Search movies (**Vulnerable to XSS**) |
| `/api/users/<id>/profile` | `GET` | Fetch user profiles (**Vulnerable to IDOR**) |

---

## **Disclaimer**
This project is intended for educational and security testing purposes only. It should not be used in a production environment. Its primary purpose is to test Dynamic Application Security Testing (DAST) with [RapiDAST](https://github.com/RedHatProductSecurity/rapidast) and it serve as a learning tool.

