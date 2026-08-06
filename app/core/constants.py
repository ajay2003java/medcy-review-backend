from enum import Enum

class ClinicCategory(str, Enum):
    IVF = "IVF"
    DERMATOLOGY = "Dermatology"
    GYNECOLOGY = "Gynecology"
    DENTIST = "Dentist"
    GENERAL_HOSPITAL = "General Hospital"

class ClinicStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"

CATEGORY_QUESTIONS = {
    ClinicCategory.IVF: [
        "How would you rate the care and support provided by our fertility specialists?",
        "Were our staff empathetic and clear about your treatment options?",
        "Did you feel comfortable asking questions during your consultation?",
        "How would you rate the facility's cleanliness and privacy?"
    ],
    ClinicCategory.DERMATOLOGY: [
        "How satisfied are you with your consultation and skin treatment plan?",
        "Did the doctor explain the procedures and expected outcomes clearly?",
        "Was the clinic environment welcoming and hygienic?",
        "Did you experience any issues scheduling your appointment?"
    ],
    ClinicCategory.GYNECOLOGY: [
        "How would you rate the comfort and privacy during your visit?",
        "Did the doctor address all your concerns regarding women's health?",
        "Was the nursing staff supportive and gentle?",
        "How would you rate the overall facility?"
    ],
    ClinicCategory.DENTIST: [
        "How comfortable and pain-free was your dental procedure?",
        "Was the clinic environment clean and welcoming?",
        "Did the dentist explain the treatment plan clearly?",
        "How would you rate our front-desk service?"
    ],
    ClinicCategory.GENERAL_HOSPITAL: [
        "How would you rate the overall facility and waiting times?",
        "Did you feel well taken care of by the nursing and medical staff?",
        "Was the admission/discharge process smooth?",
        "How would you rate the cleanliness of the hospital?"
    ]
}
