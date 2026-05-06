from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware


def build_cors_middleware(app):
    return FastAPICORSMiddleware(
        app,
        allow_origins=["https://soccho.vercel.app", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
