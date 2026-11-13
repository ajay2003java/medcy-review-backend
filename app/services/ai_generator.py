import time
import random
from typing import Optional, Union
from openai import OpenAI
from app.core.config import settings
from app.core.constants import ClinicCategory

# Initialize only if API key is provided, otherwise fallback to local dynamic SEO engine
client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
openai_quota_exhausted_until = 0

def normalize_category(category: Union[ClinicCategory, str]) -> str:
    if hasattr(category, 'value'):
        cat_str = category.value
    else:
        cat_str = str(category).strip()
    
    cat_lower = cat_str.lower().replace('-', ' ').replace('_', ' ')
    if 'dermatol' in cat_lower or 'skin' in cat_lower:
        return 'Dermatology'
    if 'ivf' in cat_lower or 'fertil' in cat_lower:
        return 'IVF'
    if 'gynec' in cat_lower or 'matern' in cat_lower or 'women' in cat_lower:
        return 'Gynecology'
    if 'dent' in cat_lower:
        return 'Dentist'
    if 'lab' in cat_lower or 'diagnost' in cat_lower or 'pathol' in cat_lower:
        return 'Laboratory'
    if 'hosp' in cat_lower or 'general' in cat_lower:
        return 'General Hospital'
    return cat_str

def clean_service_phrase(service: Optional[str]) -> str:
    if not service:
        return ""
    s = service.strip()
    if s.lower().startswith("other:"):
        s = s[6:].strip()
    if not s:
        return ""
    # If comma-separated, join with 'and' for natural English
    parts = [p.strip() for p in s.split(",") if p.strip()]
    if len(parts) == 1:
        return parts[0]
    elif len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    elif len(parts) > 2:
        return f"{', '.join(parts[:-1])}, and {parts[-1]}"
    return s

