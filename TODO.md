## Task: Fix auth gateway 503 and Google login 404

- [ ] Fix Google OAuth 404 by wiring `social_django.urls` in `auth_service/auth_service/urls.py` under `/auth/`.
- [ ] Improve gateway `/auth/login` error clarity in `gateway/routers/auth.py` when `AUTH_SERVICE_URL` is unreachable.
- [ ] Verification: confirm auth_service `/api/login` reachable through gateway and confirm Google login endpoint responds (no 404).
