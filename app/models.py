"""
This module defines the SQLAlchemy models for the fitness club application, including User, YogaClass, session, schedule, bookings and instructor. 
Each model corresponds to a table in the PostgreSQL database and includes fields for storing relevant information, as well as timestamps 
for creation and updates. The models also establish relationships between users, yoga classes, sessions, schedules, bookings and instructors

"""


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    yoga_sessions: Mapped[list["YogaSession"]] = relationship("YogaSession", secondary="bookings", back_populates="users")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="user")


class YogaClass(Base):
    __tablename__ = "yoga_classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    instructor: Mapped[list["Instructor"]] = relationship("Instructor", secondary="schedules", back_populates="yoga_classes")
    yoga_sessions: Mapped[list["YogaSession"]] = relationship("YogaSession", back_populates="yoga_class")
    schedules: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="yoga_class")


class Instructor(Base):
    __tablename__ = "instructors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    bio: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    yoga_classes: Mapped[list["YogaClass"]] = relationship("YogaClass", secondary="schedules", back_populates="instructor")
    yoga_sessions: Mapped[list["YogaSession"]] = relationship("YogaSession", back_populates="instructor")
    schedules: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="instructor")


class YogaSession(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    instructor_id: Mapped[int] = mapped_column(Integer, ForeignKey("instructors.id"), nullable=False)
    yoga_class_id: Mapped[int] = mapped_column(Integer, ForeignKey("yoga_classes.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    max_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    current_bookings: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    instructor: Mapped["Instructor"] = relationship("Instructor", back_populates="yoga_sessions")
    yoga_class: Mapped["YogaClass"] = relationship("YogaClass", back_populates="yoga_sessions")
    users: Mapped[list["User"]] = relationship("User", secondary="bookings", back_populates="yoga_sessions")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="session")


class Schedule(Base):
    __tablename__ = "schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    yoga_class_id: Mapped[int] = mapped_column(Integer, ForeignKey("yoga_classes.id"), nullable=False)
    instructor_id: Mapped[int] = mapped_column(Integer, ForeignKey("instructors.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    weekday: Mapped[int] = mapped_column(Integer, nullable=False) # 0=Monday, 6=Sunday
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    yoga_class: Mapped["YogaClass"] = relationship("YogaClass", back_populates="schedules")
    instructor: Mapped["Instructor"] = relationship("Instructor", back_populates="schedules")


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("sessions.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="booked") # booked, cancelled, attended
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="bookings")
    session: Mapped["YogaSession"] = relationship("YogaSession", back_populates="bookings")

    __table_args__ = (UniqueConstraint("user_id", "session_id", name="unique_user_session_booking"),)
    