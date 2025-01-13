from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from decouple import config
from datetime import datetime
import bcrypt
from passlib.hash import bcrypt as passlib_bcrypt
from app.core.database import get_database

async def seed_all():
    client = None
    try:
        # Ambil konfigurasi dan bersihkan dari komentar
        MONGODB_URL = config("MONGODB_URL").split('#')[0].strip() # type: ignore
        DATABASE_NAME = config("MONGODB_DATABASE").split('#')[0].strip() # type: ignore
        
        print(f"Database name: '{DATABASE_NAME}'")  # Debug line dengan quotes
        
        # Buat koneksi dengan timeout yang lebih lama
        print("Menghubungkan ke database...")
        client = AsyncIOMotorClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=30000,
            maxIdleTimeMS=30000
        )
        
        # Test koneksi
        await client.admin.command('ping')
        print("Berhasil terhubung ke MongoDB.")
        
        # Reset database
        await client.drop_database(DATABASE_NAME)
        print(f"Database {DATABASE_NAME} berhasil direset!")
        
        # Seed semua data dengan koneksi yang sama
        db = client[DATABASE_NAME]
        
        # Admin
        admin_data = {
            "email": config("ADMIN_EMAIL", default="admin@example.com"),
            "username": "admin",
            "password": passlib_bcrypt.hash("admin123"),
            "is_admin": True,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        await db.users.insert_one(admin_data)
        print("Admin berhasil dibuat!")
        
        # Blogs
        blogs = [
            {
                "title": "Blog Pertama",
                "content": "Ini adalah konten blog pertama",
                "image": "/static/uploads/blog1.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            },
            {
                "title": "Blog Kedua", 
                "content": "Ini adalah konten blog kedua",
                "image": "/static/uploads/blog2.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            }
        ]
        await db.blogs.insert_many(blogs)
        print("2 blog berhasil dibuat!")
        
        # Gallery
        gallery = [
            {
                "title": "Foto Pertama",
                "description": "Deskripsi foto pertama",
                "image": "/static/uploads/gallery1.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            },
            {
                "title": "Foto Kedua",
                "description": "Deskripsi foto kedua", 
                "image": "/static/uploads/gallery2.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            }
        ]
        await db.gallery.insert_many(gallery)
        print("2 gallery berhasil dibuat!")
        
        # Partners
        partners = [
            {
                "name": "Partner Pertama",
                "description": "Deskripsi partner pertama",
                "website_url": "https://partner1.com",
                "logo": "/static/uploads/partner1.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            },
            {
                "name": "Partner Kedua",
                "description": "Deskripsi partner kedua",
                "website_url": "https://partner2.com",
                "logo": "/static/uploads/partner2.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            }
        ]
        await db.partners.insert_many(partners)
        print("2 partner berhasil dibuat!")
        
        # Programs
        programs = [
            {
                "title": "Workshop Data Science",
                "description": "Workshop pengenalan data science",
                "program_type": "workshop",
                "image": "/static/uploads/program1.jpg",
                "start_date": datetime(2024, 1, 1),
                "end_date": datetime(2024, 1, 2),
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            },
            {
                "title": "Seminar AI",
                "description": "Seminar tentang artificial intelligence",
                "program_type": "seminar",
                "image": "/static/uploads/program2.jpg", 
                "start_date": datetime(2024, 2, 1),
                "end_date": datetime(2024, 2, 2),
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            },
            {
                "title": "Pelatihan Machine Learning",
                "description": "Pelatihan dasar machine learning",
                "program_type": "training",
                "image": "/static/uploads/program3.jpg",
                "start_date": datetime(2024, 3, 1),
                "end_date": datetime(2024, 3, 2),
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            }
        ]
        await db.programs.insert_many(programs)
        print("3 program berhasil dibuat!")
        
        print("Seeding data selesai!")
        
    except Exception as e:
        print(f"Error saat seeding data: {str(e)}")
    finally:
        if client:
            client.close()
            print("Koneksi database ditutup.")

async def migrate_program_types():
    """Memigrasi program_type yang tidak valid ke nilai yang valid"""
    db = await get_database()
    
    # Mapping untuk migrasi
    type_mapping = {
        "seminar": "workshop",
        "training": "workshop"
    }
    
    # Update semua dokumen dengan program_type yang tidak valid
    for old_type, new_type in type_mapping.items():
        result = await db.programs.update_many(
            {"program_type": old_type},
            {"$set": {"program_type": new_type}}
        )
        print(f"Migrasi {old_type} ke {new_type}: {result.modified_count} dokumen diupdate")

async def run_migrations():
    """Menjalankan semua migrasi"""
    print("Menjalankan migrasi...")
    await migrate_program_types()
    print("Migrasi selesai!")

if __name__ == "__main__":
    asyncio.run(seed_all())
    asyncio.run(run_migrations()) 