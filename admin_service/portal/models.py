from django.contrib.auth.models import User as AuthUser


class UserProxy(AuthUser):
    class Meta:
        proxy = True
        verbose_name = "Soccho User"
        verbose_name_plural = "Soccho Users"

    @property
    def friend_count(self):
        # Cross-service friend graph is owned by social_service.
        return 0

    @property
    def loyalty_score(self):
        return 0.0
