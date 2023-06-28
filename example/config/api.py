from ninja import NinjaAPI

from example.api import router as example_router

api = NinjaAPI()
api.add_router("/coins/", example_router)
