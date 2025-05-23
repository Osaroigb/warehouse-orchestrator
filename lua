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
│   ├── constants/
│   │   └── enums.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py              # SQLAlchemy session/engine
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── customer.py              # New table for customer info
│   │   ├── inventory.py
│   │   ├── order_item.py
│   │   ├── order.py
│   │   ├── robot_task.py
│   │   └── warehouse.py              
│   │            
│   ├── repositories/                # Database access layer
│   │   └── order_repo.py
│   │            
│   ├── routers/                     # API endpoint
│   │   ├── __init__.py
│   │   ├── home_route.py
│   │   └── order_route.py
│   │            
│   ├── schemas/                     # Pydantic validation
│   │   └── order_schema.py
│   │
│   ├── services/                    # Business logic layer
│   │   ├── order_service.py
│   │   ├── erp.py                   # ERPNext Adapter (non-existent)
│   │   └── robot.py                 # Robot Dispatcher (non-existent mock)
│   │
│   ├── utils/
│   │   ├── api_responses.py
│   │   ├── error_messages.py
│   │   ├── error_types.py
│   │   ├── errors.py
│   │   └── rate_limiting.py     
│   │
│   └── tasks/
│       ├── __init__.py
│       └── queue.py                 # Redis Pub/Sub logic (if needed)
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    │ 
    ├── integration/
    │   └── test_create_order.py 
    │
    ├── unit/
    │   ├── test_order_repo.py
    │   ├── test_order_service.py
    │   └── test_rate_limiter.py 
    │
    └── utils/
        └── test_helpers.py 