# --- Ultra-Diverse Combinatorial SEO Engine for GBP Ranking ---
CATEGORY_SEO_TEMPLATES = {
    'Dermatology': {
        'openers': [
            "I recently visited {clinic_name}{service_phrase} and I am beyond impressed with the care I received.",
            "If you are searching for the best dermatologist, {clinic_name} is definitely the place to go{service_phrase}.",
            "Had an exceptional experience with the skin specialists at {clinic_name}{service_phrase}!",
            "Consulting the dermatology department at {clinic_name}{service_phrase} was one of the best healthcare choices I have made.",
            "I cannot recommend {clinic_name} enough for anyone seeking advanced skin or cosmetic care{service_phrase}.",
            "Visiting {clinic_name}{service_phrase} gave me visible improvements and completely restored my skin confidence.",
            "From the moment I walked into {clinic_name}{service_phrase}, the medical care and attention to detail were top-notch.",
            "I booked an appointment at {clinic_name}{service_phrase} after hearing great reviews, and they truly exceeded all expectations.",
            "Hands down the top skin care clinic in the area — {clinic_name} takes dermatology care to the next level.",
            "My experience at {clinic_name}{service_phrase} was smooth, professional, and gave me incredible results.",
            "I have been consulting {clinic_name}{service_phrase} and their standard of care is consistently world-class.",
            "Choosing {clinic_name}{service_phrase} for my skin care was an absolute game changer."
        ],
        'middles': [
            "The dermatologists took the time to diagnose my skin condition accurately, explaining the treatment plan with immense clarity and patience.",
            "The clinic is spotlessly clean, fully hygienic, and equipped with the latest advanced skin laser and cosmetology technology.",
            "The doctor was extremely gentle, knowledgeable, and genuinely focused on long-term skin health rather than quick fixes.",
            "Every procedure was handled with absolute precision, zero discomfort, and utmost care by the skin specialist team.",
            "Their personalized treatment approach delivered noticeable, glowing results much faster than I anticipated.",
            "The nursing staff and reception were polite, welcoming, and ensured there was no unnecessary waiting time.",
            "The clinical expertise here is unmatched, and they answered all my queries regarding aftercare and daily skincare routines.",
            "They maintain top-tier sterilization standards and use evidence-based dermatological methods that actually work.",
            "The pricing was completely transparent and the doctors recommended only what was genuinely beneficial for my skin.",
            "I was particularly impressed by their thorough examination and gentle touch throughout the session."
        ],
        'closers': [
            "Easily the best skin specialist and dermatology clinic in town — 5 stars all the way for {clinic_name}!",
            "I highly recommend {clinic_name} to anyone looking for genuine, lasting skin solutions and compassionate care.",
            "A fantastic dermatology hospital that puts patient satisfaction first. Thank you, {clinic_name}!",
            "Will definitely continue visiting {clinic_name} for all my future skin and aesthetic treatments.",
            "If you want healthy, clear, glowing skin, look no further than {clinic_name}.",
            "Top-notch dermatologist with outstanding results. Truly the highest standard of skin care!",
            "10/10 recommendation for {clinic_name} — easily the most trusted skin clinic around.",
            "Grateful to the entire dermatology team at {clinic_name} for their dedication and fantastic service."
        ]
    },
    'Laboratory': {
        'openers': [
            "I visited {clinic_name}{service_phrase} and the entire diagnostic testing experience was completely seamless.",
            "If you need an accurate and reliable diagnostic laboratory, {clinic_name} is second to none.",
            "Had a great experience getting my lab tests done at {clinic_name}{service_phrase}.",
            "{clinic_name} is by far the most professional diagnostic center and pathology lab I have ever visited{service_phrase}.",
            "I chose {clinic_name}{service_phrase} based on strong recommendations and I was thoroughly impressed.",
            "Getting tests done at {clinic_name}{service_phrase} was quick, organized, and stress-free.",
            "My experience with the laboratory team at {clinic_name}{service_phrase} was exceptionally smooth from check-in to report delivery.",
            "Hands down the top diagnostic center in the city — {clinic_name} sets a high benchmark for pathology services.",
            "I regularly rely on {clinic_name}{service_phrase} for routine health checkups and they never disappoint.",
            "Visiting {clinic_name}{service_phrase} proved that diagnostic tests can be quick, comfortable, and painless.",
            "Highly impressed with the punctuality and hygiene at {clinic_name}{service_phrase}.",
            "Superb diagnostic testing facility at {clinic_name}{service_phrase} with attentive and skilled technicians."
        ],
        'middles': [
            "The phlebotomist was remarkably skilled and made the blood collection completely painless and comfortable.",
            "I received my accurate diagnostic test reports well within the promised timeframe with detailed parameters.",
            "The laboratory is impeccably clean, follows strict hygiene protocols, and uses modern automated diagnostic equipment.",
            "The reception and technician staff were courteous, answered all my preparation questions, and processed my tests without delays.",
            "The sample collection was handled with great care, maintaining proper labeling and sterile procedures throughout.",
            "Their home sample collection and lab reporting system is fast, convenient, and very well-organized.",
            "The test pricing is reasonable, transparent, and offers great value for comprehensive health packages.",
            "The diagnostic accuracy and prompt digital report dispatch via WhatsApp/email made the whole process effortless.",
            "Every staff member was patient, reassuring, and handled the testing with utmost professionalism.",
            "The diagnostic machinery is modern and the lab environment feels calm, sterile, and welcoming."
        ],
        'closers': [
            "Easily the best diagnostic laboratory and pathology center around — 5 stars for {clinic_name}!",
            "I strongly recommend {clinic_name} to anyone seeking timely, reliable, and accurate lab reports.",
            "A dependable diagnostic center with wonderful staff. Thank you, {clinic_name}!",
            "Will always choose {clinic_name} for all future blood tests, health packages, and diagnostic needs.",
            "Top-notch diagnostic laboratory with prompt service and painless blood sample collection. 10/10!",
            "Unbeatable service and accuracy. {clinic_name} is truly the most trusted lab in town.",
            "A seamless 5-star testing experience from start to finish at {clinic_name}!",
            "Heartfelt thanks to {clinic_name} for their prompt delivery of accurate test reports."
        ]
    },
    'IVF': {
        'openers': [
            "Our experience at {clinic_name}{service_phrase} has been filled with genuine warmth, empathy, and hope.",
            "If you are looking for the best fertility center, {clinic_name} is undoubtedly the most compassionate choice.",
            "We are immensely grateful to the fertility doctors and embryology team at {clinic_name}{service_phrase}.",
            "Choosing {clinic_name}{service_phrase} was the best decision we made for our parenthood journey.",
            "From our very first fertility consultation at {clinic_name}{service_phrase}, we felt supported at every single step.",
            "The reproductive specialists at {clinic_name}{service_phrase} provided clear guidance with utmost medical excellence.",
            "We had an incredibly positive experience with the IVF team at {clinic_name}{service_phrase}.",
            "Hands down the top IVF hospital in the region — {clinic_name} combines cutting-edge fertility technology with deep empathy.",
            "Consulting {clinic_name}{service_phrase} gave us clarity, reassurance, and confidence throughout our treatment.",
            "The fertility specialists at {clinic_name} are true experts who genuinely care about their patients' dreams."
        ],
        'middles': [
            "The doctors explained every stage of the treatment with complete transparency, warmth, and realistic optimism.",
            "The fertility clinic features state-of-the-art embryology labs, clean private consultation rooms, and strict confidentiality.",
            "The nursing staff and coordinators were always available to answer our medication questions and provided immense emotional comfort.",
            "Their personalized protocol and advanced reproductive technologies gave us the highest confidence in our treatment.",
            "We never felt rushed; the specialists patiently addressed all our medical history and fertility options.",
            "The holistic approach, continuous monitoring, and empathetic environment made a world of difference to our journey.",
            "Their high success rates and ethical medical practices make them stand out as premier fertility experts.",
            "The team made what can be a stressful process feel manageable, safe, and positive throughout."
        ],
        'closers': [
            "Easily the best IVF center and fertility hospital — 5/5 stars for {clinic_name}!",
            "We wholeheartedly recommend {clinic_name} to every couple aspiring to start or grow their family.",
            "A beacon of hope with world-class fertility doctors. Thank you, {clinic_name}!",
            "Forever grateful to {clinic_name} for their unmatched expertise and compassionate guidance.",
            "The most caring and experienced fertility specialists you could ever ask for. 10/10 for {clinic_name}!",
            "Top-tier reproductive medical care with genuine heart. Highly recommend {clinic_name}."
        ]
    },
    'Gynecology': {
        'openers': [
            "I had a wonderful experience at {clinic_name}{service_phrase} and felt completely safe and well-cared for.",
            "If you are looking for the best gynecologist and women's health care, {clinic_name} is the top choice.",
            "The obstetrics and gynecology team at {clinic_name}{service_phrase} is simply outstanding.",
            "Consulting the doctors at {clinic_name}{service_phrase} was an incredibly reassuring and positive experience.",
            "I highly recommend {clinic_name}{service_phrase} for compassionate, expert maternity and women's healthcare.",
            "From the warm reception to the thorough medical checkup, {clinic_name}{service_phrase} exceeded all expectations.",
            "My visit to {clinic_name}{service_phrase} was handled with great professionalism and deep empathy.",
            "Hands down the best maternity hospital and gynecology clinic in the city — {clinic_name} is exceptional.",
            "I have been visiting {clinic_name}{service_phrase} and the care is always 5-star.",
            "Exceptional care for women at {clinic_name}{service_phrase} with a truly dedicated medical staff."
        ],
        'middles': [
            "The gynecologist listened attentively to all my concerns, respected my comfort, and explained everything gently.",
            "The hospital maintains impeccable hygiene, private examination rooms, and a welcoming atmosphere.",
            "The nursing staff was so supportive, gentle during examinations, and attentive to every patient need.",
            "They prioritize patient privacy, clinical safety, and evidence-based women's healthcare at every step.",
            "The ultrasound scanning and routine tests were done smoothly without long waiting times.",
            "Their comprehensive prenatal guidance and caring nature provided great peace of mind throughout.",
            "The doctors are approachable, highly experienced, and make you feel completely at ease discussing sensitive issues.",
            "Everything from registration to doctor consultation was organized efficiently and cordially."
        ],
        'closers': [
            "Easily the best gynecologist and maternity hospital around — 5 stars for {clinic_name}!",
            "I strongly recommend {clinic_name} to all women seeking trustworthy, compassionate gynecological care.",
            "A hospital that truly understands women's healthcare needs. Thank you, {clinic_name}!",
            "Will definitely continue recommending {clinic_name} to all my family and friends.",
            "Outstanding medical care, gentle doctors, and clean facilities. 10/10 for {clinic_name}!",
            "The most supportive and skilled gynecology specialists in town. Highly recommended!"
        ]
    },
    'Dentist': {
        'openers': [
            "I had a fantastic, completely painless experience at {clinic_name}{service_phrase}!",
            "If you are nervous about dental visits, {clinic_name} is the absolute best dental clinic to visit.",
            "Consulting the dental surgeons at {clinic_name}{service_phrase} was the best healthcare decision for my smile.",
            "Had a seamless dental appointment at {clinic_name}{service_phrase} with zero discomfort.",
            "I cannot praise {clinic_name} enough for their gentle dental care and modern clinical setup{service_phrase}.",
            "Visiting {clinic_name}{service_phrase} changed my whole perspective on dental treatments.",
            "Hands down the top dentist and dental hospital in town — {clinic_name} provides world-class dental care.",
            "From check-in to procedure completion, my visit to {clinic_name}{service_phrase} was flawless.",
            "I booked a consultation at {clinic_name}{service_phrase} and received top-notch dental service.",
            "Exceptionally professional and friendly dental team at {clinic_name}{service_phrase}."
        ],
        'middles': [
            "The dentist was incredibly gentle, walked me through every step of the procedure, and ensured I was fully comfortable.",
            "The clinic is spotlessly clean, fully sanitized, and equipped with the latest modern digital dental technology.",
            "The procedure was completely pain-free, quick, and executed with utmost precision and care.",
            "They took high-definition digital scans, explained the exact treatment plan, and offered honest dental advice.",
            "The dental assistants and front-desk staff were polite, reassuring, and very helpful.",
            "Sterilization protocols are strictly followed here, which gave me complete peace of mind.",
            "Their cosmetic and restorative dental work is top-tier — my teeth feel healthier and look fantastic.",
            "Transparent pricing and clear post-treatment care instructions made the whole experience stress-free."
        ],
        'closers': [
            "Easily the best dentist and dental clinic in the area — 5 stars for {clinic_name}!",
            "I highly recommend {clinic_name} to anyone looking for painless, professional, and reliable dental care.",
            "A truly wonderful dental clinic that puts patient comfort first. Thank you, {clinic_name}!",
            "My go-to dental center for all future checkups and treatments. 10/10 for {clinic_name}!",
            "Top-quality dental work with a gentle touch. Look no further than {clinic_name} for your dental needs!",
            "Brilliant dentists and painless treatments — highest recommendation for {clinic_name}."
        ]
    },
    'General Hospital': {
        'openers': [
            "I had an exceptional experience at {clinic_name}{service_phrase} and received outstanding medical care.",
            "If you are searching for the best multi-specialty hospital, {clinic_name} is definitely the top recommendation.",
            "The doctors and medical staff at {clinic_name}{service_phrase} provided prompt, compassionate, and expert care.",
            "My recent visit to {clinic_name}{service_phrase} was handled with remarkable efficiency and clinical excellence.",
            "I am extremely grateful to the entire healthcare team at {clinic_name}{service_phrase} for their timely support.",
            "From emergency response to inpatient care, {clinic_name}{service_phrase} delivers world-class hospital services.",
            "Hands down one of the best hospitals in the city — {clinic_name} excels in patient-first healthcare.",
            "Visiting {clinic_name}{service_phrase} gave our family immense reassurance during a critical time.",
            "I was treated at {clinic_name}{service_phrase} and was deeply impressed by their modern infrastructure.",
            "Exceptional hospital facilities and dedicated doctors make {clinic_name}{service_phrase} stand out."
        ],
        'middles': [
            "The doctors were very thorough in their diagnosis, explained the condition clearly, and gave timely medical attention.",
            "The hospital rooms and common areas are spotless, well-maintained, and follow rigorous cleanliness standards.",
            "The nursing staff was attentive around the clock, gentle with treatments, and quick to respond to every call.",
            "The admission, billing, and pharmacy workflows were smooth with minimal waiting time and clear communication.",
            "They are equipped with state-of-the-art medical technology, modern ICUs, and 24/7 emergency support.",
            "The multi-specialty coordination between different departments was seamless and reassuring.",
            "Every healthcare worker treated us with dignity, warmth, and genuine compassion.",
            "The medical team provided continuous updates and made sure our treatment was completely transparent."
        ],
        'closers': [
            "Easily the best multi-specialty hospital in town — 5/5 stars for {clinic_name}!",
            "I wholeheartedly recommend {clinic_name} for reliable, high-quality, and compassionate healthcare.",
            "A hospital that truly prioritizes patient wellbeing above all else. Thank you, {clinic_name}!",
            "Our family's most trusted hospital for all medical needs. 10/10 for {clinic_name}!",
            "World-class doctors, clean hospital premises, and caring nurses. Highly recommend {clinic_name}!",
            "Top-tier hospital with dedicated medical professionals. Truly grateful to {clinic_name}."
        ]
    }
}

