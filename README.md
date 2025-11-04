# URL Shortener

A simple and handy URL shortening service built with Flask.

## Features

- Shorten long URLs
- Create custom short codes
- Click tracking and statistics
- Clean and responsive UI
- RESTful API support

## Kurulum

```bash
# # Install required packages
pip install -r requirements.txt

python url_shortener.py
```

The app will run at `http://localhost:5000`.

## Usage

### Web Interface
1. Go to the homepage
2. Enter the long URL you want to shorten
3. Optionally, define a custom code
4. Click “Shorten!”
5. Copy and share your new short URL

### API Endpoints

**Shorten a URL:**
```bash
POST /shorten
Content-Type: application/x-www-form-urlencoded

url=https://example.com&custom_code=mylink
```

**Statistics:**
```bash
GET /stats/<short_code>
```

**List All URLs:**
```bash
GET /api/all
```

## Technologies Used

- Python 3.x
- Flask
- HTML/CSS/JavaScript

## License

MIT License

## Developer

Celal AYDIN
