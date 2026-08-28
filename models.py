import datetime
import json
from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base


class Generation(Base):
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True, index=True)
    part = Column(String, nullable=False)
    params = Column(Text, nullable=False)  # JSON string
    filename = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "part": self.part,
            "params": json.loads(self.params),
            "filename": self.filename,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