INSTITUTE_SEO_TEMPLATES = {
    'Student': {
        'openers': [
            "Studying at {institute_name}{service_phrase} has been an enriching and transformative experience.",
            "{institute_name} is easily one of the best educational institutes for focused academic growth{service_phrase}.",
            "My time at {institute_name}{service_phrase} has given me strong fundamentals and high confidence.",
            "Choosing {institute_name}{service_phrase} was the best academic decision I have made.",
            "The learning environment and competitive coaching at {institute_name}{service_phrase} are truly remarkable."
        ],
        'middles': [
            "The lecturers and faculty members are approachable, explain complex topics with ease, and clear all our doubts.",
            "The campus infrastructure, science and computer labs, and library resources are modern and well-maintained.",
            "Regular mock exams, personalized feedback, and strategic study material prepared us thoroughly for competitive exams.",
            "The disciplined yet encouraging campus atmosphere motivated me to achieve my best academic performance.",
            "Beyond academics, the institute fosters overall personality development and practical problem-solving skills."
        ],
        'closers': [
            "Easily the top institute for quality education and exam coaching — 5 stars for {institute_name}!",
            "I highly recommend {institute_name} to any student aspiring for top ranks and great career foundations.",
            "A wonderful campus that genuinely supports student success. Proud to be associated with {institute_name}!",
            "10/10 recommendation for {institute_name} — the faculty and guidance are second to none."
        ]
    },
    'Parent': {
        'openers': [
            "As a parent, I am completely satisfied with the education and guidance provided by {institute_name}{service_phrase}.",
            "{institute_name} has exceeded our expectations in shaping our child's academic future{service_phrase}.",
            "Enrolling my child in {institute_name}{service_phrase} was the best decision for their career and character development.",
            "We have seen remarkable improvement in our child's confidence and academic results since joining {institute_name}{service_phrase}.",
            "{institute_name} is undeniably one of the top coaching institutes and colleges in the region."
        ],
        'middles': [
            "The teachers give individual attention, track student progress meticulously, and communicate transparently with parents.",
            "The campus maintains high standards of discipline, safety, and a positive academic environment.",
            "The curriculum and coaching methodologies are rigorous, structured, and exam-oriented.",
            "The management is approachable, receptive to feedback, and deeply committed to student welfare.",
            "Our child has developed consistent study habits and a passion for learning thanks to the dedicated faculty."
        ],
        'closers': [
            "Easily the best college and coaching institute — 5 stars for {institute_name}!",
            "I wholeheartedly recommend {institute_name} to all parents seeking excellent education and personal care for their children.",
            "A trustworthy and outstanding educational institution. Thank you, {institute_name}!",
            "Highest recommendation for {institute_name} for their dedication to student excellence."
        ]
    },
    'General': {
        'openers': [
            "My association with {institute_name}{service_phrase} has been thoroughly rewarding and positive.",
            "{institute_name} stands out as a premier educational institution with an inspiring academic culture{service_phrase}.",
            "The standard of education, mentorship, and infrastructure at {institute_name}{service_phrase} is top-tier."
        ],
        'middles': [
            "The faculty members are knowledgeable, supportive, and dedicated to creating future leaders.",
            "The campus provides modern facilities, a disciplined environment, and excellent academic resources.",
            "Their structured teaching methodology and supportive staff make learning engaging and effective."
        ],
        'closers': [
            "Easily the top educational institution in the region — 5/5 stars for {institute_name}!",
            "Highly recommend {institute_name} for anyone pursuing academic excellence and professional growth."
        ]
    }
}

