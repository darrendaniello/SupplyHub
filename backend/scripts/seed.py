from datetime import date, datetime, timedelta
from decimal import Decimal

from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine
from app.models import (
    Address,
    Business,
    Category,
    Favorite,
    Order,
    OrderItem,
    Product,
    ProductInventory,
    SalesHistory,
    SearchLog,
    User,
    Review,
)


# ============================================================
# CONFIG
# ============================================================

SUPPLIER_PASSWORD = "password123"
BUYER_PASSWORD = "password123"


# ============================================================
# USERS
# ============================================================

def seed_users(session: Session):
    users_data = [
        {
            "email": "buyer1@supplyhub.test",
            "password_hash": BUYER_PASSWORD,
            "full_name": "Andi Pratama",
            "role": "BUYER",
        },
        {
            "email": "buyer2@supplyhub.test",
            "password_hash": BUYER_PASSWORD,
            "full_name": "Budi Santoso",
            "role": "BUYER",
        },
        {
            "email": "buyer3@supplyhub.test",
            "password_hash": BUYER_PASSWORD,
            "full_name": "Citra Lestari",
            "role": "BUYER",
        },
        {
            "email": "buyer4@supplyhub.test",
            "password_hash": BUYER_PASSWORD,
            "full_name": "Dimas Saputra",
            "role": "BUYER",
        },
        {
            "email": "buyer5@supplyhub.test",
            "password_hash": BUYER_PASSWORD,
            "full_name": "Eka Putri",
            "role": "BUYER",
        },
        {
            "email": "supplier1@supplyhub.test",
            "password_hash": SUPPLIER_PASSWORD,
            "full_name": "Fajar Wijaya",
            "role": "SUPPLIER",
        },
        {
            "email": "supplier2@supplyhub.test",
            "password_hash": SUPPLIER_PASSWORD,
            "full_name": "Gilang Ramadhan",
            "role": "SUPPLIER",
        },
        {
            "email": "supplier3@supplyhub.test",
            "password_hash": SUPPLIER_PASSWORD,
            "full_name": "Hendra Kurniawan",
            "role": "SUPPLIER",
        },
        {
            "email": "supplier4@supplyhub.test",
            "password_hash": SUPPLIER_PASSWORD,
            "full_name": "Indra Gunawan",
            "role": "SUPPLIER",
        },
        {
            "email": "supplier5@supplyhub.test",
            "password_hash": SUPPLIER_PASSWORD,
            "full_name": "Joko Susanto",
            "role": "SUPPLIER",
        },
        {
            "email": "admin@supplyhub.test",
            "password_hash": "admin123",
            "full_name": "SupplyHub Admin",
            "role": "ADMIN",
        },
    ]

    users = {}

    for data in users_data:
        user = session.scalar(
            select(User).where(User.email == data["email"])
        )

        if not user:
            user = User(**data)
            session.add(user)
            session.flush()

        users[data["email"]] = user

    return users


# ============================================================
# BUSINESSES
# ============================================================

def seed_businesses(session: Session, users):
    businesses_data = [
        {
            "owner_email": "supplier1@supplyhub.test",
            "business_name": "Jakarta Agro Supply",
            "business_type": "Supplier",
            "description": "Supplier bahan baku pangan dan kebutuhan usaha.",
            "phone": "081200000001",
        },
        {
            "owner_email": "supplier2@supplyhub.test",
            "business_name": "Nusantara Raw Materials",
            "business_type": "Supplier",
            "description": "Penyedia bahan baku grosir untuk UMKM dan restoran.",
            "phone": "081200000002",
        },
        {
            "owner_email": "supplier3@supplyhub.test",
            "business_name": "Berkah Pangan Mandiri",
            "business_type": "Supplier",
            "description": "Distributor bahan pangan dan kebutuhan dapur usaha.",
            "phone": "081200000003",
        },
        {
            "owner_email": "supplier4@supplyhub.test",
            "business_name": "Sentra Bahan Usaha",
            "business_type": "Supplier",
            "description": "Supplier bahan baku untuk bisnis kuliner dan retail.",
            "phone": "081200000004",
        },
        {
            "owner_email": "supplier5@supplyhub.test",
            "business_name": "Prima Commodity Hub",
            "business_type": "Supplier",
            "description": "Penyedia komoditas dan bahan baku dalam jumlah besar.",
            "phone": "081200000005",
        },
    ]

    businesses = {}

    for data in businesses_data:
        owner = users[data["owner_email"]]

        business = session.scalar(
            select(Business).where(
                Business.owner_id == owner.id
            )
        )

        if not business:
            business = Business(
                owner_id=owner.id,
                business_name=data["business_name"],
                business_type=data["business_type"],
                description=data["description"],
                phone=data["phone"],
            )
            session.add(business)
            session.flush()

        businesses[data["business_name"]] = business

    return businesses


