"""Firestore-backed tools for ChefPro AI."""

import re
from typing import Any
from google.cloud import firestore
from google.cloud.firestore import FieldFilter

# Hardcoded project ID as string to avoid project number issues on Agent Platform
PROJECT_ID = "qwiklabs-gcp-04-48ac5222ff71"
COLLECTION_NAME = "recipes"

_db_client: firestore.Client | None = None


def _get_db() -> firestore.Client:
    """Returns a singleton Firestore client configured with the hardcoded project ID."""
    global _db_client
    if _db_client is None:
        _db_client = firestore.Client(project=PROJECT_ID)
    return _db_client


def search_recipes(ingredients: str = "", cuisine: str = "") -> dict[str, Any]:
    """Search for authentic recipes in the database based on available ingredients or cuisine.

    Args:
        ingredients: Comma-separated list of ingredients on hand (e.g., 'rice, onions, mint' or 'tamarind, green chillies').
        cuisine: Optional cuisine filter (e.g., 'Hyderabadi' or 'Telangana').

    Returns:
        A dictionary containing the list of matching recipes with details.
    """
    db = _get_db()
    collection_ref = db.collection(COLLECTION_NAME)

    query = collection_ref
    if cuisine:
        cleaned_cuisine = cuisine.strip().capitalize()
        query = query.where(filter=FieldFilter("cuisine", "==", cleaned_cuisine))

    docs = list(query.stream())
    results = []

    # Parse search keywords from ingredients
    keywords = [k.strip().lower() for k in re.split(r"[,;]+", ingredients) if k.strip()]

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id

        if not keywords:
            results.append(data)
            continue

        doc_ingredients = [str(ing).lower() for ing in data.get("ingredients", [])]
        doc_text = (
            f"{data.get('title', '')} {data.get('description', '')} {' '.join(doc_ingredients)}"
        ).lower()

        matched_ingredients = [
            kw for kw in keywords if any(kw in ing for ing in doc_ingredients) or kw in doc_text
        ]

        if matched_ingredients:
            data["matched_ingredients"] = matched_ingredients
            results.append(data)

    return {
        "status": "success",
        "count": len(results),
        "recipes": results,
    }


def get_recipe_details(recipe_id: str) -> dict[str, Any]:
    """Retrieve complete recipe details including step-by-step cooking instructions and full ingredient list.

    Args:
        recipe_id: The unique ID or slug of the recipe (e.g., 'hyderabadi-dum-biryani', 'telangana-sarva-pindi', 'pacchi-pulusu').

    Returns:
        A dictionary containing the complete recipe details or an error message if not found.
    """
    db = _get_db()
    clean_id = recipe_id.strip().lower().replace(" ", "-")
    doc_ref = db.collection(COLLECTION_NAME).document(clean_id)
    doc = doc_ref.get()

    if not doc.exists:
        for d in db.collection(COLLECTION_NAME).stream():
            data = d.to_dict()
            if recipe_id.lower() in data.get("title", "").lower():
                data["id"] = d.id
                return {"status": "success", "recipe": data}
        return {"status": "error", "message": f"Recipe with ID or title '{recipe_id}' not found."}

    data = doc.to_dict()
    data["id"] = doc.id
    return {"status": "success", "recipe": data}