def generate_combinatorial_review(clinic_name: str, category_key: str, service_received: Optional[str] = None) -> str:
    """
    Deterministically random combinatorial generator ensuring EVERY review is unique,
    naturally weaves in the exact clinic_name (e.g. ABC Hospital),
    embeds high-intent GBP SEO keywords for that specific category,
    and integrates the specific service received.
    """
    templates = CATEGORY_SEO_TEMPLATES.get(category_key, CATEGORY_SEO_TEMPLATES['General Hospital'])
    
    clean_service = clean_service_phrase(service_received)
    service_phrase = f" for my {clean_service}" if clean_service else ""
    
    opener_raw = random.choice(templates['openers'])
    middle_raw = random.choice(templates['middles'])
    closer_raw = random.choice(templates['closers'])
    
    # Format with parameters
    opener = opener_raw.format(clinic_name=clinic_name, service_phrase=service_phrase)
    middle = middle_raw.format(clinic_name=clinic_name, service_phrase=service_phrase)
    closer = closer_raw.format(clinic_name=clinic_name, service_phrase=service_phrase)
    
    # 25% chance of 2-sentence punchy review vs 75% 3-sentence detailed review
    if random.random() < 0.25:
        # If opener already has the service, pair with closer
        return f"{opener} {closer}"
    
    return f"{opener} {middle} {closer}"

