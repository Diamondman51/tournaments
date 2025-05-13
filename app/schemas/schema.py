import datetime
from pydantic import BaseModel, ConfigDict, field_validator, Field, EmailStr
from typing import Optional


class Tournament(BaseModel):
    id: int
    name: str
    max_players: int
    start_at: Optional[datetime.datetime] = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC))

    model_config = ConfigDict(
        from_attributes=True,
        # json_encoders={
        #     datetime.datetime: lambda v: v.strftime('%d.%m.%Y %H:%M')
        # }
        )
    
    
    # @field_validator('start', mode='before')
    # def check_start(cls, start):
    #     if isinstance(start, str):
    #         try:
    #             return datetime.datetime.strptime(start, '%d.%m.%Y %H:%M')
    #         except ValueError:
    #             raise ValueError("start must be in format DD.MM.YYYY HH:MM")
    #     return start

class PostTournament(BaseModel):
    name: str
    max_players: int
    start_at: Optional[datetime.datetime] = Field(default=datetime.datetime.now(datetime.UTC))


class Player(BaseModel):
    name: str
    email: EmailStr
