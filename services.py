import math
from schemas import (
    OpponentPerformanceRequest,
    OpponentPerformanceResponse,
    CalculationDetails,
    PerformanceTier,
)
from utils import mean, std_dev


def compute_opponent_performance(payload: OpponentPerformanceRequest):

    matches = payload.recent_matches[-20:]

    all_scores = [match.score for match in matches]

    opponent_scores = [
        match.score
        for match in matches
        if match.opponent_team == payload.target_opponent
    ]

    overall_average_score = mean(all_scores)
    overall_score_std_dev = std_dev(all_scores)

    if opponent_scores:
        opponent_average_score = mean(opponent_scores)
        opponent_score_std_dev = std_dev(opponent_scores)
    else:
        opponent_average_score = overall_average_score
        opponent_score_std_dev = overall_score_std_dev

    matches_vs_opponent = len(opponent_scores)

    credibility_factor = (overall_score_std_dev / opponent_score_std_dev) ** 2

    opponent_weight = (
        matches_vs_opponent / (matches_vs_opponent + credibility_factor)
        if matches_vs_opponent > 0 else 0
    )

    overall_weight = 1 - opponent_weight

    expected_score = (
        opponent_weight * opponent_average_score
        + overall_weight * overall_average_score
    )

    expected_variability = math.sqrt(
        overall_weight * (overall_score_std_dev ** 2)
        + opponent_weight * (opponent_score_std_dev ** 2)
    )

    predicted_score = round(expected_score, 2)

    if predicted_score < 20:
        performance_tier = PerformanceTier.POOR
    elif predicted_score < 35:
        performance_tier = PerformanceTier.BELOW_AVERAGE
    elif predicted_score < 55:
        performance_tier = PerformanceTier.AVERAGE
    elif predicted_score < 80:
        performance_tier = PerformanceTier.STRONG
    else:
        performance_tier = PerformanceTier.ELITE

    interpretation = (
        f"{payload.player_name} is projected at {predicted_score} "
        f"against {payload.target_opponent}, classified as {performance_tier.value}."
    )

    return OpponentPerformanceResponse(
        player_id=payload.player_id,
        player_name=payload.player_name,
        opponent_team=payload.target_opponent,
        predicted_score=predicted_score,
        performance_tier=performance_tier,
        interpretation=interpretation,
        calculation_details=CalculationDetails(
            credibility_factor=round(credibility_factor, 4),
            opponent_weight=round(opponent_weight, 4),
            overall_weight=round(overall_weight, 4),
            expected_score=round(expected_score, 4),
            expected_variability=round(expected_variability, 4),
            overall_average_score=round(overall_average_score, 4),
            opponent_average_score=round(opponent_average_score, 4),
            matches_vs_opponent=matches_vs_opponent,
        ),
    )
