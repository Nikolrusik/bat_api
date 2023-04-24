from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Table, Boolean, Column, MetaData, Integer, String, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

metadata = MetaData()

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    metadata = metadata

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
            String(length=320), unique=True, index=True, nullable=False
        )
    hashed_password: Mapped[str] = mapped_column(
            String(length=1024), nullable=False
        )
    registered_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)        
    is_superuser: Mapped[bool] = mapped_column(
            Boolean, default=False, nullable=False
        )
    is_verified: Mapped[bool] = mapped_column(
            Boolean, default=False, nullable=False
        )