from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from auth.base_config import current_user
from .tasks import get_email_template_dashboard, send_email_report_dashboard

router = APIRouter(
    prefix='/tasks',
    tags=['Tasks'],
)


@router.get('/dashboard')
def get_task(user=Depends(current_user)):
    send_email_report_dashboard.delay(user.username)
    return {
        'status': '200',
        'data': 'Письмо отправлено',
        'details': None
    }
