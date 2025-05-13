from typing import List
from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.schemas.schema import Player, PostTournament, Tournament
from app.models.tournament import Participant, Tournament as TournamentModel, engine_async


app = FastAPI()


async def get_async_session():
    async with AsyncSession(engine_async) as session:
        return session


@app.get('/tournaments/', tags=['tournaments'], summary='Get tournaments', responses={
    200: {
        'description': "Successful",
        "content": {
            "application/json": {
                'example': [{
                    "name": "Running Uzbekistan 2025",
                    "number of participants": 100,
                    'start_at': "2025-05-11T13:28:48.949387Z "
                }]
            }
        }
    }
})
async def get_tournaments():
    async with AsyncSession(engine_async) as session:
        data = select(TournamentModel)
        res = await session.execute(data)
        res = res.scalars().all()
        return JSONResponse({'data': [Tournament.model_validate(d).model_dump(mode='json') for d in res]}, status_code=200)


@app.post('/tournaments/', tags=['tournaments'], summary='Add tournament', status_code=status.HTTP_201_CREATED, response_model=Tournament, responses={
    201: {
        'description': "Successful",
        "content": {
            "application/json": {
                'example': {
                    "id": 1,
                    "name": "Running Uzbekistan 2025",
                    "max players": 100,
                    'start at': "2025-05-11T13:28:48.949387Z"
                }
            }
        }
    }
})
async def post_tournaments(tournament: PostTournament):
    async with AsyncSession(engine_async) as session:
        tour = TournamentModel(name=tournament.name, max_players=tournament.max_players, start_at=tournament.start_at)
        session.add(tour)
        await session.commit()
        await session.refresh(tour)
        return tour


@app.post('/tournaments/{tournament_id}/register', tags=['player'], summary='Add player', status_code=status.HTTP_201_CREATED, responses={
    201: {
        'Description': "Successfull",
        "content":{
            "application/json":{
                'example': {
                    "id": 1,
                    'name': 'John Doe',
                    'email': 'user@gmail.com'
                }
            }
        }
    }
})
async def register_player(tournament_id, player: Player, session: AsyncSession=Depends(get_async_session)):
    try:
        data = select(TournamentModel).options(selectinload(TournamentModel.players)).where(TournamentModel.id == int(tournament_id))
        res = await session.execute(data)
        tournament = res.scalar_one_or_none()
        if tournament:
            if tournament.max_players > len(tournament.players):
                participant = Participant(name=player.name, email=player.email, tournament_id=int(tournament_id))
                session.add(participant)
                await session.commit()
                await session.refresh(participant)
                return JSONResponse(content={"id": participant.id, "name": participant.name, "email": participant.email}, status_code=201)
            else:
                return JSONResponse({'error': f'This tournament is full. Allowed number of players is {tournament.max_players}'}, status_code=403)
        else:
            return JSONResponse({'error': 'Tournament model not found'}, status_code=404)
    except IntegrityError as e:
        await session.rollback()
        return JSONResponse(content={'error': f'email {player.email} is already exists'}, status_code=400)


@app.get('/tournaments/{tournament_id}/players/', tags=['player'], summary='Get players', response_model=List[Player])
async def get_players(tournament_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(TournamentModel).options(selectinload(TournamentModel.players)).where(TournamentModel.id == tournament_id)
    res = await session.execute(query)
    tournament: TournamentModel = res.scalar()
    return tournament.players


def main():
    import uvicorn
    uvicorn.run('app.main:app', reload=True)
