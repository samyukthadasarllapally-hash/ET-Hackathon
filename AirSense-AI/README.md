# AirSense AI — AI-Powered Urban Air Quality Intelligence Platform

## Hackathon Project | Economic Times

---

## Project Structure

```
AirSense-AI/
├── frontend/        # React + Tailwind CSS
├── backend/         # FastAPI backend
│   ├── app.py
│   ├── routes/
│   │   ├── prediction.py
│   │   ├── chatbot.py
│   │   ├── maps.py
│   │   └── recommendations.py
│   └── requirements.txt
├── ai/              # ML models and RAG pipeline
├── data/            # AQI datasets
├── docs/            # SDD and documentation
├── docker/          # Docker configs
└── README.md
```

---

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

API runs at: http://localhost:8000
Swagger docs: http://localhost:8000/docs

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/prediction/forecast` | GET | AQI forecast 24/48/72h |
| `/api/chat/query` | POST | AI chatbot (RAG) |
| `/api/maps/heatmap` | GET | GeoJSON heatmap data |
| `/api/recommendations/citizen` | GET | Citizen health advisory |
| `/api/recommendations/government` | GET | Government inspection recommendations |

---

## Tech Stack

- **Frontend**: React + Tailwind CSS + Leaflet
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Vector DB**: FAISS
- **ML**: Scikit-learn / PyTorch
- **Agents**: LangGraph
