import debugpy


from core.start_app import AppBuilder
from utils.default import create_default_data
# debugpy.listen(("127.0.0.1", 5678))
# debugpy.wait_for_client()





app = AppBuilder().get_app()
@app.on_event("startup")
async def startup_event():
    create_default_data()