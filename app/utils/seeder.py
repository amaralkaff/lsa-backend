from app.core.database import get_database, connect_to_mongo, close_mongo_connection
from passlib.context import CryptContext
from datetime import datetime
import asyncio
from decouple import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_admin():
    try:
        await connect_to_mongo()
        db = await get_database()
        
        # Check if admin already exists
        admin = await db.users.find_one({"email": config("ADMIN_EMAIL", default="admin@admin.com")})
        if admin:
            print("Admin already exists!")
            return
        
        # Create admin user
        admin_data = {
            "email": config("ADMIN_EMAIL", default="admin@admin.com"),
            "username": config("ADMIN_USERNAME", default="admin"),
            "password": pwd_context.hash(config("ADMIN_PASSWORD", default="admin123")),
            "is_active": True,
            "is_admin": True,
            "created_at": datetime.utcnow()
        }
        
        result = await db.users.insert_one(admin_data)
        if result.inserted_id:
            print("Admin user created successfully!")
        else:
            print("Failed to create admin user!")
    except Exception as e:
        print(f"Error creating admin: {str(e)}")
    finally:
        await close_mongo_connection()

async def seed_blog():
    try:
        await connect_to_mongo()
        db = await get_database()
        
        # Check if blog posts exist
        if await db.blogs.count_documents({}) > 0:
            print("Blog posts already exist!")
            return
        
        blog_data = [
            {
                "title": "Blog Post 1",
                "content": "Ini adalah konten blog pertama",
                "image_url": "https://example.com/image1.jpg",
                "author": "Admin",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            # Tambahkan blog post lainnya di sini
        ]
        
        result = await db.blogs.insert_many(blog_data)
        print(f"{len(result.inserted_ids)} blog posts created successfully!")
    except Exception as e:
        print(f"Error creating blog posts: {str(e)}")
    finally:
        await close_mongo_connection()
        
async def seed_gallery():
    try:
        await connect_to_mongo()
        db = await get_database()
        
        if await db.gallery.count_documents({}) > 0:
            print("Gallery items already exist!")
            return
            
        gallery_data = [
            {
                "title": "Gambar 1",
                "description": "Deskripsi gambar 1",
                "image_url": "https://example.com/gallery1.jpg",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            # Tambahkan item gallery lainnya di sini
        ]
        
        result = await db.gallery.insert_many(gallery_data)
        print(f"{len(result.inserted_ids)} gallery items created successfully!")
    except Exception as e:
        print(f"Error creating gallery items: {str(e)}")
    finally:
        await close_mongo_connection()

async def seed_partners():
    try:
        await connect_to_mongo()
        db = await get_database()
        
        if await db.partners.count_documents({}) > 0:
            print("Partners already exist!")
            return
            
        partners_data = [
            {
                "name": "Partner 1",
                "description": "Deskripsi partner 1",
                "logo_url": "https://example.com/partner1.jpg",
                "website": "https://partner1.com",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            # Tambahkan partner lainnya di sini
        ]
        
        result = await db.partners.insert_many(partners_data)
        print(f"{len(result.inserted_ids)} partners created successfully!")
    except Exception as e:
        print(f"Error creating partners: {str(e)}")
    finally:
        await close_mongo_connection()

async def seed_programs():
    try:
        await connect_to_mongo()
        db = await get_database()
        
        if await db.programs.count_documents({}) > 0:
            print("Programs already exist!")
            return
            
        programs_data = [
            {
                "title": "Program 1",
                "description": "Deskripsi program 1",
                "image_url": "https://example.com/program1.jpg",
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow(),
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            # Tambahkan program lainnya di sini
        ]
        
        result = await db.programs.insert_many(programs_data)
        print(f"{len(result.inserted_ids)} programs created successfully!")
    except Exception as e:
        print(f"Error creating programs: {str(e)}")
    finally:
        await close_mongo_connection()

async def seed_all():
    await connect_to_mongo()
    try:
        await seed_admin()
        await seed_blog()
        await seed_gallery()
        await seed_partners()
        await seed_programs()
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
    finally:
        await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(seed_all()) 