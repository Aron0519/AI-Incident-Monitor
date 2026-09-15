from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    status = Column(String, nullable=False, default="unknown")

    incidents = relationship("Incident", back_populates="service")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    status = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    message = Column(String, nullable=False)

    service = relationship("Service", back_populates="incidents")

    @property
    def service_name(self):
        return self.service.name