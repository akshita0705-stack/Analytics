# Analytics Project

This project is designed for analytics tasks and includes the following main components:

## Folder Structure
- `main.py`: Entry point for running analytics operations.
- `database.py`: Handles database connections and queries.
- `worker.py`: Contains background processing logic or worker functions.
- `__pycache__/`: Python cache files (auto-generated).

## Architecture Decision

This project uses asynchronous processing via a queue system. Events received by the API are placed into an in-memory queue, which is processed by a background worker (`worker.py`). This design decouples event ingestion from processing, allowing the API to respond quickly and handle bursts of incoming events. The queue ensures reliable, ordered processing and can be extended to use more robust systems (e.g., Redis, RabbitMQ) if needed.

## Database Schema

The database consists of a single table to store analytics events:

| Table Name: `events` |
|----------------------|
| id (INTEGER, PRIMARY KEY, AUTOINCREMENT) |
| event_type (TEXT) |
| event_data (TEXT) |
| timestamp (DATETIME) |

Example schema diagram:

```
+---------+--------------+-----------+----------+
|   id    | event_type   | event_data|timestamp |
+---------+--------------+-----------+----------+
| INTEGER |   TEXT       |   TEXT    | DATETIME |
+---------+--------------+-----------+----------+
```

## Setup Instructions

1. **Clone the repository**
2. **Create a virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
4. **Initialize the database** (if required):
   ```powershell
   python database.py --init
   ```
5. **Start the API server**:
   ```powershell
   python main.py
   ```
6. **Start the worker processor** (in a separate terminal):
   ```powershell
   python worker.py
   ```

## API Usage

### POST /event
Submit a new event to the system:

```powershell
curl -X POST http://localhost:5000/event -H "Content-Type: application/json" -d "{\"event_type\": \"click\", \"event_data\": \"buttonA\"}"
```

### GET /stats
Retrieve analytics statistics:

```powershell
curl http://localhost:5000/stats
```

## Notes
- Update `requirements.txt` with any required packages.
- Customize `database.py` for your database configuration.
- Extend `worker.py` for additional background tasks.

---
Feel free to modify and expand this project as needed for your analytics workflow.