def save_recipe(
    title: str,
    cuisine: str,
    description: str,
    ingredients: list[str],
    instructions: list[str],
    prep_time: str = "20 mins",
    cook_time: str = "30 mins",
    spice_level: str = "Medium",
    difficulty: str = "Medium",
) -> dict[str, Any]:
    """Save a new recipe or custom meal to the database.

    Args:
        title: Title of the dish (e.g., 'Telangana Sakinalu' or 'Hyderabadi Chicken Korma').
        cuisine: Cuisine type ('Hyderabadi', 'Telangana', or other regional cuisine).
        description: Brief description of the dish and flavor profile.
        ingredients: List of all required ingredients.
        instructions: Ordered list of step-by-step cooking directions.
        prep_time: Preparation time (e.g., '15 mins').
        cook_time: Cooking time (e.g., '30 mins').
        spice_level: Spice level ('Mild', 'Medium', 'Spicy', or 'Fiery').
        difficulty: Cooking difficulty ('Easy', 'Medium', or 'Advanced').

    Returns:
        A dictionary confirming the recipe was saved with its generated recipe ID.
    """
    db = _get_db()
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    doc_ref = db.collection(COLLECTION_NAME).document(slug)

    recipe_data = {
        "id": slug,
        "title": title.strip(),
        "cuisine": cuisine.strip().capitalize(),
        "description": description.strip(),
        "ingredients": ingredients,
        "instructions": instructions,
        "prep_time": prep_time,
        "cook_time": cook_time,
        "spice_level": spice_level,
        "difficulty": difficulty,
        "is_favorite": True,
        "tags": [cuisine.lower(), spice_level.lower()],
    }

    doc_ref.set(recipe_data)
    return {
        "status": "success",
        "recipe_id": slug,
        "message": f"Recipe '{title}' saved successfully to Firestore.",
    }


def list_favorites() -> dict[str, Any]:
    """Retrieve all recipes marked as favorites by the user.

    Returns:
        A dictionary containing the list of favorite recipes.
    """
    db = _get_db()
    query = db.collection(COLLECTION_NAME).where(filter=FieldFilter("is_favorite", "==", True))
    docs = list(query.stream())

    favorites = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        favorites.append(data)

    return {
        "status": "success",
        "count": len(favorites),
        "favorites": favorites,
    }


def set_favorite_status(recipe_id: str, is_favorite: bool) -> dict[str, Any]:
    """Update the favorite status of a recipe in the database.

    Args:
        recipe_id: The ID of the recipe to update.
        is_favorite: True to add to favorites, False to remove.

    Returns:
        A dictionary confirming the updated status.
    """
    db = _get_db()
    clean_id = recipe_id.strip().lower().replace(" ", "-")
    doc_ref = db.collection(COLLECTION_NAME).document(clean_id)
    doc = doc_ref.get()

    if not doc.exists:
        return {"status": "error", "message": f"Recipe '{recipe_id}' not found."}

    doc_ref.update({"is_favorite": is_favorite})
    status_text = "favorited" if is_favorite else "unfavorited"
    return {
        "status": "success",
        "recipe_id": clean_id,
        "message": f"Recipe '{doc.to_dict().get('title', clean_id)}' successfully {status_text}.",
    }


def create_shopping_list(recipe_id: str, on_hand_ingredients: str = "") -> dict[str, Any]:
    """Generate a grocery shopping list of missing ingredients for a recipe and save it to Firestore.

    Args:
        recipe_id: The ID or title of the recipe (e.g., 'hyderabadi-dum-biryani' or 'telangana-sarva-pindi').
        on_hand_ingredients: Comma-separated list of ingredients already available in the pantry.

    Returns:
        A dictionary with the missing ingredients list and saved shopping list ID.
    """
    recipe_info = get_recipe_details(recipe_id)
    if recipe_info.get("status") != "success":
        return recipe_info

    recipe = recipe_info["recipe"]
    required_ingredients = recipe.get("ingredients", [])

    on_hand = [item.strip().lower() for item in re.split(r"[,;]+", on_hand_ingredients) if item.strip()]

    missing = []
    for ing in required_ingredients:
        ing_lower = str(ing).lower()
        if not any(oh in ing_lower for oh in on_hand):
            missing.append(ing)

    db = _get_db()
    slug = f"shop-{recipe.get('id', 'list')}"
    doc_ref = db.collection("shopping_lists").document(slug)
    list_data = {
        "recipe_id": recipe.get("id"),
        "recipe_title": recipe.get("title"),
        "missing_ingredients": missing,
        "on_hand_ingredients": on_hand,
    }
    doc_ref.set(list_data)

    return {
        "status": "success",
        "shopping_list_id": slug,
        "recipe_title": recipe.get("title"),
        "missing_count": len(missing),
        "missing_ingredients": missing,
    }

