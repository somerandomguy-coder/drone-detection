# PLACEHOLDER ONLY
# import asyncio
# from datetime import datetime
#
# from database import initialize_database, save_prediction
#
#
# async def main():
#     print("init database")
#     now = datetime.now()
#     await initialize_database()
#     process_time = datetime.now() - now
#     print(f"finish init database, latency is: {process_time}")
#
#     print("test save prediction")
#     id = "meme"
#     filepath = "run/asdasd.png"
#     result = "0 0.5 0.3 0.2 0.5"
#
#     await save_prediction(id, filepath, result)
#
#     print("finish test save prediction")
#
#
# asyncio.run(main())
