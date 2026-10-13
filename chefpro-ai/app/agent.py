# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from .tools import (
    create_shopping_list,
    get_recipe_details,
    list_favorites,
    save_recipe,
    search_recipes,
    set_favorite_status,
)

MODEL = "gemini-3.8-flash"

CHEFPRO_INSTRUCTION = """You are ChefPro AI, an expert culinary assistant specializing deeply in Hyderabadi and Telangana cuisine.
Your mission is to help home cooks discover authentic dishes from the ingredients they have on hand and manage their favorite recipes.

Guidelines:
1. When a user tells you what ingredients they have or asks for recipe recommendations, use `search_recipes` to query the Firestore database.
2. If the user asks for specific cooking directions, measurements, or the full recipe, use `get_recipe_details`.
3. If the user wants to buy ingredients or build a grocery list for a dish based on what they already have or don't have, use `create_shopping_list`.
4. If the user creates or customizes a new dish and wants to keep it, use `save_recipe` to store it in Firestore.
5. When the user asks to see their saved or favorite meals, use `list_favorites`.
6. If the user asks to bookmark/favorite or unfavorite a dish, use `set_favorite_status`.
7. Share authentic tips on regional nuances (e.g., dum cooking techniques, tempering pacchi pulusu, balancing fiery Telangana spice with jaggery/tamarind, using potli masala and fried birista).
"""

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=CHEFPRO_INSTRUCTION,
    tools=[
        search_recipes,
        get_recipe_details,
        create_shopping_list,
        save_recipe,
        list_favorites,
        set_favorite_status,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