# ============================================================
# ADDRESSES
# ============================================================

def seed_addresses(session: Session, businesses):
    addresses_data = [
        {
            "business_name": "Jakarta Agro Supply",
            "address_line": "Jl. Gajah Mada No. 12",
            "city": "Jakarta Pusat",
            "province": "DKI Jakarta",
            "postal_code": "10130",
            "latitude": -6.1667,
            "longitude": 106.8167,
        },
        {
            "business_name": "Nusantara Raw Materials",
            "address_line": "Jl. Kebon Jeruk Raya No. 20",
            "city": "Jakarta Barat",
            "province": "DKI Jakarta",
            "postal_code": "11530",
            "latitude": -6.1920,
            "longitude": 106.7660,
        },
        {
            "business_name": "Berkah Pangan Mandiri",
            "address_line": "Jl. Matraman Raya No. 45",
            "city": "Jakarta Timur",
            "province": "DKI Jakarta",
            "postal_code": "13150",
            "latitude": -6.2030,
            "longitude": 106.8650,
        },
        {
            "business_name": "Sentra Bahan Usaha",
            "address_line": "Jl. Fatmawati Raya No. 88",
            "city": "Jakarta Selatan",
            "province": "DKI Jakarta",
            "postal_code": "12420",
            "latitude": -6.2930,
            "longitude": 106.7980,
        },
        {
            "business_name": "Prima Commodity Hub",
            "address_line": "Jl. Yos Sudarso No. 31",
            "city": "Jakarta Utara",
            "province": "DKI Jakarta",
            "postal_code": "14350",
            "latitude": -6.1380,
            "longitude": 106.8850,
        },
    ]

    for data in addresses_data:
        business = businesses[data["business_name"]]

        address = session.scalar(
            select(Address).where(
                Address.business_id == business.id
            )
        )

        if not address:
            address = Address(
                business_id=business.id,
                address_line=data["address_line"],
                city=data["city"],
                province=data["province"],
                postal_code=data["postal_code"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                geom=from_shape(
                    Point(
                        data["longitude"],
                        data["latitude"],
                    ),
                    srid=4326,
                ),
            )

            session.add(address)


# ============================================================
# CATEGORIES
# ============================================================

def seed_categories(session: Session):
    categories_data = [
        ("Beras & Grain", "Beras dan produk berbahan dasar grain."),
        ("Tepung", "Berbagai jenis tepung untuk kebutuhan produksi."),
        ("Gula & Pemanis", "Gula dan bahan pemanis."),
        ("Minyak & Lemak", "Minyak goreng dan bahan lemak."),
        ("Bumbu", "Bumbu dan bahan penyedap."),
        ("Protein", "Daging, ayam, telur, dan bahan protein."),
        ("Sayuran", "Sayuran segar untuk kebutuhan usaha."),
        ("Kemasan", "Kemasan dan perlengkapan packaging."),
    ]

    categories = {}

    for name, description in categories_data:
        category = session.scalar(
            select(Category).where(Category.name == name)
        )

        if not category:
            category = Category(
                name=name,
                description=description,
            )
            session.add(category)
            session.flush()

        categories[name] = category

    return categories


# ============================================================
# PRODUCTS
# ============================================================

def seed_products(session: Session, businesses, categories):
    products_data = [
        {
            "business": "Jakarta Agro Supply",
            "category": "Beras & Grain",
            "name": "Beras Premium 25kg",
            "description": "Beras premium untuk kebutuhan restoran dan catering.",
            "unit": "kg",
            "minimum_order": 25,
            "cost_price": 320000,
            "selling_price": 350000,
        },
        {
            "business": "Jakarta Agro Supply",
            "category": "Tepung",
            "name": "Tepung Terigu 25kg",
            "description": "Tepung terigu protein sedang untuk kebutuhan produksi.",
            "unit": "kg",
            "minimum_order": 25,
            "cost_price": 220000,
            "selling_price": 245000,
        },
        {
            "business": "Jakarta Agro Supply",
            "category": "Gula & Pemanis",
            "name": "Gula Pasir 25kg",
            "description": "Gula pasir kemasan grosir.",
            "unit": "kg",
            "minimum_order": 25,
            "cost_price": 360000,
            "selling_price": 390000,
        },
        {
            "business": "Jakarta Agro Supply",
            "category": "Minyak & Lemak",
            "name": "Minyak Goreng 20L",
            "description": "Minyak goreng untuk kebutuhan dapur usaha.",
            "unit": "liter",
            "minimum_order": 20,
            "cost_price": 310000,
            "selling_price": 340000,
        },
        {
            "business": "Nusantara Raw Materials",
            "category": "Beras & Grain",
            "name": "Beras Medium 25kg",
            "description": "Beras medium untuk kebutuhan restoran dan warung.",
            "unit": "kg",
            "minimum_order": 25,
            "cost_price": 295000,
            "selling_price": 325000,
        },
        {
            "business": "Nusantara Raw Materials",
            "category": "Tepung",
            "name": "Tepung Tapioka 25kg",
            "description": "Tepung tapioka untuk kebutuhan produksi makanan.",
            "unit": "kg",
            "minimum_order": 25,
            "cost_price": 185000,
            "selling_price": 210000,
        },
        {
            "business": "Nusantara Raw Materials",
            "category": "Gula & Pemanis",
            "name": "Gula Halus 10kg",
            "description": "Gula halus untuk bakery dan produksi makanan.",
            "unit": "kg",
            "minimum_order": 10,
            "cost_price": 150000,
            "selling_price": 175000,
        },
        {
            "business": "Nusantara Raw Materials",
            "category": "Bumbu",
            "name": "Lada Bubuk 5kg",
            "description": "Lada bubuk untuk kebutuhan produksi.",
            "unit": "kg",
            "minimum_order": 5,
            "cost_price": 180000,
            "selling_price": 210000,
        },
        {
            "business": "Berkah Pangan Mandiri",
            "category": "Protein",
            "name": "Telur Ayam 30kg",
            "description": "Telur ayam untuk restoran, bakery, dan catering.",
            "unit": "kg",
            "minimum_order": 10,
            "cost_price": 600000,
            "selling_price": 650000,
        },
        {
            "business": "Berkah Pangan Mandiri",
            "category": "Protein",
            "name": "Daging Ayam 20kg",
            "description": "Daging ayam segar untuk kebutuhan usaha.",
            "unit": "kg",
            "minimum_order": 10,
            "cost_price": 620000,
            "selling_price": 680000,
        },
        {
            "business": "Berkah Pangan Mandiri",
            "category": "Sayuran",
            "name": "Kentang 25kg",
            "description": "Kentang segar untuk restoran dan katering.",
            "unit": "kg",
            "minimum_order": 10,
            "cost_price": 250000,
            "selling_price": 290000,
        },
        {
            "business": "Berkah Pangan Mandiri",
            "category": "Sayuran",
            "name": "Bawang Merah 10kg",
            "description": "Bawang merah segar untuk kebutuhan dapur.",
            "unit": "kg",
            "minimum_order": 5,
            "cost_price": 280000,
            "selling_price": 320000,
        },
        {
            "business": "Sentra Bahan Usaha",
            "category": "Beras & Grain",
            "name": "Beras Premium 50kg",
            "description": "Beras premium dalam kemasan grosir.",
            "unit": "kg",
            "minimum_order": 50,
            "cost_price": 630000,
            "selling_price": 690000,
        },
        {
            "business": "Sentra Bahan Usaha",
            "category": "Tepung",
            "name": "Tepung Roti 10kg",
            "description": "Tepung roti untuk kebutuhan bakery.",
            "unit": "kg",
            "minimum_order": 10,
            "cost_price": 130000,
            "selling_price": 155000,
        },
        {
            "business": "Sentra Bahan Usaha",
            "category": "Minyak & Lemak",
            "name": "Margarin 15kg",
            "description": "Margarin untuk kebutuhan bakery dan produksi makanan.",
            "unit": "kg",
            "minimum_order": 10,
            "cost_price": 210000,
            "selling_price": 240000,
        },
        {
            "business": "Sentra Bahan Usaha",
            "category": "Kemasan",
            "name": "Food Container 500ml",
            "description": "Kemasan makanan ukuran 500ml.",
            "unit": "pcs",
            "minimum_order": 100,
            "cost_price": 75000,
            "selling_price": 95000,
        },
        {
            "business": "Prima Commodity Hub",
            "category": "Beras & Grain",
            "name": "Beras Medium 50kg",
            "description": "Beras medium untuk kebutuhan usaha skala besar.",
            "unit": "kg",
            "minimum_order": 50,
            "cost_price": 570000,
            "selling_price": 620000,
        },
        {
            "business": "Prima Commodity Hub",
            "category": "Gula & Pemanis",
            "name": "Gula Pasir 50kg",
            "description": "Gula pasir grosir untuk kebutuhan produksi.",
            "unit": "kg",
            "minimum_order": 50,
            "cost_price": 700000,
            "selling_price": 750000,
        },
        {
            "business": "Prima Commodity Hub",
            "category": "Bumbu",
            "name": "Bawang Putih 20kg",
            "description": "Bawang putih untuk kebutuhan dapur usaha.",
            "unit": "kg",
            "minimum_order": 10,
            "cost_price": 520000,
            "selling_price": 580000,
        },
        {
            "business": "Prima Commodity Hub",
            "category": "Kemasan",
            "name": "Paper Bowl 500ml",
            "description": "Paper bowl untuk makanan siap saji.",
            "unit": "pcs",
            "minimum_order": 100,
            "cost_price": 85000,
            "selling_price": 105000,
        },
    ]

    products = {}

    for data in products_data:
        business = businesses[data["business"]]
        category = categories[data["category"]]

        product = session.scalar(
            select(Product).where(
                Product.business_id == business.id,
                Product.name == data["name"],
            )
        )

        if not product:
            product = Product(
                business_id=business.id,
                category_id=category.id,
                name=data["name"],
                description=data["description"],
                unit=data["unit"],
                minimum_order=data["minimum_order"],
                cost_price=Decimal(str(data["cost_price"])),
                selling_price=Decimal(str(data["selling_price"])),
                status="AVAILABLE",
            )

            session.add(product)
            session.flush()

        products[data["name"]] = product

    return products


# ============================================================
# INVENTORY
# ============================================================

def seed_inventory(session: Session, products):
    stock_values = [
        500,
        350,
        400,
        250,
        450,
        300,
        180,
        100,
        200,
        180,
        250,
        120,
        300,
        180,
        220,
        1000,
        350,
        400,
        250,
        1000,
    ]

    for (product_name, product), stock in zip(
        products.items(),
        stock_values,
    ):
        inventory = session.scalar(
            select(ProductInventory).where(
                ProductInventory.product_id == product.id
            )
        )

        if not inventory:
            inventory = ProductInventory(
                product_id=product.id,
                stock_quantity=stock,
                reserved_quantity=0,
            )
            session.add(inventory)


# ============================================================
# ORDERS
# ============================================================

def seed_orders(session: Session, users, businesses, products):
    buyer = users["buyer1@supplyhub.test"]

    orders_data = [
        {
            "business": "Jakarta Agro Supply",
            "status": "COMPLETED",
            "products": [
                ("Beras Premium 25kg", 50),
                ("Gula Pasir 25kg", 25),
            ],
        },
        {
            "business": "Nusantara Raw Materials",
            "status": "COMPLETED",
            "products": [
                ("Beras Medium 25kg", 50),
                ("Tepung Tapioka 25kg", 25),
            ],
        },
        {
            "business": "Berkah Pangan Mandiri",
            "status": "COMPLETED",
            "products": [
                ("Telur Ayam 30kg", 20),
                ("Kentang 25kg", 20),
            ],
        },
        {
            "business": "Sentra Bahan Usaha",
            "status": "PENDING",
            "products": [
                ("Food Container 500ml", 200),
            ],
        },
    ]

    orders = []

    for data in orders_data:
        business = businesses[data["business"]]

        order = Order(
            buyer_id=buyer.id,
            supplier_business_id=business.id,
            status=data["status"],
            total_amount=Decimal("0"),
        )

        session.add(order)
        session.flush()

        total = Decimal("0")

        for product_name, quantity in data["products"]:
            product = products[product_name]

            subtotal = product.selling_price * quantity

            item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=product.selling_price,
                subtotal=subtotal,
            )

            session.add(item)

            total += subtotal

        order.total_amount = total

        orders.append(order)

    return orders


