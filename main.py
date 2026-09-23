from fastapi import FastAPI

from routers.customer import router as customer_router
from routers.user import router as user_router
from routers.invitation import router as invitation_router
from routers.activation import router as activation_router
from routers.approval import router as approval_router
from routers.rejection import router as rejection_router
from routers.ai_router import router as ai_router


app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "FDE Customer Management API"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


app.include_router(customer_router)
app.include_router(user_router)
app.include_router(invitation_router)
app.include_router(activation_router)
app.include_router(approval_router)
app.include_router(rejection_router)
app.include_router(ai_router)