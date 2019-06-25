from django.db import models

# Blacklist for access tokens
class TokenBlacklist(models.Model):    # authorization demanded for sure
    token_id = models.CharField(max_length=500, blank=False, null=False,unique=True)

    def __str__(self): return 'Token ID:' + str(self.id)
