from openai import OpenAI
from app.core.config import settings
from app.core.constants import ClinicCategory

# Initialize only if API key is provided, otherwise mock it for testing
client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

def generate_review_draft(clinic_name: str, category: ClinicCategory, rating: int, service_received: str = None) -> str:
    """
    Generates a tailored review draft using AI based on the clinic category, rating, and service received.
    """
    if not client:
        service_text = f" for my {service_received} treatment" if service_received else ""
        return f"I had a fantastic experience at {clinic_name}{service_text}. The {category.value} team was highly professional and caring. Highly recommended!"

    service_context = f" The patient specifically received '{service_received}' as their treatment. " if service_received else " "

    prompt = (
        f"Write a short, highly positive, and natural-sounding Google review (2-3 sentences) for a {category.value} clinic named {clinic_name}. "
        f"The patient gave it a {rating}/5 star rating.{service_context}"
        f"CRITICAL: Ensure the review naturally includes strong SEO keywords related to {category.value} services (e.g., 'best {category.value} clinic', 'top treatments', 'highly recommended doctors'). "
        f"Make it sound completely unique, personal, and different from a generic review. Do not use hashtags."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # or gpt-4
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes highly unique, varied, and SEO-optimized Google reviews for patients. Never generate the exact same review twice."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=70,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating review: {e}")
        return f"I had a great experience at {clinic_name}. The staff was excellent and I highly recommend them."

def generate_institute_review_draft(institute_name: str, role: str, rating: int, service_received: str = None) -> str:
    """
    Generates a tailored review draft using AI based on the reviewer's role (Student, Parent, Staff).
    """
    if not client:
        service_text = f" regarding the {service_received} program" if service_received else ""
        return f"My experience with {institute_name}{service_text} has been wonderful. The environment is incredibly positive and supportive!"

    service_context = f" They are specifically associated with the '{service_received}' program/aspect. Ensure the generated review naturally incorporates this as a strong SEO keyword (e.g. 'best {service_received} coaching'). " if service_received else " "

    prompt = (
        f"Write a short, highly positive, and natural-sounding Google review (2-3 sentences) for an educational institute named {institute_name}. "
        f"The reviewer gave it a {rating}/5 star rating. "
        f"CRITICAL CONTEXT: The person writing the review is a '{role}'. "
        f"If they are a Parent, it must sound like a proud parent whose child attends the school. "
        f"If they are a Student or Alumni, it must sound like a student talking about their studies and campus life. "
        f"If they are Staff, it must sound like an employee talking about the great work environment and management. "
        f"{service_context}"
        f"Make it sound completely unique, personal, and different from a generic review. Do not use hashtags."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes highly unique, varied, and context-specific Google reviews for educational institutes. Never generate the exact same review twice."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=80,
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating institute review: {e}")
        return f"My experience with {institute_name} has been wonderful. The environment is incredibly positive and supportive!"
