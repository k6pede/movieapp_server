from fastapi import APIRouter
import requests
from pydantic import BaseModel
from pydantic_settings import BaseSettings


class MovieRequest(BaseModel):
    movie_id : int

class Settings(BaseSettings):
    tmdb_api_key: str
    tmdb_api_access_token: str
    tmdb_base_url: str

    class Config:
        env_file = ".env"

# 環境変数群
settings = Settings()
api_key = settings.tmdb_api_key
api_access_token = settings.tmdb_api_access_token
tmdb_base_url = settings.tmdb_base_url
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_access_token}"
}

# TMDB API公式リファレンス
# https://developer.themoviedb.org/reference/intro/getting-started
router = APIRouter()

language = 'ja-JA'


@router.get('/movie/top', summary="人気top10の映画情報取得")
def getMovieTop10():
    """
    movie

    映画情報を人気(vote_average)順に10件取得します
    """
    # TMDb APIから映画のリストを取得するためのURL（&language=en-US）
    # page=1としているため、人気TOP10になる

    # TODO:日本語英語を切り替えられるようにする
    url = f'https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language={language}&page=1'
    response = requests.get(url)

    data = response.json()

    print(data)
    return {"info": data}

@router.get('/movie/{movie_id}', summary="映画情報取得")
def getMovieById(movie_id: int ):
    """
    movie

    指定したidの映画情報をTMDbから取得します
    お気に入りした映画ピンポイントの取得用
    """
    url = f'{tmdb_base_url}/{movie_id}?api_key={api_key}&language={language}'
    response = requests.get(url)

    data = response.json()

    print(data)
    return {"info": data}

