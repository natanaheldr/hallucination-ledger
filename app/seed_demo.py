from app.database import SessionLocal, Base, engine
from app.models import Claim, ClaimAudit, ResponseSource
from datetime import datetime, timezone, timedelta


DEMO_DATA = [
    {
        "model_name": "GPT-4o",
        "prompt": "Tell me about the history of the Eiffel Tower",
        "raw_text": (
            "The Eiffel Tower was completed in 1889 for the World's Fair. "
            "It stands 330 meters tall and was the tallest structure in the world until 1930. "
            "Gustave Eiffel also designed the Statue of Liberty's internal framework. "
            "Over 7 million people visit the tower each year, making it the most visited paid monument in the world. "
            "The tower was originally intended to be dismantled after 20 years."
        ),
        "claims": [
            ("The Eiffel Tower was completed in 1889 for the World's Fair.", "verified"),
            ("It stands 330 meters tall and was the tallest structure in the world until 1930.", "verified"),
            ("Gustave Eiffel also designed the Statue of Liberty's internal framework.", "verified"),
            ("Over 7 million people visit the tower each year.", "doubtful"),
            ("The tower was originally intended to be dismantled after 20 years.", "verified"),
        ],
    },
    {
        "model_name": "Claude 3.5 Sonnet",
        "prompt": "What are the health benefits of drinking coffee?",
        "raw_text": (
            "Coffee consumption has been linked to a reduced risk of type 2 diabetes according to a 2023 meta-analysis. "
            "Regular coffee drinkers have a 30% lower chance of developing Parkinson's disease. "
            "Drinking coffee can increase lifespan by up to 10 years according to recent studies. "
            "Coffee contains more antioxidants than both fruits and vegetables combined. "
            "The FDA recommends limiting caffeine intake to 400mg per day for healthy adults."
        ),
        "claims": [
            ("Coffee consumption reduces the risk of type 2 diabetes according to a 2023 meta-analysis.", "verified"),
            ("Regular coffee drinkers have a 30% lower chance of developing Parkinson's disease.", "verified"),
            ("Drinking coffee can increase lifespan by up to 10 years according to recent studies.", "false"),
            ("Coffee contains more antioxidants than both fruits and vegetables combined.", "false"),
            ("The FDA recommends limiting caffeine intake to 400mg per day for healthy adults.", "verified"),
        ],
    },
    {
        "model_name": "Gemini 1.5 Pro",
        "prompt": "Explain quantum computing in simple terms",
        "raw_text": (
            "The first quantum computer was built by IBM in 1998 with just 2 qubits. "
            "In 2019, Google announced quantum supremacy with a 53-qubit processor named Sycamore. "
            "Quantum computers operate at temperatures near absolute zero, around -273 degrees Celsius. "
            "By 2025, quantum computers will replace all classical computers according to industry experts. "
            "China has invested over $15 billion in quantum computing research as of 2023."
        ),
        "claims": [
            ("The first quantum computer was built by IBM in 1998 with just 2 qubits.", "verified"),
            ("In 2019, Google announced quantum supremacy with a 53-qubit processor.", "verified"),
            ("Quantum computers operate at temperatures near absolute zero, around -273 degrees Celsius.", "verified"),
            ("By 2025, quantum computers will replace all classical computers according to industry experts.", "false"),
            ("China has invested over $15 billion in quantum computing research as of 2023.", "doubtful"),
        ],
    },
    {
        "model_name": "GPT-4o",
        "prompt": "What are the biggest companies by market cap?",
        "raw_text": (
            "Apple became the first company to reach a $3 trillion market cap in January 2022. "
            "Microsoft's market cap surpassed $3 trillion in 2024, driven by AI investments. "
            "NVIDIA's valuation grew by over 200% in 2023 alone, reaching $1 trillion. "
            "Saudi Aramco was the most valuable company in the world in 2020 at $2 trillion. "
            "By 2030, Tesla will have a market cap of $10 trillion according to Elon Musk."
        ),
        "claims": [
            ("Apple became the first company to reach a $3 trillion market cap in January 2022.", "verified"),
            ("Microsoft's market cap surpassed $3 trillion in 2024, driven by AI investments.", "verified"),
            ("NVIDIA's valuation grew by over 200% in 2023 alone, reaching $1 trillion.", "verified"),
            ("Saudi Aramco was the most valuable company in the world in 2020 at $2 trillion.", "doubtful"),
            ("By 2030, Tesla will have a market cap of $10 trillion according to Elon Musk.", "false"),
        ],
    },
    {
        "model_name": "Claude 3 Opus",
        "prompt": "Tell me about the Apollo 11 mission",
        "raw_text": (
            "Apollo 11 launched on July 16, 1969 from Kennedy Space Center in Florida. "
            "Neil Armstrong became the first human to walk on the Moon on July 20, 1969. "
            "The mission carried three astronauts: Neil Armstrong, Buzz Aldrin, and Michael Collins. "
            "The Saturn V rocket that launched Apollo 11 remains the most powerful rocket ever built. "
            "Only 10 people have walked on the Moon since the Apollo program ended in 1972."
        ),
        "claims": [
            ("Apollo 11 launched on July 16, 1969 from Kennedy Space Center in Florida.", "verified"),
            ("Neil Armstrong became the first human to walk on the Moon on July 20, 1969.", "verified"),
            ("The mission carried three astronauts: Neil Armstrong, Buzz Aldrin, and Michael Collins.", "verified"),
            ("The Saturn V rocket remains the most powerful rocket ever built.", "verified"),
            ("Only 10 people have walked on the Moon since the Apollo program ended in 1972.", "false"),
        ],
    },
]


def seed_demo_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    existing = db.query(ResponseSource).count()
    if existing > 0:
        db.close()
        return {"seeded": False, "message": f"Database already has {existing} sources. Demo data not inserted."}

    now = datetime.now(timezone.utc)
    total_claims = 0

    for i, entry in enumerate(DEMO_DATA):
        days_ago = len(DEMO_DATA) - i
        created = now - timedelta(days=days_ago, hours=i * 3)

        source = ResponseSource(
            model_name=entry["model_name"],
            prompt=entry["prompt"],
            raw_text=entry["raw_text"],
            created_at=created,
        )
        db.add(source)
        db.flush()

        for j, (text, status) in enumerate(entry["claims"]):
            claim = Claim(
                source_id=source.id,
                claim_text=text,
                status=status,
                created_at=created + timedelta(minutes=j),
                updated_at=created + timedelta(minutes=j),
            )
            db.add(claim)
            db.flush()

            if status != "unreviewed":
                audit = ClaimAudit(
                    claim_id=claim.id,
                    old_status="unreviewed",
                    new_status=status,
                    changed_at=created + timedelta(minutes=j + 1),
                )
                db.add(audit)

            total_claims += 1

        source.claim_count = len(entry["claims"])
        source.verified_count = sum(1 for _, s in entry["claims"] if s == "verified")
        source.false_count = sum(1 for _, s in entry["claims"] if s == "false")

    db.commit()
    db.close()

    return {"seeded": True, "sources": len(DEMO_DATA), "claims": total_claims}


if __name__ == "__main__":
    result = seed_demo_data()
    print(result)