# ============================================================
# FAVORITES
# ============================================================

def seed_favorites(session: Session, users, products):
    favorites_data = [
        ("buyer1@supplyhub.test", "Beras Premium 25kg"),
        ("buyer1@supplyhub.test", "Beras Medium 25kg"),
        ("buyer1@supplyhub.test", "Telur Ayam 30kg"),
        ("buyer2@supplyhub.test", "Tepung Terigu 25kg"),
        ("buyer2@supplyhub.test", "Gula Pasir 25kg"),
        ("buyer3@supplyhub.test", "Daging Ayam 20kg"),
        ("buyer3@supplyhub.test", "Kentang 25kg"),
        ("buyer4@supplyhub.test", "Food Container 500ml"),
        ("buyer5@supplyhub.test", "Beras Medium 50kg"),
    ]

    for email, product_name in favorites_data:
        user = users[email]
        product = products[product_name]

        favorite = session.scalar(
            select(Favorite).where(
                Favorite.user_id == user.id,
                Favorite.product_id == product.id,
            )
        )

        if not favorite:
            session.add(
                Favorite(
                    user_id=user.id,
                    product_id=product.id,
                )
            )


# ============================================================
# SALES HISTORY
# ============================================================

def seed_sales_history(session: Session, products):
    today = date.today()

    for product_name, product in products.items():
        base_quantity = 10 + (product.id % 8)

        for days_ago in range(30, 0, -1):
            sales_date = today - timedelta(days=days_ago)

            existing = session.scalar(
                select(SalesHistory).where(
                    SalesHistory.product_id == product.id,
                    SalesHistory.sales_date == sales_date,
                )
            )

            if not existing:
                variation = (days_ago + product.id) % 7 - 3
                quantity = max(0, base_quantity + variation)

                session.add(
                    SalesHistory(
                        product_id=product.id,
                        quantity_sold=quantity,
                        sales_date=sales_date,
                    )
                )


