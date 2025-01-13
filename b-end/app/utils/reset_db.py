from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from decouple import config

async def reset_db():
    try:
        # Mengambil konfigurasi dari .env
        MONGODB_URL = config("MONGODB_URL")
        DATABASE_NAME = config("DATABASE_NAME")
        
        print(f"Menghubungkan ke database {DATABASE_NAME}...")
        client = AsyncIOMotorClient(MONGODB_URL)
        
        # Test koneksi
        await client.admin.command('ping')
        print("Berhasil terhubung ke MongoDB.")
        
        # Drop database
        await client.drop_database(DATABASE_NAME)
        print(f"Database {DATABASE_NAME} berhasil direset!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client.close()
        print("Koneksi database ditutup.")

if __name__ == "__main__":
    asyncio.run(reset_db()) 