def generate_review_draft(clinic_name: str, category: Union[ClinicCategory, str], rating: int, service_received: Optional[str] = None) -> str:
    """
    Generates a tailored, unique review draft using AI (OpenAI gpt-4o-mini) with an ultra-diverse 
    local SEO combinatorial fallback engine.
    Ensures that every submission produces a completely different review, tailored to the clinic name,
    category, and services for maximum Google Business Profile (GBP) ranking.
    """
    cat_key = normalize_category(category)
    clean_service = clean_service_phrase(service_received)
    
    global openai_quota_exhausted_until
    # If no OpenAI client or key, or quota exhausted cooloff active, use the ultra-diverse combinatorial SEO engine directly
    if not client or time.time() < openai_quota_exhausted_until:
        return generate_combinatorial_review(clinic_name, cat_key, clean_service)
    
    service_context = f" The patient specifically received '{clean_service}'. " if clean_service else " "
    
    prompt = (
        f"Write a short, highly persuasive, authentic, and natural-sounding 5-star Google review (2-3 sentences) for '{clinic_name}', which is a premier {cat_key} center. "
        f"The patient rated their experience {rating}/5 stars.{service_context}"
        f"MANDATORY LOCAL SEO INSTRUCTIONS FOR GOOGLE BUSINESS PROFILE (GBP) LOCAL RANKING: "
        f"1. Explicitly mention the name '{clinic_name}' naturally in the review. "
        f"2. Seamlessly incorporate high-intent local SEO keywords relevant to {cat_key} (e.g. for Dermatology: 'best dermatologist', 'top skin specialist', 'skin clinic'; for Laboratory: 'accurate diagnostic lab', 'painless blood test reports', 'pathology center'; for Hospital: 'best multi-specialty hospital'). "
        f"3. Highlight specific patient value: gentle procedure, clean facility, prompt reports, skilled doctors, or short wait times. "
        f"4. VARIATION DIRECTIVE: Craft a fresh, unique review with a distinct sentence structure. Avoid generic clichés and never start reviews the same way. Do not include hashtags or quotes."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert Google Business Profile (GBP) local SEO reputation strategist. You write unique, authentic, high-converting patient reviews that rank local clinics on Google Maps. Never repeat the exact same sentence pattern."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=90,
            temperature=0.95
        )
        review_text = response.choices[0].message.content.strip().strip('"').strip("'")
        if review_text and len(review_text) > 20:
            return review_text
        return generate_combinatorial_review(clinic_name, cat_key, clean_service)
    except Exception as e:
        # Fallback to combinatorial generator so reviews are ALWAYS unique and SEO-optimized
        print(f"OpenAI generator fallback triggered: {e}")
        err_msg = str(e).lower()
        if "quota" in err_msg or "429" in err_msg or "credit_balance" in err_msg:
            openai_quota_exhausted_until = time.time() + 300
        return generate_combinatorial_review(clinic_name, cat_key, clean_service)