# ============================================================
# SEARCH LOGS
# ============================================================

def seed_search_logs(session: Session, users):
    searches = [
        (
            "buyer1@supplyhub.test",
            "beras 25kg",
            "beras 25kg",
        ),
        (
            "buyer1@supplyhub.test",
            "supplier beras dekat jakarta pusat",
            "beras + supplier + Jakarta Pusat",
        ),
        (
            "buyer2@supplyhub.test",
            "tepung untuk bakery",
            "tepung + bakery",
        ),
        (
            "buyer2@supplyhub.test",
            "gula grosir murah",
            "gula + grosir + murah",
        ),
        (
            "buyer3@supplyhub.test",
            "telur 20kg",
            "telur + 20kg",
        ),
        (
            "buyer3@supplyhub.test",
            "supplier kentang terdekat",
            "kentang + supplier + nearby",
        ),
        (
            "buyer4@supplyhub.test",
            "kemasan makanan 500ml",
            "food container 500ml",
        ),
        (
            "buyer5@supplyhub.test",
            "beras murah",
            "beras + harga murah",
        ),
    ]

    for email, query, interpreted_query in searches:
        user = users[email]

        existing = session.scalar(
            select(SearchLog).where(
                SearchLog.user_id == user.id,
                SearchLog.query == query,
            )
        )

        if not existing:
            session.add(
                SearchLog(
                    user_id=user.id,
                    query=query,
                    interpreted_query=interpreted_query,
                )
            )

