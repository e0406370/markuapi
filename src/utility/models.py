from msgspec import Struct
from pydantic import BaseModel, Field


class AnimeDataClip(Struct):
    anime_series_id: int
    anime_season_id: int
    count: int


class AnimeDataMark(Struct):
    anime_series_id: int
    anime_season_id: int
    count: int


class DramaDataClip(Struct):
    drama_series_id: int
    drama_season_id: int
    count: int


class DramaDataMark(Struct):
    drama_series_id: int
    drama_season_id: int
    count: int


class MovieDataClip(Struct):
    movie_id: int
    count: int


class MovieDataMark(Struct):
    movie_id: int
    count: int


class ReviewParams(BaseModel):
    page: int = Field(1, gt=0, le=10000)


class SearchParams(BaseModel):
    limit: int = Field(10, gt=0, le=100)
    page: int = Field(1, gt=0, le=10000)
