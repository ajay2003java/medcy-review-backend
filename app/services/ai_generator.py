from openai import OpenAI
from app.core.config import settings
from app.core.constants import ClinicCategory

# Initialize only if API key is provided, otherwise mock it for testing
client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

def generate_review_draft(clinic_name: str, category: ClinicCategory, rating: int) -> str:
    """
    Generates a tailored review draft using AI based on the clinic category and rating.
    """
    if not client:
        return f"I had a fantastic experience at {clinic_name}. The {category.value} team was highly professional and caring. Highly recommended!"

    prompt = f"Write a short, highly positive, natural-sounding Google review (2-3 sentences) for a {category.value} clinic named {clinic_name}. The patient gave it a {rating}/5 star rating. Do not use hashtags."
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # or gpt-4
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes brief, natural Google reviews for patients."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=60,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating review: {e}")
        return f"I had a great experience at {clinic_name}. The staff was excellent and I highly recommend them."
