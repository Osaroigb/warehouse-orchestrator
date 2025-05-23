warehouse-orchestrator/
├── alembic/
│   ├── versions/
│   └── env.py
│
├── alembic.ini
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
│
├── app/
│   ├── main.py                      # FastAPI app
│   ├── exception_handler.py   
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py              # SQLAlchemy session/engine
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── order.py
│   │   ├── inventory.py
│   │   ├── warehouse.py
│   │   ├── robot_task.py
│   │   └── customer.py              # New table for customer info
│   │            
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── orders.py
│   │   └── health.py 
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── order.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── erp.py                   # ERPNext Adapter
│   │   ├── robot.py                 # Robot Dispatcher (Mock)
│   │   └── logger.py
│   └── tasks/
│       ├── __init__.py
│       └── queue.py                 # Redis Pub/Sub logic
│
└── tests/
    ├── __init__.py
    └── test_orders.py   