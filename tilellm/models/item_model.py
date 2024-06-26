from pydantic import BaseModel, Field,  validator, field_validator, ValidationError, BaseConfig
from typing import Dict, Optional, List
import datetime


class ItemSingle(BaseModel):
    id: str
    source: str | None = None
    type: str | None = None
    content: str | None =None
    gptkey: str | None = None
    embedding: str = Field(default_factory=lambda: "text-embedding-ada-002")
    namespace: str | None =None
    webhook: str = Field(default_factory=lambda: "")


class MetadataItem(BaseModel):
    id: str
    source: str | None = None
    type: str | None = None
    embedding: str = Field(default_factory=lambda: "text-embedding-ada-002")


class ChatEntry(BaseModel):
    question: str
    answer: str
    #metadata: Optional[Dict[str, str]] = None  # Optional field for additional data


class ChatHistory(BaseModel):
    chat_history: Dict[str, ChatEntry]

    @classmethod
    def from_dict(cls, data: dict) -> "ChatHistory":
        """Custom constructor to handle potential issues during initialization."""
        chat_history = {}
        for key, entry_data in data.items():
            try:
                if not isinstance(key, str):
                    raise ValueError(f"Invalid key type '{type(key)}'. Expected string.")
                chat_history[key] = ChatEntry(**entry_data)
            except (TypeError, ValueError) as e:
                raise ValidationError(f"Error processing entry '{key}': {str(e)}")
        return cls(chat_history=chat_history)
    

class QuestionAnswer(BaseModel):
    question: str
    namespace: str
    gptkey: str
    model: str =Field(default="gpt-3.5-turbo") 
    temperature: float = Field(default=0.0)
    top_k: int = Field(default=5)
    max_tokens: int = Field(default=128)
    embedding: str = Field(default_factory=lambda: "text-embedding-ada-002")
    system_context: Optional[str] = None
    chat_history_dict : Optional[Dict[str, ChatEntry]] = None

    @field_validator("temperature")
    def temperature_range(cls, v):
        """Ensures temperature is within valid range (usually 0.0 to 1.0)."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Temperature must be between 0.0 and 1.0.")
        return v

    @field_validator("top_k")
    def top_k_range(cls, v):
        """Ensures top_k is a positive integer."""
        if v <= 0:
            raise ValueError("top_k must be a positive integer.")
        return v


class RetrievalResult(BaseModel):
    answer: str = Field(default="No answer")
    sources: Optional[List[str]]|None =None
    source: str |None= None
    id: str |None= None
    namespace: str
    ids: Optional[List[str]]|None =None
    prompt_token_size: int = Field(default=0)
    success: bool = Field(default=False)
    error_message: Optional[str]|None =None
    chat_history_dict:Optional[Dict[str, ChatEntry]]


class PineconeQueryResult(BaseModel):
    id: str
    metadata_id: str
    metadata_source: str
    metadata_type: str
    text: Optional[str] | None = None


class PineconeItems(BaseModel):
    matches: List[PineconeQueryResult]


class PineconeItemToDelete(BaseModel):
    id: str
    namespace: str


class ScrapeStatusReq(BaseModel):
    id: str
    namespace: str
    namespace_list: Optional[List[str]] | None = None


class ScrapeStatusResponse(BaseModel):
    status_message: str =  Field(default="Crawling is not started")
    status_code: int =  Field(default=0)
    queue_order: int =  Field(default=-1)


class PineconeIndexingResult(BaseModel):
    #  {"id": f"{id}", "chunks": f"{len(chuncks)}", "total_tokens": f"{total_tokens}", "cost": f"{cost:.6f}"}
    id: str | None = None
    chunks: int | None = None
    total_tokens: int | None = None
    cost: str | None = None
    status: int = Field(default=300)
    date: str = Field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f"))
    error: Optional[str] | None = None


class PineconeItemNamespaceResult(BaseModel):
    namespace: str
    vector_count: int


class PineconeNamespaceResult(BaseModel):
    namespaces: Optional[List[PineconeItemNamespaceResult]]




