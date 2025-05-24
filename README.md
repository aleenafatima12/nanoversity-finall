# NanoVersity - Online Learning Platform

---

## How to Set Up and Run the Project

### 1. Install Python

Make sure Python 3 is installed.  
Check by running:

```bash
python --version
```
If not installed, download it from [https://www.python.org/](https://www.python.org/).

---

### 2. Create a Virtual Environment

Inside the project folder, create a virtual environment:

```bash
python -m venv .venv
```

---

### 3. Activate the Virtual Environment

- **Windows**:

```bash
.venv\Scripts\activate
```
- **macOS/Linux**:

```bash
source .venv/bin/activate
```

---

### 4. Install Dependencies

Install Flask and any other packages:

```bash
pip install flask
```
Or, if `requirements.txt` is provided:

```bash
pip install -r requirements.txt
```

---

### 5. Initialize the Database

First, run the application to create the `database.db`:

```bash
python app.py
```
After the server starts, stop it once using `CTRL+C`.

---

### 6. Insert Demo Courses

Run the seeding script to insert 10 demo courses:

```bash
python seed_courses.py
```
You should see the message: "10 Courses inserted successfully!"

---
### For finding secret key run following command:
python3 -c "import secrets; print(secrets.token_hex(16))"

---
### 7. Start the Flask Server

Run the server again:

```bash
python app.py
```

You can now access the application at:

```
http://localhost:5000/
```

---

### 8. Access the Application

- Open your web browser and go to `http://localhost:5000/`
- Register a new account
- Login
- Browse courses
- Add to cart
- Proceed to simulated payment
- View enrolled courses on the dashboard

---

### 9. Important Notes

- Python may generate `__pycache__/` and `.pyc` files automatically; they are not required to be submitted.
- Do **not** submit the `.venv/` folder in any project delivery.
- If database schema is updated later, delete `database.db` and reinitialize by running `app.py` again.
- Payment functionality is simulated and does not involve real transactions.

---

