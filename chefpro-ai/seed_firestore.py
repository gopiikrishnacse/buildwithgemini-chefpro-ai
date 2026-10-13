"""Script to seed Firestore database with authentic Hyderabadi and Telangana recipes."""

from google.cloud import firestore

# Hardcoded project ID as string to avoid project number issues on Agent Platform
PROJECT_ID = "qwiklabs-gcp-04-48ac5222ff71"
COLLECTION_NAME = "recipes"

SEEDED_RECIPES = [
    {
        "id": "hyderabadi-dum-biryani",
        "title": "Hyderabadi Kacchi Gosht Dum Biryani",
        "cuisine": "Hyderabadi",
        "description": "Legendary royal dish made with marinated raw meat layered with fragrant basmati rice and cooked on slow dum.",
        "prep_time": "45 mins",
        "cook_time": "60 mins",
        "spice_level": "Medium-High",
        "difficulty": "Advanced",
        "ingredients": [
            "basmati rice",
            "mutton",
            "yogurt",
            "fried onions (birista)",
            "ginger garlic paste",
            "shahi jeera",
            "mint leaves",
            "coriander leaves",
            "saffron milk",
            "ghee",
            "garam masala",
            "green chillies"
        ],
        "instructions": [
            "Marinate raw mutton with yogurt, ginger-garlic paste, spices, fried onions, mint, and raw papaya paste for 3-4 hours.",
            "Boil basmati rice with whole spices (shahi jeera, cardamom, cloves) until 70% cooked.",
            "Layer partially cooked rice over marinated meat in a heavy-bottomed handi.",
            "Drizzle saffron milk and ghee; seal tightly with dough or foil.",
            "Cook on dum on low flame for 45-50 minutes until meat is tender and aromas release."
        ],
        "tags": ["rice", "dum", "royal", "mutton", "festive"],
        "is_favorite": True,
    },
    {
        "id": "mirchi-ka-salan",
        "title": "Hyderabadi Mirchi Ka Salan",
        "cuisine": "Hyderabadi",
        "description": "A rich, tangy, and nutty curry made with long green chillies, peanuts, sesame seeds, and tamarind, traditionally served with biryani.",
        "prep_time": "20 mins",
        "cook_time": "30 mins",
        "spice_level": "Medium",
        "difficulty": "Medium",
        "ingredients": [
            "bhavnagri green chillies",
            "peanuts",
            "sesame seeds (til)",
            "desiccated coconut",
            "tamarind pulp",
            "onions",
            "ginger garlic paste",
            "mustard seeds",
            "curry leaves",
            "turmeric",
            "coriander powder"
        ],
        "instructions": [
            "Roast peanuts, sesame seeds, and desiccated coconut, then grind into a smooth paste with fried onions.",
            "Slit large chillies and shallow fry until blistered.",
            "Temper mustard seeds and curry leaves in oil, add ginger-garlic paste and the ground nutty masala.",
            "Simmer with tamarind pulp and water until oil separates.",
            "Add fried chillies and cook on low heat for 10 minutes."
        ],
        "tags": ["curry", "tangy", "vegetarian", "biryani accompaniment"],
        "is_favorite": True,
    },
    {
        "id": "telangana-sarva-pindi",
        "title": "Telangana Sarva Pindi",
        "cuisine": "Telangana",
        "description": "A traditional savory, crispy pancake from Telangana made with rice flour, chana dal, sesame seeds, peanuts, and green chillies cooked in a deep pan.",
        "prep_time": "15 mins",
        "cook_time": "25 mins",
        "spice_level": "Spicy",
        "difficulty": "Easy",
        "ingredients": [
            "rice flour",
            "soaked chana dal",
            "peanuts",
            "sesame seeds",
            "green chillies",
            "onions",
            "curry leaves",
            "cumin seeds",
            "oil",
            "salt"
        ],
        "instructions": [
            "Soak chana dal in water for 30 minutes.",
            "In a large bowl, mix rice flour with soaked chana dal, crushed peanuts, sesame seeds, chopped onions, green chillies, curry leaves, and cumin.",
            "Add water in increments to knead into a soft pliable dough.",
            "Grease a deep pan with oil and press dough thinly across the bottom.",
            "Make small finger indentations in dough, drizzle a drop of oil into each hole, cover and cook on medium-low flame until crisp and golden brown on the underside."
        ],
        "tags": ["snack", "crispy", "rice flour", "traditional", "vegetarian"],
        "is_favorite": False,
    },
    {
        "id": "pacchi-pulusu",
        "title": "Telangana Pacchi Pulusu",
        "cuisine": "Telangana",
        "description": "An uncooked, refreshing raw tamarind soup seasoned with charred green chillies, raw onions, and fragrant tempering.",
        "prep_time": "10 mins",
        "cook_time": "5 mins",
        "spice_level": "Medium-High",
        "difficulty": "Easy",
        "ingredients": [
            "tamarind",
            "green chillies",
            "onions",
            "jaggery",
            "cumin seeds",
            "mustard seeds",
            "garlic",
            "curry leaves",
            "coriander",
            "oil",
            "salt"
        ],
        "instructions": [
            "Roast green chillies directly on open flame or pan until blistered and charred, then crush with salt and garlic.",
            "Extract tamarind juice with water to a light consistency and mix in a little jaggery.",
            "Add the crushed charred chilli-garlic paste and finely chopped raw onions into the tamarind water.",
            "Prepare a quick tempering of mustard seeds, cumin seeds, and curry leaves in oil, and pour over the pulusu.",
            "Garnish with fresh coriander; serve room temperature with hot steamed rice."
        ],
        "tags": ["soup", "tangy", "summer", "vegetarian", "quick"],
        "is_favorite": True,
    },
    {
        "id": "bagara-rice",
        "title": "Hyderabadi Bagara Rice",
        "cuisine": "Hyderabadi",
        "description": "Fragrant spiced rice tempered with whole spices, onions, mint, and coriander, popular across Telangana and Hyderabad wedding feasts.",
        "prep_time": "10 mins",
        "cook_time": "20 mins",
        "spice_level": "Mild",
        "difficulty": "Easy",
        "ingredients": [
            "basmati rice",
            "onions",
            "ginger garlic paste",
            "bay leaf",
            "cinnamon stick",
            "cloves",
            "shahi jeera",
            "cardamom",
            "mint leaves",
            "coriander leaves",
            "ghee",
            "oil"
        ],
        "instructions": [
            "Wash and soak basmati rice for 20 minutes.",
            "Heat ghee and oil in a heavy pot, add shahi jeera, bay leaf, cinnamon, cloves, and cardamom until fragrant.",
            "Add sliced onions and sauté until golden brown; stir in ginger-garlic paste, fresh mint, and coriander.",
            "Add water (1:2 ratio) and bring to a rolling boil.",
            "Add soaked rice and salt, cover, and cook on low heat until water is absorbed and grains are fluffy."
        ],
        "tags": ["rice", "aromatic", "mild", "vegetarian", "staple"],
        "is_favorite": False,
    },
]


def seed_database():
    print(f"Connecting to Firestore for project: {PROJECT_ID}...")
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection(COLLECTION_NAME)

    for item in SEEDED_RECIPES:
        doc_id = item["id"]
        doc_ref = collection_ref.document(doc_id)
        doc_ref.set(item)
        print(f"  ✓ Seeded recipe: {item['title']} (ID: {doc_id})")

    print(f"\nSuccessfully seeded {len(SEEDED_RECIPES)} recipes into Firestore collection '{COLLECTION_NAME}'!")


if __name__ == "__main__":
    seed_database()
