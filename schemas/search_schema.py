from enum import Enum
from datetime import datetime
from typing import Optional, List
from pathlib import Path

from pydantic import BaseModel, Field, UUID4
from db.models.search_table import Search


class Operator(str, Enum):
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    GE = "ge"
    LE = "le"


class Size(BaseModel):
    value: int = Field(..., description="File size in bytes")
    operator: Operator = Field(Operator.LE, description="Compare file size and field 'value'")


class Time(BaseModel):
    value: datetime = Field(..., description="Text to search in files")
    operator: Operator = Field(Operator.LE, description="Compare file creation time and field 'value'")


class SearchSettings(BaseModel):
    text: Optional[str] = Field(None, description="Text to search in files")
    file_mask: Optional[str] = Field(None, description="File name mask in glob format")
    size: Optional[Size] = Field(None, description="Size constraints")
    creation_time: Optional[Time] = Field(None, description="Creation time constraints")
    
    @classmethod
    def from_orm(cls, record: Search):
        return cls(**{
            "text": record.text,
            "file_mask": record.file_mask,
            "size": {
                "value": record.size_value, 
                "operator": record.size_operator
            },
            "creation_time": {
                "value": record.creation_time_value, 
                "operator": record.creation_time_operator
            }
        })

    class Config:
        schema_extra = {
            "example": {
                "text": "hello world",
                "file_mask": "*a*.???",
                "size": {
                    "value": 42000,
                    "operator": "gt"
                },
                "creation_time": {
                    "value": "2023-04-18T20:22:00Z",
                    "operator": "le"
                }
            }
        }


class SearchId(BaseModel):
    search_id: UUID4


class SearchResult(BaseModel):
    finished: bool = False
    paths: Optional[List[Path]] = None

    class Config:
        schema_extra = {
            "example": {
                "finished": True,
                "paths": ["Sysinternals Suite/AdaExplorer.shm",
                          "git/git-2.36.1.vfs.0.0.zip/bin/gita.exe"
                ]
            }
        }
