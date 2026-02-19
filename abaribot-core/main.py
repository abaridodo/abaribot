
from llms import LLMService
from enum import Enum
from typing import List, Dict, Any, Optional
import json
import asyncio
async def get_ophthalmology_advice():
    # Initialize the LLM service
    llm_service = LLMService()

    # User's question about glaucoma
    user_query = "What are the early symptoms of glaucoma I should watch for?"

    # Context retrieved from medical knowledge base
    medical_context = """
    [MEDICAL CONTEXT]
    Glaucoma is a group of eye conditions that damage the optic nerve.
    Early symptoms are often absent, but may include:
    - Gradual loss of peripheral vision
    - Seeing halos around lights
    - Eye redness or discomfort
    - Vision changes in low light

    Risk factors: Age over 60, family history, diabetes.
    First-line treatment: Prostaglandin analogs like latanoprost.
    """

    # Prepare messages in chat format
    messages = [
        {
            "role": "user",
            "content": user_query
        }
    ]

    try:
        # Get response from LLM
        response = await llm_service.generate_response(
            messages=messages,
            context=medical_context,
            temperature=0.3  
        )


        # Extract the actual content
        if "response" in response["content"]:
            return response["content"]["response"]
        else:
            return "I recommend consulting an ophthalmologist for personalized advice."

    except Exception as e:
        print(f"Error getting response: {e}")
        return "Our medical advice service is currently unavailable."

# Run the example
if __name__ == "__main__":
    response =  asyncio.run(get_ophthalmology_advice())

    print("\nFinal Response:")
    print(response)