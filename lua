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
├── app/                             # FastAPI app
│   ├── main.py                      
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
│   │   ├── order_item.py
│   │   ├── warehouse.py
│   │   ├── robot_task.py
│   │   └── customer.py              # New table for customer info
│   │            
│   ├── repositories/                # Database access layer
│   │   ├── __init__.py
│   │   └── home.py
│   │            
│   ├── routers/                     # API endpoint
│   │   ├── __init__.py
│   │   └── home.py
│   │            
│   ├── utils/
│   │   ├── api_responses.py
│   │   ├── error_messages.py
│   │   ├── error_types.py
│   │   ├── errors.py
│   │   └── rate_limiting.py     
│   │
│   ├── schemas/                     # Pydantic validation
│   │   └── __init__.py
│   │
│   ├── services/                    # Business logic layer
│   │   ├── __init__.py
│   │   ├── erp.py                   # ERPNext Adapter (empty)
│   │   └── robot.py                 # Robot Dispatcher (Mock) empty
│   │
│   └── tasks/
│       ├── __init__.py
│       └── queue.py                 # Redis Pub/Sub logic (empty)
│
└── tests/
    ├── __init__.py
    └── test_orders.py   