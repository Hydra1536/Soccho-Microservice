from django.db.models import Sum
from django.contrib.auth import get_user_model
from friends.models import Friendship
User = get_user_model()

def calculate_loyalty_score(user: User) -> float:
    """(total_given - total_lent) / total_transactions."""
    # Mock - integrate with transaction service
    total_given = 1000
    total_lent = 800
    total_tx = 50
    return (total_given - total_lent) / total_tx if total_tx else 0.0