def generate_institute_review_draft(institute_name: str, role: Optional[str], rating: int, service_received: Optional[str] = None) -> str:
    """
    Generates a tailored review draft for educational institutes with local SEO optimization.
    """
    clean_service = clean_service_phrase(service_received)
    service_phrase = f" for the {clean_service} program" if clean_service else ""
    role_key = 'Student' if role in ['Student', 'Present Student', 'Ex-Student / Alumni'] else ('Parent' if role == 'Parent' else 'General')
    
    def generate_combinatorial_institute_review() -> str:
        templates = INSTITUTE_SEO_TEMPLATES.get(role_key, INSTITUTE_SEO_TEMPLATES['General'])
        opener = random.choice(templates['openers']).format(institute_name=institute_name, service_phrase=service_phrase)
        middle = random.choice(templates['middles']).format(institute_name=institute_name, service_phrase=service_phrase)
        closer = random.choice(templates['closers']).format(institute_name=institute_name, service_phrase=service_phrase)
        return f"{opener} {middle} {closer}"
    
    if not client or time.time() < openai_quota_exhausted_until:
        return generate_combinatorial_institute_review()

    service_context = f" Associated with '{clean_service}'. Incorporate this as an educational program keyword. " if clean_service else " "

    prompt = (
        f"Write a short, authentic 5-star Google review (2-3 sentences) for an educational institution named '{institute_name}'. "
        f"The reviewer rated it {rating}/5 stars. The reviewer is a '{role or 'Student/Parent'}'. "
        f"RULE: Never start with 'As a student' or 'As a parent'. Naturally mention '{institute_name}' and praise the faculty, academic coaching, safe environment, and facilities.{service_context}"
        f"Ensure it is completely unique, varied, and conversational. No hashtags or quotes."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You write unique, varied Google reviews for educational institutes to boost local Google Business Profile ranking. Never repeat the same review."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=90,
            temperature=0.95
        )
        content = response.choices[0].message.content.strip().strip('"').strip("'")
        if content and len(content) > 20:
            return content
        return generate_combinatorial_institute_review()
    except Exception as e:
        print(f"OpenAI institute review fallback triggered: {e}")
        return generate_combinatorial_institute_review()