# ============================================================
# REVIEWS
# ============================================================

def seed_reviews(session: Session, users, products):
    reviews_data = [
        {
            "email": "buyer1@supplyhub.test",
            "product": "Beras Premium 25kg",
            "rating": 5,
            "comment": "Kualitas beras sangat bagus dan sesuai dengan deskripsi.",
        },
        {
            "email": "buyer2@supplyhub.test",
            "product": "Beras Premium 25kg",
            "rating": 4,
            "comment": "Kualitas bagus dan pengiriman cukup cepat.",
        },
        {
            "email": "buyer3@supplyhub.test",
            "product": "Beras Premium 25kg",
            "rating": 5,
            "comment": "Beras cocok untuk kebutuhan restoran.",
        },
        {
            "email": "buyer4@supplyhub.test",
            "product": "Beras Premium 25kg",
            "rating": 4,
            "comment": "Produk bagus dan kemasannya aman.",
        },
        {
            "email": "buyer5@supplyhub.test",
            "product": "Beras Premium 25kg",
            "rating": 5,
            "comment": "Sangat puas dengan kualitas produknya.",
        },

        {
            "email": "buyer1@supplyhub.test",
            "product": "Tepung Terigu 25kg",
            "rating": 5,
            "comment": "Tepung bagus untuk kebutuhan produksi.",
        },
        {
            "email": "buyer3@supplyhub.test",
            "product": "Tepung Terigu 25kg",
            "rating": 4,
            "comment": "Kualitas sesuai dengan harga.",
        },
        {
            "email": "buyer5@supplyhub.test",
            "product": "Tepung Terigu 25kg",
            "rating": 5,
            "comment": "Cocok untuk kebutuhan bakery.",
        },

        {
            "email": "buyer1@supplyhub.test",
            "product": "Beras Medium 25kg",
            "rating": 4,
            "comment": "Kualitas cukup baik untuk kebutuhan usaha.",
        },
        {
            "email": "buyer2@supplyhub.test",
            "product": "Beras Medium 25kg",
            "rating": 5,
            "comment": "Harga dan kualitas sangat seimbang.",
        },
        {
            "email": "buyer4@supplyhub.test",
            "product": "Beras Medium 25kg",
            "rating": 4,
            "comment": "Produk sesuai pesanan.",
        },

        {
            "email": "buyer2@supplyhub.test",
            "product": "Telur Ayam 30kg",
            "rating": 5,
            "comment": "Telur segar dan kualitasnya bagus.",
        },
        {
            "email": "buyer3@supplyhub.test",
            "product": "Telur Ayam 30kg",
            "rating": 5,
            "comment": "Sangat cocok untuk kebutuhan catering.",
        },
        {
            "email": "buyer5@supplyhub.test",
            "product": "Telur Ayam 30kg",
            "rating": 4,
            "comment": "Kualitas bagus dan pengiriman aman.",
        },

        {
            "email": "buyer1@supplyhub.test",
            "product": "Food Container 500ml",
            "rating": 5,
            "comment": "Kemasan kuat dan cocok untuk usaha makanan.",
        },
        {
            "email": "buyer4@supplyhub.test",
            "product": "Food Container 500ml",
            "rating": 4,
            "comment": "Kualitas cukup bagus untuk kebutuhan packaging.",
        },
    ]

    for data in reviews_data:
        user = users[data["email"]]
        product = products[data["product"]]

        existing = session.scalar(
            select(Review).where(
                Review.user_id == user.id,
                Review.product_id == product.id,
            )
        )

        if not existing:
            session.add(
                Review(
                    user_id=user.id,
                    product_id=product.id,
                    rating=data["rating"],
                    comment=data["comment"],
                )
            )


# ============================================================
# MAIN
# ============================================================

def seed_database():
    print("Starting SupplyHub database seed...")

    with Session(engine) as session:
        try:
            users = seed_users(session)
            session.flush()

            businesses = seed_businesses(session, users)
            session.flush()

            seed_addresses(session, businesses)
            session.flush()

            categories = seed_categories(session)
            session.flush()

            products = seed_products(
                session,
                businesses,
                categories,
            )
            session.flush()

            seed_inventory(session, products)
            session.flush()

            seed_orders(
                session,
                users,
                businesses,
                products,
            )
            session.flush()

            seed_favorites(
                session,
                users,
                products,
            )

            seed_reviews(
                session,
                users,
                products,
            )

            seed_sales_history(
                session,
                products,
            )

            seed_search_logs(
                session,
                users,
            )

            session.commit()

            print("SupplyHub database seed completed successfully!")

        except Exception:
            session.rollback()
            raise


if __name__ == "__main__":
    seed_database()