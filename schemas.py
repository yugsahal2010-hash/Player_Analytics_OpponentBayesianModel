from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class PerformanceTier(str, Enum):
    POOR = "Poor"
    BELOW_AVERAGE = "Below Average"
    AVERAGE = "Average"
    STRONG = "Strong"
    ELITE = "Elite"


class MatchRecord(BaseModel):
    score: float = Field(..., ge=0)
    opponent_team: str


class OpponentPerformanceRequest(BaseModel):
    player_id: str
    player_name: str
    target_opponent: str
    recent_matches: List[MatchRecord]


class CalculationDetails(BaseModel):
    credibility_factor: float
    opponent_weight: float
    overall_weight: float
    expected_score: float
    expected_variability: float
    overall_average_score: float
    opponent_average_score: float
    matches_vs_opponent: int


class OpponentPerformanceResponse(BaseModel):
    player_id: str
    player_name: str
    opponent_team: str
    predicted_score: float
    performance_tier: PerformanceTier
    interpretation: str
    calculation_details: CalculationDetails
