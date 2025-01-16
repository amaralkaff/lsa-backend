from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from decouple import config
from datetime import datetime
from app.core.security import get_password_hash


async def seed_all():
    client = None
    try:
        # Ambil konfigurasi dan bersihkan dari komentar
        MONGODB_URL = config("MONGODB_URL").split('#')[
            0].strip()  # type: ignore
        DATABASE_NAME = config("MONGODB_DATABASE").split('#')[
            0].strip()  # type: ignore

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
            "email": "amangly@gmail.com",
            "username": "amangly",
            "full_name": "amangly palepale",
            "password": get_password_hash("amangly123"),
            "is_admin": True,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        await db.users.insert_one(admin_data)
        print("Admin berhasil dibuat!")

        # Blogs
        blogs = [
            {
                "title": "Dampaknya Terhadap Stabilitas Global",
                "content": "Ketegangan di Laut China Selatan semakin meningkat seiring perebutan klaim wilayah dan sumber daya alam di kawasan tersebut. Konflik ini melibatkan berbagai negara besar seperti China, Filipina, Vietnam, dan Amerika Serikat...",
                "image": "/static/uploads/gallery1.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            },
            {
                "title": "Dampaknya Terhadap Stabilitas Global",
                "content": "Ketegangan di Laut China Selatan semakin meningkat seiring perebutan klaim wilayah dan sumber daya alam di kawasan tersebut. Konflik ini melibatkan berbagai negara besar seperti China, Filipina, Vietnam, dan Amerika Serikat...",
                "image": "/static/uploads/gallery2.jpg",
                "author": admin_data["email"],
                "created_at": datetime.utcnow()
            }
            # ... tambahkan blog lainnya sesuai data frontend
        ]
        await db.blogs.insert_many(blogs)
        print(f"{len(blogs)} blog berhasil dibuat!")

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
                "subtitle": "Pengenalan Data Science untuk Pemula",
                "description": "Workshop pengenalan data science dengan materi dasar-dasar pengolahan data, visualisasi, dan machine learning",
                "image": "/static/uploads/program1.jpg",
                "created_at": datetime.utcnow()
            },
            {
                "title": "Seminar Artificial Intelligence",
                "subtitle": "Memahami Dampak AI dalam Kehidupan Sehari-hari",
                "description": "Seminar yang membahas tentang perkembangan AI dan dampaknya terhadap berbagai aspek kehidupan",
                "image": "/static/uploads/program2.jpg",
                "created_at": datetime.utcnow()
            },
            {
                "title": "Pelatihan Machine Learning",
                "subtitle": "Implementasi ML untuk Pemecahan Masalah",
                "description": "Pelatihan intensif tentang implementasi machine learning dalam menyelesaikan berbagai kasus nyata",
                "image": "/static/uploads/program3.jpg",
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

if __name__ == "__main__":
    asyncio.run(seed_all())
