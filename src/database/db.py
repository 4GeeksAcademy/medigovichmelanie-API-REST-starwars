from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

db = SQLAlchemy()

# Exporta TODO lo necesario, incluyendo ForeignKey
__all__ = ['db', 'Mapped', 'mapped_column', 'relationship',
           'String', 'Integer', 'Boolean', 'ForeignKey', 'List', 'Optional']