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
        "Did you feel fully supported by our fertility specialists during your visit?",
        "Were our staff empathetic and clear about your treatment options?",
        "Did you feel comfortable asking questions during your consultation?",
        "Was the facility clean, private, and comfortable for you?"
    ],
    ClinicCategory.DERMATOLOGY: [
        "Were you satisfied with your consultation and skin treatment plan?",
        "Did the doctor explain the procedures and expected outcomes clearly?",
        "Was the clinic environment welcoming and hygienic?",
        "Was it easy to schedule and check-in for your appointment?"
    ],
    ClinicCategory.GYNECOLOGY: [
        "Did you feel that your privacy and comfort were respected during your visit?",
        "Did the doctor address all your concerns regarding women's health?",
        "Was the nursing staff supportive and gentle?",
        "Would you recommend our facility to your friends and family?"
    ],
    ClinicCategory.DENTIST: [
        "Did the dentist make sure you were comfortable during the procedure?",
        "Was the clinic environment clean and welcoming?",
        "Did the dentist explain the treatment plan clearly?",
        "Were our front-desk staff polite and helpful?"
    ],
    ClinicCategory.GENERAL_HOSPITAL: [
        "Were you seen by a doctor within a reasonable waiting time?",
        "Did you feel well taken care of by the nursing and medical staff?",
        "Was the admission and discharge process smooth?",
        "Did you find the hospital rooms and facilities completely clean?"
    ]
}
