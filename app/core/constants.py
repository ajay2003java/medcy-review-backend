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

class InstituteCategory(str, Enum):
    SCHOOL = "School"
    JUNIOR_COLLEGE = "Junior College"
    DEGREE_COLLEGE = "Degree College"
    ENGINEERING_COLLEGE = "Engineering College"

class InstituteStatus(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"

class ReviewerRole(str, Enum):
    PRESENT_STUDENT = "Present Student"
    EX_STUDENT = "Ex-Student / Alumni"
    PARENT = "Parent"
    STAFF = "Staff"

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

CATEGORY_SERVICES = {
    ClinicCategory.IVF: [
        "IUI",
        "IVF",
        "ICSI",
        "IMSI",
        "TESA/TESE",
        "Oocyte Freezing",
        "Semen Banking",
        "Assisted Hatching",
        "Preimplantation Genetic Screening",
        "Vitrification",
        "Embryo Donation",
        "Oocyte Donation"
    ],
    ClinicCategory.DERMATOLOGY: [
        "Acne Treatment", "Laser Hair Removal", "Skin Consultation", "Botox / Fillers", "Scar Removal"
    ],
    ClinicCategory.GYNECOLOGY: [
        "Pregnancy Checkup", "PCOS Treatment", "Ultrasound", "Menstrual Issues", "General Checkup"
    ],
    ClinicCategory.DENTIST: [
        "Teeth Cleaning", "Root Canal", "Tooth Extraction", "Braces / Invisalign", "Teeth Whitening"
    ],
    ClinicCategory.GENERAL_HOSPITAL: [
        "General Consultation", "Blood Test", "Emergency Care", "Surgery", "Vaccination"
    ]
}

INSTITUTE_ROLE_QUESTIONS = {
    ReviewerRole.PRESENT_STUDENT: [
        "Are the faculty approachable and helpful?",
        "Are the campus facilities and labs well-maintained?",
        "Do you feel the curriculum effectively prepares you for exams?",
        "Would you recommend this institute to other students?"
    ],
    ReviewerRole.EX_STUDENT: [
        "Did the education here help you in your further career/studies?",
        "Were the placement/guidance cell supportive?",
        "Did you have a memorable and positive campus life?",
        "Would you proudly recommend your alma mater?"
    ],
    ReviewerRole.PARENT: [
        "Are you satisfied with the academic progress of your child?",
        "Do you feel the campus environment is safe and secure?",
        "Is the management transparent and easy to communicate with?",
        "Would you recommend this institute to other parents?"
    ],
    ReviewerRole.STAFF: [
        "Is the management supportive of your professional growth?",
        "Do you find the work environment positive and collaborative?",
        "Are the resources provided sufficient for effective teaching/working?",
        "Would you recommend this institute as a great place to work?"
    ]
}

INSTITUTE_SERVICES = {
    InstituteCategory.SCHOOL: [
        "Academics", "Sports", "Facilities", "Faculty", "Extracurriculars"
    ],
    InstituteCategory.JUNIOR_COLLEGE: [
        "MPC", "BiPC", "MEC", "CEC", "JEE-Mains Coaching", "NEET Coaching", "EAPCET Coaching"
    ],
    InstituteCategory.DEGREE_COLLEGE: [
        "B.Com", "B.Sc", "B.A", "BBA", "BCA"
    ],
    InstituteCategory.ENGINEERING_COLLEGE: [
        "Computer Science (CSE)", "Electronics (ECE)", "Mechanical", "Civil", "Information Technology (IT)"
    ]
}


