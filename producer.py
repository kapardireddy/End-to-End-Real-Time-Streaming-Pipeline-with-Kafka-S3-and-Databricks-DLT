from kafka import KafkaProducer
import json, time, random, uuid
from datetime import datetime
from faker import Faker

fake = Faker()
Faker.seed(42)

# Kafka configuration
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',   # Update when deployed to EC2/MSK
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    linger_ms=10
)

# Domain constants
CURRENCIES = ["USD", "EUR", "GBP","INR"]
PAYMENT_METHODS = ["credit_card", "paypal", "apple_pay", "google_pay"]
DEVICES = ["mobile", "desktop", "tablet"]

# Category-to-item mapping (10+ realistic items per category)
CATEGORY_ITEMS = {
    "food": [
        "Pizza", "Burger", "Pasta", "Sushi", "Sandwich", "Salad", "Steak",
        "Fries", "Ice Cream", "Soup", "Taco", "Hotdog"
    ],
    "electronics": [
        "Smartphone", "Laptop", "Tablet", "Headphones", "Monitor",
        "Keyboard", "Mouse", "Smartwatch", "Camera", "Bluetooth Speaker"
    ],
    "travel": [
        "Flight Ticket", "Hotel Booking", "Car Rental", "Train Pass",
        "Travel Insurance", "Luggage Bag", "Travel Adapter", "Backpack",
        "Tour Package", "Cruise Ticket"
    ],
    "fashion": [
        "T-Shirt", "Jeans", "Jacket", "Sneakers", "Dress", "Hat", "Sunglasses",
        "Watch", "Handbag", "Belt", "Scarf"
    ],
    "sports": [
        "Football", "Tennis Racket", "Basketball", "Running Shoes",
        "Gym Bag", "Yoga Mat", "Golf Club", "Helmet", "Gloves", "Water Bottle"
    ],
    "home": [
        "Vacuum Cleaner", "Lamp", "Curtains", "Cushions", "Cookware Set",
        "Microwave", "Coffee Maker", "Toaster", "Blender", "Dining Table"
    ]
}

# Fixed user pool (repeatable customers)
USER_POOL = [
    {
        "user_id": i,
        "name": fake.name(),
        "email": fake.email(),
        "country": fake.country(),
        "city": fake.city(),
        "address": fake.address(),
        "age": random.randint(18, 65),
        "payment_method": random.choice(PAYMENT_METHODS),
        "device_type": random.choice(DEVICES),
        "ip_address": fake.ipv4()
    }
    for i in range(1, 51)
]


def generate_transaction():
    """Generate a realistic transaction record with category-based items."""
    user = random.choice(USER_POOL)
    category = random.choice(list(CATEGORY_ITEMS.keys()))

    # Pick items from that category
    item_names = random.sample(CATEGORY_ITEMS[category], k=random.randint(1, 3))

    items = [
        {
            "item_id": str(uuid.uuid4()),
            "name": item_name,
            "price": round(random.uniform(10.0, 500.0), 2),
            "quantity": random.randint(1, 5)
        }
        for item_name in item_names
    ]

    # Calculate total amount accurately
    total_amount = round(sum(item["price"] * item["quantity"] for item in items), 2)

    # Construct final JSON payload
    return {
        "transaction_id": str(uuid.uuid4()),
        "user": user,
        "amount": total_amount,
        "currency": random.choice(CURRENCIES),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "category": category,
        "items": items
    }


if __name__ == "__main__":
    print("🚀 Kafka Producer started — sending data to topic 'transaction_logs'")
    try:
        while True:
            txn = generate_transaction()
            producer.send("transaction_logs", txn)
            producer.flush()

            # Print formatted JSON
            print(json.dumps(txn, indent=2))
            time.sleep(0.5)  # Produce ~2 messages/second
    except KeyboardInterrupt:
        print("\n🛑 Shutting down producer...")
        producer.close()
