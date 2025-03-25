from pydantic import BaseModel
from typing import List, Optional

class FileContext(BaseModel):
    filename: str
    content: str

class CodeChange(BaseModel):
    line: int
    original: str
    suggested: str

class Suggestion(BaseModel):
    file: str
    changes: List[CodeChange]
    reasoning: Optional[str] = None

class Approval(BaseModel):
    file: str
    approved: bool

class Fact(BaseModel):
    key: str
    value: str

class Conversation(BaseModel):
    text: str

class User(BaseModel):
    user_id: int
    username: str
