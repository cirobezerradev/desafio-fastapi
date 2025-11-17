from fastapi import FastAPI

from app.routers import atleta, categoria, centro_treinamento

app = FastAPI(title='WorkoutAPI', description='API de competição de crossfit')

# Inclusão de Rotas
app.include_router(atleta.router)
app.include_router(categoria.router)
app.include_router(centro_treinamento.router)
