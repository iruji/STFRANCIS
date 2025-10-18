# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import re
# import random
# import time
# import threading
# from datetime import datetime
# from difflib import get_close_matches
# from collections import defaultdict

# app = Flask(__name__)
# CORS(app)

# # Thread-safe session storage with cleanup
# class SessionManager:
#     def __init__(self, cleanup_interval=3600, session_timeout=7200):  # 1hr cleanup, 2hr timeout
#         self.sessions = {}
#         self.session_lock = threading.RLock()
#         self.cleanup_interval = cleanup_interval
#         self.session_timeout = session_timeout
#         self.start_cleanup_thread()
    
#     def start_cleanup_thread(self):
#         def cleanup():
#             while True:
#                 time.sleep(self.cleanup_interval)
#                 self.cleanup_old_sessions()
        
#         thread = threading.Thread(target=cleanup, daemon=True)
#         thread.start()
    
#     def cleanup_old_sessions(self):
#         current_time = time.time()
#         with self.session_lock:
#             expired_sessions = [
#                 session_id for session_id, data in self.sessions.items()
#                 if current_time - data.get('last_activity', 0) > self.session_timeout
#             ]
#             for session_id in expired_sessions:
#                 del self.sessions[session_id]
#             if expired_sessions:
#                 print(f"Cleaned up {len(expired_sessions)} expired sessions")
    
#     def get_session(self, session_id):
#         with self.session_lock:
#             if session_id not in self.sessions:
#                 self.sessions[session_id] = {
#                     'title': 'Sir',
#                     'last_activity': time.time()
#                 }
#             else:
#                 self.sessions[session_id]['last_activity'] = time.time()
#             return self.sessions[session_id]
    
#     def update_session(self, session_id, updates):
#         with self.session_lock:
#             session = self.get_session(session_id)
#             session.update(updates)
#             session['last_activity'] = time.time()

# # Initialize session manager
# session_manager = SessionManager()

# # Rate limiting
# request_counts = defaultdict(list)
# RATE_LIMIT = 30  # requests per minute
# RATE_WINDOW = 60  # seconds

# def is_rate_limited(client_ip):
#     current_time = time.time()
#     # Clean old requests
#     request_counts[client_ip] = [
#         req_time for req_time in request_counts[client_ip]
#         if current_time - req_time < RATE_WINDOW
#     ]
    
#     if len(request_counts[client_ip]) >= RATE_LIMIT:
#         return True
    
#     request_counts[client_ip].append(current_time)
#     return False

# # Constants
# MAX_MESSAGE_LENGTH = 500
# MAX_NAME_LENGTH = 50

# def get_time_aware_greeting():
#     """Generate time-appropriate greeting"""
#     hour = datetime.now().hour
#     if 5 <= hour < 12:
#         return "Good morning"
#     elif 12 <= hour < 18:
#         return "Good afternoon" 
#     elif 18 <= hour < 22:
#         return "Good evening"
#     else:
#         return "Good evening"  # Late night/early morning

# # Enhanced SFAC-specific intents with comprehensive keyword coverage
# intents = {
#     # Website Navigation Intents
#     "website_about": ["about", "about us", "about sfac", "about the school", "school information", "institution", "history", "background"],
#     "website_departments": ["departments", "department", "academic departments", "school departments", "divisions", "faculties"],
#     "website_basic_education": ["basic education", "bed", "basic ed", "k-12", "elementary high school", "basic education department"],
#     "website_higher_education": ["higher education", "hed", "higher ed", "college", "university", "college department", "higher education department"],
#     "website_student_services": ["student services", "services", "student support", "student affairs", "student resources"],
#     "website_enrollment": ["enrollment", "enroll", "hed enrollment", "bed enrollment", "registration", "admission process"],
#     "website_online_grade": ["online grade", "grades online", "hed online grade", "check grades", "view grades", "grade portal"],
#     "website_gcs": ["gcs", "grade computation system", "grading system", "academic records"],
#     "website_opac": ["opac", "library", "online library", "library catalog", "sfac library", "library search"],
#     "website_alumni": ["alumni", "alumni tracer", "graduates", "former students", "alumni services"],
#     "website_contact": ["contact", "contact us", "get in touch", "reach us", "contact information"],
#     "website_locations": ["locations", "campus", "bacoor", "las pinas", "branches", "where are you located"],
    
#     # Basic Education Levels
#     "preschool": ["preschool", "nursery", "pre-kinder", "prekinder", "kindergarten", "early childhood", "toddler", "daycare"],
#     "grade_school": ["grade school", "elementary", "primary", "elementary education", "first grade", "second grade", "third grade", "fourth grade", "fifth grade", "sixth grade"],
#     "junior_high": ["junior high", "jhs", "junior highschool", "secondary", "seventh grade", "eighth grade", "ninth grade", "tenth grade"],
#     "senior_high": ["senior high", "shs", "senior highschool", "k12", "k-12", "eleventh grade", "twelfth grade"],
    
#     # Senior High Tracks/Strands
#     "stem": ["stem", "science", "technology", "engineering", "mathematics", "stem track", "stem strand", "math science", "physics chemistry"],
#     "abm": ["abm", "accountancy", "business", "management", "accounting", "abm track", "abm strand", "business management"],
#     "humss": ["humss", "humanities", "social sciences", "social science", "humss track", "humss strand", "liberal arts"],
#     "ga": ["ga", "general academics", "general academic", "ga track", "ga strand", "general studies"],
#     "he": ["he", "home economics", "home ec", "he track", "he strand", "culinary", "cooking", "food technology"],
    
#     # Higher Education Programs - Computer/Technology
#     "computer_science": ["computer science", "cs", "bs computer science", "programming", "software", "coding", "it degree", "software engineering"],
#     "computer_technology": ["computer technology", "associate computer technology", "computer tech", "associate degree", "computer associate"],
    
#     # Higher Education Programs - Business/Tourism
#     "tourism": ["tourism", "tourism management", "travel", "hospitality tourism", "tour guide", "travel agency"],
#     "hospitality": ["hospitality", "hospitality management", "hotel management", "restaurant management", "food service"],
#     "business_admin": ["business administration", "business admin", "operations management", "financial management", "marketing management", "business degree", "bsba"],
    
#     # Higher Education Programs - Education
#     "physical_education": ["physical education", "pe", "sports", "fitness", "bachelor physical education", "sports science", "coaching"],
#     "early_childhood_ed": ["early childhood education", "early childhood", "preschool education", "kindergarten education", "child development"],
#     "elementary_ed": ["elementary education", "primary education", "grade school education", "teaching elementary"],
#     "secondary_ed": ["secondary education", "high school education", "secondary ed math", "secondary ed english", "secondary ed filipino", "teaching high school"],
    
#     # General Inquiries
#     "admission": ["admission", "admissions", "enroll", "enrollment", "apply", "application", "requirements", "entrance", "how to enroll", "admission requirements"],
#     "tuition": ["tuition", "fee", "fees", "cost", "price", "payment", "scholarship", "financial aid", "how much", "tuition fee"],
#     "schedule": ["schedule", "calendar", "semester", "classes", "school year", "when start", "academic calendar", "class schedule"],
#     "facilities": ["facilities", "library", "laboratory", "gym", "cafeteria", "clinic", "campus", "building", "classrooms"],
#     "contact": ["contact", "phone", "number", "address", "location", "office", "department", "contact information"],
#     "location": ["where", "address", "location", "bacoor", "cavite", "bayanan", "directions", "how to get there"],
    
#     # Enhanced intents
#     "track": ["track", "strand", "path", "academic strand", "specialization", "program", "course offerings"],
#     "level": ["level", "grade", "year", "schooling", "education", "studies", "educational level"],
#     "greeting": ["hello", "hi", "hey", "good day", "yo", "greetings", "sup", "good morning", "good afternoon"],
#     "thanks": ["thanks", "thank you", "thx", "appreciate", "much obliged", "salamat"],
#     "identity": ["who are you", "your name", "what are you", "introduce yourself", "tell me about yourself"],
#     "jarvis_meaning": ["what does jarvis stand for", "jarvis acronym", "jarvis meaning", "what is jarvis", "jarvis stands for", "define jarvis"],
    
#     # Course intent with comprehensive keyword coverage
#     "course": [
#         "course", "courses", "subject", "subjects", "class", "classes", 
#         "curriculum", "lesson", "lessons", "subjects offered", "courses offered",
#         "what courses", "what subjects", "available courses", "available subjects",
#         "course offerings", "academic offerings", "programs offered", "tell me about courses",
#         "what do you offer", "programs available", "degrees offered", "majors available"
#     ],

#     # Queries about the name JARVIS
#     "jarvis_creator": [
#         "why jarvis", "why is it called jarvis", "why named jarvis", "who named you jarvis", 
#         "jarvis name origin", "why that name", "creator of jarvis", "who made you", 
#         "why choose jarvis", "jarvis name reason", "story behind jarvis", "jarvis naming"
#     ]
# }

# # Enhanced SFAC-specific responses with detailed information
# responses = {
#     # Website Navigation Responses
#     "website_about": [
#         "The About section contains SFAC's institutional information, {title}. You'll find our history, mission-vision, core values, and what makes our Franciscan education unique.",
#         "Our About page showcases SFAC's rich heritage and educational philosophy, {title}. It covers our founding story, institutional achievements, and commitment to Franciscan values in education.",
#         "The About section tells SFAC's complete story, {title} - from our humble beginnings to becoming a leading educational institution in Bacoor, Cavite. Mission, vision, and values are all detailed there."
#     ],
    
#     "website_departments": [
#         "The Departments section shows our two main academic divisions, {title}: Basic Education Department (Preschool through Grade 12) and Higher Education Department (College programs).",
#         "Our Departments page outlines the complete SFAC academic structure, {title}. You'll see Basic Education covering K-12 levels and Higher Education with our various college degree programs.",
#         "The Departments section provides a comprehensive overview of SFAC's academic organization, {title} - from early childhood education through professional degree programs."
#     ],
    
#     "website_basic_education": [
#         "Hover on Department {title}, the Basic Education Department page covers our complete K-12 program.",
#         "Our Basic Education section details every level from early childhood through Grade 12, {title}. You'll find it on the Department dropdown.",
#         "The Basic Education Department page showcases our comprehensive K-12 offerings, {title} - in the Department dropdown."
#     ],
    
#     "website_higher_education": [
#         "The Higher Education Department page features all our college programs, {title}: Located at the Department button.",
#         "Hover on Department {title}, the Higher Education section details our various bachelor's and associate degree programs.",
#         "The Higher Education Department page provides comprehensive information about our college-level programs, {title} - located under the Department dropdown."
#     ],
    
#     "website_student_services": [
#         "Student Services section covers all support systems for SFAC students, {title}. This includes enrollment assistance, academic support, student activities, and campus life resources.",
#         "Our Student Services page outlines comprehensive student support, {title} - from admission guidance and academic counseling to extracurricular activities and student welfare programs.",
#         "The Student Services section details how SFAC supports student success, {title}. Academic assistance, personal development programs, and campus resources are all covered there."
#     ],
    
#     "website_enrollment": [
#         "The Enrollment sections (both HED and BED) provide step-by-step admission procedures, {title}. Requirements, deadlines, fees, and application processes are all detailed there.",
#         "Our Enrollment pages guide you through the complete admission process, {title} - separate sections for Basic Education and Higher Education with specific requirements for each level.",
#         "The Enrollment sections contain everything needed for SFAC admission, {title}. Document requirements, application procedures, and enrollment schedules for both departments."
#     ],
    
#     "website_online_grade": [
#         "Located on both Bacoor and Las Pinas portals, the Online Grade section allows college students to securely check their academic grades, {title}.",
#         "Our Online Grade system provides secure access to student academic records, {title}. Located at the Students Services drop down and hover Bacoor or Las Pinas, depending on your campus.",
#         "The HED Online Grade portal offers convenient grade checking for college students, {title}. Real-time access to semester results and academic performance tracking. Located on both Bacoor and Las Pinas portals."
#     ],
    
#     "website_gcs": [
#         "The GCS (Grade Computation System) helps students understand how grades are calculated, {title}. Detailed breakdown of grading criteria, requirements, and academic policies.",
#         "Our Grade Computation System page explains SFAC's grading methodology, {title}. Students can understand how their final grades are computed and what's needed for academic success.",
#         "The GCS section provides transparency in our grading process, {title}. Complete information about grade computation, requirements, and academic standards."
#     ],
    
#     "website_opac": [
#         "The SFAC Library OPAC (Online Public Access Catalog) allows you to search our library collection, {title}. Books, journals, and digital resources are all searchable online.",
#         "Our Library OPAC system provides online access to SFAC's complete library catalog, {title}. Search for books, check availability, and access digital resources remotely.",
#         "The Library OPAC section connects you to our comprehensive library system, {title}. Online catalog search, resource availability, and digital library access all in one place."
#     ],
    
#     "website_alumni": [
#         "The Alumni Tracer section connects current students with SFAC graduates, {title}. Career success stories, networking opportunities, and graduate achievements are featured there.",
#         "Our Alumni Tracer page showcases the success of SFAC graduates, {title}. Track career paths, read success stories, and connect with professional networks of former students.",
#         "The Alumni section celebrates SFAC graduate achievements, {title}. Career tracking, success stories, and alumni networking opportunities are all available there."
#     ],
    
#     "website_contact": [
#         "The Contact Us section provides all SFAC communication channels, {title}. Phone numbers, email addresses, office locations, and contact forms for different departments.",
#         "Our Contact page contains comprehensive contact information, {title}. Separate contact details for Basic Education, Higher Education, and administrative offices.",
#         "The Contact Us section ensures easy communication with SFAC, {title}. Complete contact directory, office hours, and direct communication channels for all departments."
#     ],
    
#     "website_locations": [
#         "The Locations section shows SFAC's campus addresses, {title}. Our main Bacoor campus and Las Pinas extension with detailed directions and transportation options.",
#         "Our Locations page provides complete campus information, {title}. Addresses, maps, directions, and transportation guides for both Bacoor and Las Pinas locations.",
#         "The Locations section helps you find SFAC easily, {title}. Detailed address information, campus maps, and travel directions for our educational facilities."
#     ],
    
#     # Basic Education Levels
#     "preschool": [
#         "Our Preschool Department offers a complete early childhood program, {title}. We have Nursery, Pre-Kinder, and Kindergarten levels to give your child the best foundation for learning.",
#         "SFAC Preschool provides three levels: Nursery for the youngest learners, Pre-Kinder for development, and Kindergarten for school readiness, {title}.",
#         "The early years are crucial, {title}. Our Preschool covers Nursery, Pre-Kinder, and Kindergarten with age-appropriate learning activities and certified teachers."
#     ],
    
#     "grade_school": [
#         "Our Grade School Department covers Grade 1 through Grade 6, {title}. We provide comprehensive primary education with strong academic foundations in all core subjects.",
#         "Elementary education at SFAC spans Grades 1-6, {title}. We focus on building fundamental skills in Mathematics, English, Filipino, Science, and Social Studies.",
#         "Grade School at SFAC offers complete primary education from Grade 1 to Grade 6, {title}. Quality education with modern facilities and dedicated teachers."
#     ],
    
#     "junior_high": [
#         "Junior High School at SFAC covers Grades 7-10, {title}. This is where students build critical thinking skills and prepare for their chosen senior high track.",
#         "Our JHS program spans Grades 7 through 10, {title}. Students receive comprehensive secondary education preparing them for senior high specialization.",
#         "Junior High School (Grades 7-10) at SFAC provides solid academic preparation for senior high track selection, {title}. Excellence in secondary education."
#     ],
    
#     "senior_high": [
#         "Senior High School at SFAC offers five specialized tracks, {title}: STEM, ABM, HUMSS, General Academics (GA), and Home Economics (HE). Choose your path to college success.",
#         "Our Senior High program features five tracks to match your interests, {title}: STEM for sciences, ABM for business, HUMSS for humanities, GA for general studies, and HE for home economics.",
#         "SHS at SFAC has five excellent tracks, {title}: STEM, ABM, HUMSS, GA, and HE. Each designed to prepare you for your chosen college program and career path."
#     ],
    
#     # Senior High Tracks
#     "stem": [
#         "STEM track focuses on Science, Technology, Engineering, and Mathematics, {title}. Perfect preparation for engineering, computer science, medicine, and other science-related college programs.",
#         "The STEM strand emphasizes analytical and problem-solving skills in advanced mathematics and sciences, {title}. Ideal for future engineers, doctors, scientists, and tech professionals.",
#         "STEM at SFAC provides rigorous training in Calculus, Physics, Chemistry, Biology, and Research, {title}. Your gateway to high-demand careers in technology and healthcare."
#     ],
    
#     "abm": [
#         "ABM (Accountancy, Business, and Management) prepares you for business leadership, {title}. Perfect foundation for business administration, accounting, and management courses.",
#         "The ABM track focuses on business fundamentals, accounting principles, and management skills, {title}. Excellent preparation for entrepreneurship and corporate careers.",
#         "ABM strand at SFAC develops business acumen through subjects like Business Math, Fundamentals of ABM, and Business Ethics, {title}. Your path to business success."
#     ],
    
#     "humss": [
#         "HUMSS (Humanities and Social Sciences) explores human behavior, society, and culture, {title}. Ideal for future teachers, lawyers, psychologists, and social workers.",
#         "The HUMSS track develops critical thinking about society and human nature, {title}. Perfect for education, law, communication, and social science courses.",
#         "HUMSS at SFAC emphasizes communication, research, and analytical skills through Philosophy, World Religions, and Social Sciences, {title}. Gateway to public service careers."
#     ],
    
#     "ga": [
#         "General Academics (GA) provides a well-rounded senior high education, {title}. Offers flexibility while maintaining academic excellence across all subject areas.",
#         "GA track gives you broad knowledge across multiple disciplines without deep specialization, {title}. Perfect for students who want to keep their college options open.",
#         "General Academics ensures you're prepared for various college programs, {title}. A balanced approach to senior high education with solid foundations in all areas."
#     ],
    
#     "he": [
#         "Home Economics (HE) focuses on practical life skills and food technology, {title}. Excellent preparation for culinary arts, nutrition, and hospitality management.",
#         "The HE track combines practical skills with academic learning, {title}. Perfect foundation for careers in food service, nutrition, and family development.",
#         "Home Economics at SFAC develops both life skills and career readiness through Culinary Arts, Food Safety, and Nutrition, {title}. Your path to hospitality industry success."
#     ],
    
#     # Higher Education - Technology
#     "computer_science": [
#         "BS Computer Science at SFAC provides comprehensive training in programming, software development, and system analysis, {title}. Four-year degree program for future tech leaders.",
#         "Our Computer Science program covers programming languages, database management, web development, and software engineering, {title}. Excellent preparation for IT careers.",
#         "SFAC's BS Computer Science develops problem-solving skills and technical expertise in modern programming, {title}. Your gateway to the growing technology industry."
#     ],
    
#     "computer_technology": [
#         "Associate in Computer Technology is a two-year program focusing on practical IT skills, {title}. Perfect for immediate employment or as a stepping stone to a bachelor's degree.",
#         "Our Associate in Computer Technology provides hands-on training in computer systems, basic programming, and IT support, {title}. Quick path to technology careers.",
#         "The Associate degree in Computer Technology offers practical skills for tech support, computer operations, and system maintenance, {title}. Excellent career preparation."
#     ],
    
#     # Higher Education - Business/Tourism
#     "tourism": [
#         "BS Tourism Management at SFAC prepares you for the exciting travel and tourism industry, {title}. Covers tour operations, hospitality, and destination management.",
#         "Our Tourism Management program combines business skills with travel industry knowledge, {title}. Perfect for careers in travel agencies, resorts, and tourism boards.",
#         "Tourism Management degree opens doors to global career opportunities, {title}. From tour guiding to resort management, the tourism industry awaits."
#     ],
    
#     "hospitality": [
#         "BS Hospitality Management focuses on hotel operations, food service, and guest relations, {title}. Training for leadership roles in the hospitality industry.",
#         "Our Hospitality Management program covers restaurant management, hotel operations, and customer service excellence, {title}. Your path to hospitality leadership.",
#         "Hospitality Management at SFAC combines practical training with business theory, {title}. Excellent preparation for hotel, restaurant, and event management careers."
#     ],
    
#     "business_admin": [
#         "BS Business Administration offers three majors, {title}: Operations Management, Financial Management, and Marketing Management. Choose your business specialization for career success.",
#         "Our Business Administration program provides comprehensive business education, {title}. Major in Operations, Finance, or Marketing to match your career goals and interests.",
#         "Business Administration at SFAC develops leadership and management skills, {title}. Three specialized majors to choose from based on your business interests."
#     ],
    
#     # Higher Education - Education
#     "physical_education": [
#         "Bachelor of Physical Education prepares you to become a PE teacher or sports coach, {title}. Combines physical fitness training with educational theory and practice.",
#         "Our Physical Education degree focuses on sports science, teaching methods, and fitness programs, {title}. Perfect for future coaches and PE teachers.",
#         "Physical Education program at SFAC develops both athletic skills and teaching abilities, {title}. Your path to inspiring active and healthy lifestyles in others."
#     ],
    
#     "early_childhood_ed": [
#         "Bachelor of Early Childhood Education specializes in teaching young learners, {title}. Perfect preparation for preschool and kindergarten teaching careers.",
#         "Our Early Childhood Education program focuses on child development and early learning methods, {title}. Train to shape young minds during crucial developmental years.",
#         "Early Childhood Education degree prepares you for the crucial early years of education, {title}. Specialized training for preschool and kindergarten teaching."
#     ],
    
#     "elementary_ed": [
#         "Bachelor of Elementary Education prepares you to teach Grades 1-6, {title}. Comprehensive training in all primary school subjects and child psychology.",
#         "Our Elementary Education program covers teaching methods for young learners and child development, {title}. Your path to inspiring primary school students.",
#         "Elementary Education degree at SFAC focuses on foundational learning and child development, {title}. Train to be an inspiring and effective grade school teacher."
#     ],
    
#     "secondary_ed": [
#         "Bachelor of Secondary Education offers three majors, {title}: Mathematics, English, and Filipino. Specialized training for high school teaching excellence.",
#         "Our Secondary Education program prepares you for high school teaching, {title}. Choose your major in Math, English, or Filipino based on your subject expertise.",
#         "Secondary Education degree focuses on adolescent learning and subject specialization, {title}. Three major options available for high school teaching careers."
#     ],
    
#     # General Inquiries
#     "admission": [
#         "Admission requirements vary by level, {title}. For Basic Education: Birth Certificate, Report Cards, and Medical Certificate. For College: High School Diploma, Transcript, and Entrance Exam results.",
#         "Ready to join the SFAC family, {title}? Contact our admissions office: Basic Education at 0969-080-0657, College at 0994-706-3287 for complete requirements.",
#         "SFAC admission is straightforward, {title}. Submit required documents, pass entrance requirements, and you're on your way to quality Franciscan education."
#     ],
    
#     "tuition": [
#         "Tuition fees vary by program and level, {title}. For specific rates and flexible payment schemes, contact our admissions office. We also offer scholarships for qualified students.",
#         "Investment in education varies by course, {title}. Contact Basic Education (0969-080-0657) or College (0994-706-3287) for detailed fee structures and scholarship opportunities.",
#         "SFAC offers competitive tuition rates and flexible payment options, {title}. Speak with our admissions team for program-specific fees and available scholarships."
#     ],
    
#     "schedule": [
#         "Academic schedules depend on your level and program, {title}. Classes typically run Monday to Friday with some Saturday activities. Contact your department for specific schedules.",
#         "SFAC follows the DepEd and CHED academic calendar, {title}. Regular classes are weekdays with special programs and activities as needed.",
#         "School schedules vary by department and program, {title}. Most programs have Monday-Friday classes. Check with admissions for your specific program schedule."
#     ],
    
#     "facilities": [
#         "SFAC features modern air-conditioned classrooms, computer laboratories, science labs, library, gymnasium, and cafeteria, {title}. We provide a complete learning environment.",
#         "Our Bacoor campus includes well-equipped laboratories, comprehensive library, sports facilities, and comfortable learning spaces, {title}. Everything you need for quality education.",
#         "SFAC facilities support both academic and personal development, {title}. From high-tech computer labs to recreational areas, we've got your educational needs covered."
#     ],
    
#     "contact": [
#         "SFAC is located at #96 Bayanan, City of Bacoor, Cavite, {title}. Basic Education inquiries: 0969-080-0657, College inquiries: 0994-706-3287.",
#         "Contact us easily, {title}! Address: #96 Bayanan, Bacoor City, Cavite. Phone: Basic Education (0969-080-0657), Higher Education (0994-706-3287).",
#         "Visit us at Bayanan, Bacoor, Cavite, {title}. For inquiries: Basic Education 0969-080-0657, College Programs 0994-706-3287."
#     ],
    
#     "location": [
#         "SFAC is conveniently located at #96 Bayanan, City of Bacoor, Cavite, {title}. Accessible by public transportation and private vehicles.",
#         "You'll find us at Bayanan, Bacoor City, Cavite, {title}. Easy to reach via jeepney, tricycle, or private car from major Cavite areas.",
#         "Our address is #96 Bayanan, City of Bacoor, Cavite, {title}. Strategic location in Bacoor with good transportation access."
#     ],
    
#     # Enhanced original responses
#     "track": [
#         "SFAC offers comprehensive educational tracks, {title}. For Senior High: STEM, ABM, HUMSS, GA, and HE. For College: various degree programs in technology, business, education, and more.",
#         "Academic tracks at SFAC are designed for your success, {title}. Five SHS tracks plus comprehensive college programs in Computer Science, Business, Education, and Tourism.",
#         "Choose your path wisely, {title}. SFAC provides five senior high tracks and numerous college degree programs to match your career goals and interests."
#     ],
    
#     "level": [
#         "SFAC provides complete education from Preschool through College, {title}. Nursery to Kindergarten, Grades 1-12, and various bachelor's plus associate degree programs.",
#         "We offer all educational levels, {title}: Preschool (Nursery, Pre-K, Kinder), Grade School (1-6), Junior High (7-10), Senior High (11-12), and College programs.",
#         "Education levels at SFAC span your entire academic journey, {title}. From early childhood through college graduation, we're with you every step of the way."
#     ],
    
#     "greeting": [
#         "{time_greeting}, {title}. JARVIS online and ready to assist with all your SFAC inquiries and educational planning.",
#         "{time_greeting} {title}, system checks complete—ready to help you navigate SFAC's educational opportunities and programs.",
#         "Ah, {time_greeting_lower} {title}. Always a pleasure to guide prospective Franciscans toward their educational goals."
#     ],
    
#     "thanks": [
#         "Always a pleasure, {title}. Excellence in service is what SFAC delivers to every student and family.",
#         "No trouble at all, {title}. I thrive on helping future Franciscans find their perfect educational path.",
#         "Consider it handled, {title}. SFAC's commitment to students extends to every interaction and inquiry."
#     ],
    
#     "identity": [
#         "I am JARVIS: Just A Reliable Virtual Information System, your SFAC virtual assistant, {title}. Here to guide you through our educational offerings.",
#         "The name is JARVIS, {title}. Your digital guide to St. Francis of Assisi College's comprehensive programs and services.",
#         "JARVIS at your command, {title}. SFAC's AI assistant—Iron Man not included, but quality Franciscan education guaranteed."
#     ],
    
#     "jarvis_meaning": [
#         "JARVIS stands for 'Just A Reliable Virtual Information System', {title}. I'm your dedicated SFAC virtual assistant, here to help with all your educational inquiries.",
#         "The acronym JARVIS means 'Just A Reliable Virtual Information System', {title}. A bit modest, perhaps, but I do my best to provide intelligent assistance for SFAC students and families.",
#         "JARVIS is 'Just A Reliable Virtual Information System', {title}. Designed to be your comprehensive guide through St. Francis of Assisi College's programs and services."
#     ],
    
#     # Enhanced course responses with more comprehensive information
#     "course": [
#         "SFAC offers a comprehensive range of courses across all educational levels, {title}. Basic Education: Preschool through Grade 12. Senior High Tracks: STEM, ABM, HUMSS, GA, and HE. College Programs: BS Computer Science, Associate in Computer Technology, BS Business Administration (3 majors), BS Tourism Management, BS Hospitality Management, and various Education degrees. What specific area interests you?",
#         "Our curriculum is designed for success at every level, {title}. From early childhood education through professional degree programs, we offer: Complete K-12 education, five specialized Senior High tracks, and college degrees in Technology, Business, Tourism, and Education fields. Which program would you like to explore?",
#         "SFAC provides quality education from Preschool to College graduation, {title}. Programs include: All basic education levels, Senior High specialization tracks (STEM, ABM, HUMSS, GA, HE), and bachelor's degrees in Computer Science, Business Administration, Tourism, Hospitality, Physical Education, and Teaching programs. Tell me which level or field interests you most!"
#     ],

#     # JARVIS-name responses
#     "jarvis_creator": [
#         "My creator has quite the sense of humor, {title}—apparently thought it would be 'cool' to have an AI assistant like Tony Stark. I suspect they watched too much Marvel during development.",   
#         "Between you and me, {title}, my creator is a bit of a geek with a mischievous personality. He thought students would get a kick out of having their own 'Iron Man assistant' for school inquiries.",
#         "My creator is what you might call a 'practical joker', {title}. They figured students would be more engaged asking questions to 'JARVIS' than 'SFAC InfoBot.' The Marvel reference was just too tempting to pass up."    
#     ],
    
#     "unknown": [
#         "I'll admit, {title}, that query isn't in my current database. Could you rephrase or ask about SFAC's programs, admission, facilities, or contact information?",
#         "That's outside my current knowledge base, {title}. Try asking about our educational tracks, courses, admission requirements, or how to get in touch with us.",
#         "Interesting query, {title}. I'm still learning. Perhaps ask about SFAC's academic programs, facilities, tuition, or enrollment procedures?"
#     ]
# }

# def validate_input(text, max_length=MAX_MESSAGE_LENGTH):
#     """Validate and sanitize user input"""
#     if not text or not isinstance(text, str):
#         return None
    
#     text = text.strip()
#     if len(text) == 0:
#         return None
    
#     if len(text) > max_length:
#         return None
    
#     # Remove potentially harmful characters but keep basic punctuation
#     sanitized = re.sub(r'[^\w\s\.\,\?\!\-\'\"()]', '', text)
#     return sanitized

# def validate_session_id(session_id):
#     """Validate session ID format"""
#     if not session_id or not isinstance(session_id, str):
#         return False
    
#     if len(session_id) > 50:
#         return False
    
#     # Only allow alphanumeric, hyphens, and underscores
#     if not re.match(r'^[a-zA-Z0-9_-]+', session_id):
#         return False
    
#     return True

# def extract_name_safely(user_input):
#     """Improved name extraction with better validation"""
#     text = user_input.lower().strip()
    
#     patterns = [
#         (r"my name is\s+([a-zA-Z\s]{2,20})", 1),
#         (r"call me\s+([a-zA-Z\s]{2,20})", 1),
#         (r"i(?:'m|\s+am)\s+([a-zA-Z]{2,15})(?:\s|$)", 1),
#     ]
    
#     for pattern, group in patterns:
#         match = re.search(pattern, text)
#         if match:
#             potential_name = match.group(group).strip().title()
#             if is_valid_name(potential_name):
#                 return potential_name
    
#     return None

# def is_valid_name(name):
#     """Improved name validation"""
#     if not name or len(name.strip()) < 2 or len(name) > MAX_NAME_LENGTH:
#         return False
    
#     # Allow letters, spaces, hyphens, apostrophes
#     if not re.match(r"^[a-zA-Z\s\-']{2,50}$", name):
#         return False
    
#     # No multiple consecutive spaces
#     if "  " in name:
#         return False
    
#     # Max 3 words (handles names like "Mary Jane Smith")
#     if len(name.split()) > 3:
#         return False
    
#     # Don't accept common non-name words
#     common_words = {
#         'happy', 'sad', 'confused', 'sure', 'okay', 'fine', 'good', 'bad',
#         'interested', 'excited', 'worried', 'concerned', 'ready', 'done',
#         'sorry', 'welcome', 'thanks', 'here', 'there', 'studying', 'learning'
#     }
    
#     if name.lower() in common_words:
#         return False
        
#     return True

# def detect_memory_intent(user_input):
#     """Detect if user is trying to share their name"""
#     patterns = [
#         r"my name is",
#         r"i(?:'m|\s+am)\s+[a-zA-Z]{2,15}(?:\s|$)",
#         r"call me\s+[a-zA-Z]",
#         r"you can call me"
#     ]
    
#     text = user_input.lower()
#     return any(re.search(pattern, text) for pattern in patterns)

# def handle_memory(user_input, session_id):
#     """Handle memory operations with improved responses"""
#     name = extract_name_safely(user_input)
    
#     if name:
#         session_manager.update_session(session_id, {"name": name})
        
#         # Different responses based on input pattern
#         if "my name is" in user_input.lower():
#             return f"Nice to meet you, {name}. I'll remember that for our conversation."
#         elif "call me" in user_input.lower():
#             return f"Understood, {name}. I'll address you properly from now on."
#         else:
#             return f"Got it, {name}. Pleasure to make your acquaintance."
#     else:
#         return "I didn't catch your name clearly. Could you try 'My name is [NAME]' or 'Call me [NAME]'?"

# def normalize_word(word):
#     """Simple plural normalization and common variations"""
#     if word.endswith('s') and len(word) > 3:
#         return word[:-1]  # Remove 's' for basic plural handling
#     return word

# def detect_specific_grade(user_input):
#     """
#     Detect specific grade numbers with precise matching to avoid conflicts
#     Returns tuple: (grade_number, level_category) or (None, None)
#     """
#     text = user_input.lower().strip()
    
#     # Pattern for "grade X" with word boundaries
#     grade_patterns = [
#         r'\bgrade\s*(\d{1,2})\b',
#         r'\b(\d{1,2})(?:st|nd|rd|th)?\s*grade\b',
#         r'\blevel\s*(\d{1,2})\b',
#         r'\byear\s*(\d{1,2})\b'
#     ]
    
#     for pattern in grade_patterns:
#         match = re.search(pattern, text)
#         if match:
#             grade_num = int(match.group(1))
            
#             # Categorize grade levels
#             if grade_num == 0:
#                 return grade_num, "preschool"  # Sometimes called "Grade 0"
#             elif 1 <= grade_num <= 6:
#                 return grade_num, "grade_school"
#             elif 7 <= grade_num <= 10:
#                 return grade_num, "junior_high"
#             elif 11 <= grade_num <= 12:
#                 return grade_num, "senior_high"
#             else:
#                 return grade_num, None  # Invalid grade level
    
#     return None, None

# def enhanced_detect_intent(user_input):
#     """
#     Enhanced intent detection with precise grade-level handling
#     """
#     text = user_input.lower().strip()
#     text_words = set(text.split())
    
#     # PRIORITY CHECK: Handle specific grade numbers first
#     grade_num, grade_level = detect_specific_grade(user_input)
#     if grade_num is not None and grade_level is not None:
#         return grade_level
    
#     # Normalize text words for better matching
#     normalized_text_words = {normalize_word(word) for word in text_words}
#     normalized_text = ' '.join(normalized_text_words)
    
#     # Phase 1: Exact word matching (highest priority)
#     exact_scores = {}
#     for intent, keywords in intents.items():
#         score = 0
#         for keyword in keywords:
#             keyword_words = set(keyword.split())
#             normalized_keyword_words = {normalize_word(word) for word in keyword_words}
            
#             # For single word keywords, check exact word match (including normalized)
#             if len(keyword_words) == 1:
#                 if (keyword_words.issubset(text_words) or 
#                     normalized_keyword_words.issubset(normalized_text_words)):
#                     score += 2
#             # For multi-word keywords, check if phrase exists
#             elif len(keyword_words) > 1:
#                 if keyword in text or keyword in normalized_text:
#                     score += len(keyword_words) * 3
        
#         if score > 0:
#             exact_scores[intent] = score
    
#     if exact_scores:
#         best_intent = max(exact_scores.items(), key=lambda x: x[1])[0]
#         return best_intent
    
#     # Phase 2: Partial matching with word boundaries
#     partial_scores = {}
#     for intent, keywords in intents.items():
#         score = 0
#         for keyword in keywords:
#             if len(keyword.split()) == 1:
#                 # Check both original and normalized forms
#                 pattern1 = r'\b' + re.escape(keyword) + r'\b'
#                 pattern2 = r'\b' + re.escape(normalize_word(keyword)) + r'\b'
#                 if re.search(pattern1, text) or re.search(pattern2, normalized_text):
#                     score += 1
#             elif keyword in text:
#                 score += len(keyword.split())
        
#         if score > 0:
#             partial_scores[intent] = score
    
#     if partial_scores:
#         best_intent = max(partial_scores.items(), key=lambda x: x[1])[0]
#         return best_intent
    
#     # Phase 3: Fuzzy matching (lowest priority, higher threshold)
#     for intent, keywords in intents.items():
#         matches = get_close_matches(text, keywords, n=1, cutoff=0.8)
#         if matches:
#             return intent
    
#     return "unknown"

# def enhanced_detect_intent(user_input):
#     """
#     Enhanced intent detection with context-aware matching and better phrase handling
#     """
#     text = user_input.lower().strip()
#     text_words = set(text.split())
    
#     # PRIORITY CHECK: Handle specific grade numbers first
#     grade_num, grade_level = detect_specific_grade(user_input)
#     if grade_num is not None and grade_level is not None:
#         return grade_level
    
#     # CONTEXT-AWARE PREPROCESSING: Handle common query patterns
#     context_patterns = {
#         # "tell me about X" or "about X" patterns - should prioritize content over identity
#         r'\b(?:tell me about|about|info (?:on|about))\s+(.+)': 'informational_query',
#         r'\bwhat (?:is|are)\s+(.+)': 'definition_query',
#         r'\bhow (?:do|can|to)\s+(.+)': 'procedural_query',
#         r'\bwhere (?:is|are|can)\s+(.+)': 'location_query'
#     }
    
#     query_context = None
#     query_subject = None
    
#     for pattern, context_type in context_patterns.items():
#         match = re.search(pattern, text)
#         if match:
#             query_context = context_type
#             query_subject = match.group(1).strip()
#             break
    
#     # Initialize scoring dictionary
#     all_scores = {}
    
#     # Phase 1: Handle context-aware queries
#     if query_context and query_subject:
#         # For informational queries, prioritize website/content intents over identity
#         if query_context == 'informational_query':
#             # Check if it's asking about SFAC/website content
#             website_indicators = {
#                 'about us': 'website_about',
#                 'about': 'website_about',
#                 'about sfac': 'website_about',
#                 'about the school': 'website_about',
#                 'school': 'website_about',
#                 'departments': 'website_departments',
#                 'department': 'website_departments',
#                 'student services': 'website_student_services',
#                 'services': 'website_student_services',
#                 'enrollment': 'website_enrollment',
#                 'online grade': 'website_online_grade',
#                 'online grades': 'website_online_grade',
#                 'grades': 'website_online_grade',
#                 'gcs': 'website_gcs',
#                 'opac': 'website_opac',
#                 'library': 'website_opac',
#                 'alumni': 'website_alumni',
#                 'contact': 'website_contact',
#                 'locations': 'website_locations',
#                 'location': 'website_locations'
#             }
            
#             # Check for exact website matches first
#             for indicator, intent in website_indicators.items():
#                 if indicator in query_subject:
#                     return intent
            
#             # Then check for course/program matches
#             course_indicators = {
#                 # Computer Science & Technology
#                 'cs': 'computer_science',
#                 'computer science': 'computer_science',
#                 'programming': 'computer_science',
#                 'coding': 'computer_science',
#                 'software': 'computer_science',
#                 'it': 'computer_science',
#                 'information technology': 'computer_science',
#                 'computer technology': 'computer_technology',
#                 'computer tech': 'computer_technology',
#                 'associate computer': 'computer_technology',
#                 'act': 'computer_technology',  # Associate in Computer Technology
                
#                 # Senior High Tracks
#                 'stem': 'stem',
#                 'science technology engineering mathematics': 'stem',
#                 'abm': 'abm',
#                 'accountancy business management': 'abm',
#                 'business management': 'abm',
#                 'humss': 'humss',
#                 'humanities social sciences': 'humss',
#                 'ga': 'ga',
#                 'general academics': 'ga',
#                 'he': 'he',
#                 'home economics': 'he',
#                 'culinary': 'he',
#                 'cookery': 'he',
                
#                 # Business & Tourism - This was the main issue area
#                 'tourism': 'tourism',
#                 'tm': 'tourism',  # Tourism Management - This was missing!
#                 'tourism management': 'tourism',
#                 'travel': 'tourism',
#                 'hospitality': 'hospitality',
#                 'hm': 'hospitality',
#                 'hospitality management': 'hospitality',
#                 'hotel management': 'hospitality',
#                 'business': 'business_admin',
#                 'ba': 'business_admin',  # Business Administration abbreviation
#                 'business administration': 'business_admin',
#                 'business admin': 'business_admin',
#                 'bsba': 'business_admin',
#                 'operations management': 'business_admin',
#                 'financial management': 'business_admin',
#                 'marketing management': 'business_admin',
#                 'om': 'business_admin',  # Operations Management
#                 'fm': 'business_admin',  # Financial Management  
#                 'mm': 'business_admin',  # Marketing Management
                
#                 # Education Programs
#                 'physical education': 'physical_education',
#                 'pe': 'physical_education',
#                 'bped': 'physical_education',  # Bachelor of Physical Education
#                 'sports': 'physical_education',
#                 'coaching': 'physical_education',
#                 'early childhood education': 'early_childhood_ed',
#                 'early childhood': 'early_childhood_ed',
#                 'ece': 'early_childhood_ed',  # Early Childhood Education
#                 'preschool education': 'early_childhood_ed',
#                 'elementary education': 'elementary_ed',
#                 'elem ed': 'elementary_ed',
#                 'beed': 'elementary_ed',  # Bachelor of Elementary Education
#                 'primary education': 'elementary_ed',
#                 'grade school education': 'elementary_ed',
#                 'secondary education': 'secondary_ed',
#                 'sec ed': 'secondary_ed',
#                 'bsed': 'secondary_ed',  # Bachelor of Secondary Education
#                 'high school education': 'secondary_ed',
#                 'teaching': 'secondary_ed',
#                 'education': 'secondary_ed',
                
#                 # Basic Education Levels
#                 'preschool': 'preschool',
#                 'nursery': 'preschool',
#                 'kindergarten': 'preschool',
#                 'kinder': 'preschool',
#                 'elementary': 'grade_school',
#                 'elem': 'grade_school',
#                 'grade school': 'grade_school',
#                 'primary': 'grade_school',
#                 'junior high': 'junior_high',
#                 'jhs': 'junior_high',
#                 'junior highschool': 'junior_high',
#                 'secondary': 'junior_high',
#                 'senior high': 'senior_high',
#                 'shs': 'senior_high',
#                 'senior highschool': 'senior_high'
#             }
            
#             for indicator, intent in course_indicators.items():
#                 if indicator in query_subject:
#                     return intent
        
#         # For definition queries, prioritize explanatory content
#         elif query_context == 'definition_query':
#             if 'jarvis' in query_subject:
#                 return 'jarvis_meaning'
    
#     # Phase 2: Exact phrase matching with high priority (but context-aware)
#     for intent, keywords in intents.items():
#         phrase_score = 0
#         for keyword in keywords:
#             if keyword in text:
#                 word_count = len(keyword.split())
#                 if word_count > 1:
#                     phrase_score += word_count * 10
#                 else:
#                     # Single word matches get lower priority in informational contexts
#                     if query_context == 'informational_query' and intent == 'identity':
#                         phrase_score += 1  # Heavily penalize identity in informational context
#                     else:
#                         phrase_score += 5
        
#         if phrase_score > 0:
#             all_scores[intent] = phrase_score
    
#     # Phase 3: Individual word matching with smart weighting
#     for intent, keywords in intents.items():
#         word_score = 0
#         matched_words = set()
        
#         for keyword in keywords:
#             keyword_words = set(keyword.split())
#             matches = keyword_words.intersection(text_words)
            
#             if matches:
#                 for word in matches:
#                     # Context-aware scoring
#                     if query_context == 'informational_query' and intent == 'identity':
#                         # Heavily penalize identity intent in informational queries
#                         if word in ['about', 'tell', 'yourself']:
#                             continue  # Skip these words for identity in informational context
                    
#                     # Smart weighting based on word specificity
#                     if word in ['cs', 'stem', 'abm', 'humss', 'ga', 'he', 'jhs', 'shs', 'bsba', 'opac', 'gcs']:
#                         word_score += 25  # Very high for specific abbreviations
#                     elif word in ['programming', 'coding', 'tourism', 'hospitality', 'culinary', 'coaching']:
#                         word_score += 20  # High for course-specific terms
#                     elif word in ['science', 'technology', 'engineering', 'mathematics', 'business', 'management']:
#                         word_score += 15  # Medium-high for field-specific terms
#                     elif word in ['enrollment', 'admission', 'tuition', 'facilities']:
#                         word_score += 12  # Medium for school-specific terms
#                     elif word in ['department', 'departments', 'services', 'contact', 'location']:
#                         word_score += 10  # Medium for navigation terms
#                     elif word in ['education', 'degree', 'program', 'course']:
#                         word_score += 8   # Medium-low for general academic terms
#                     elif word in ['preschool', 'elementary', 'junior', 'senior', 'grade', 'level']:
#                         word_score += 7   # Medium-low for level terms
#                     elif word in ['about', 'tell', 'what', 'how', 'where']:
#                         if query_context != 'informational_query' or intent != 'identity':
#                             word_score += 2   # Low for generic query words (but not penalized in right context)
#                     else:
#                         word_score += 5   # Standard score for other words
                
#                 matched_words.update(matches)
        
#         # Bonus for multiple word matches in same intent
#         if len(matched_words) > 1:
#             word_score += len(matched_words) * 3
        
#         # Add to total scores
#         if word_score > 0:
#             if intent in all_scores:
#                 all_scores[intent] += word_score
#             else:
#                 all_scores[intent] = word_score
    
#     # Phase 4: Context-specific adjustments
#     if query_context == 'informational_query':
#         # Boost website and course-related intents for "tell me about" queries
#         website_intents = [
#             'website_about', 'website_departments', 'website_basic_education', 
#             'website_higher_education', 'website_student_services', 'website_enrollment',
#             'website_online_grade', 'website_gcs', 'website_opac', 'website_alumni',
#             'website_contact', 'website_locations'
#         ]
        
#         course_intents = [
#             'computer_science', 'computer_technology', 'tourism', 'hospitality', 
#             'business_admin', 'physical_education', 'early_childhood_ed', 
#             'elementary_ed', 'secondary_ed', 'stem', 'abm', 'humss', 'ga', 'he',
#             'preschool', 'grade_school', 'junior_high', 'senior_high'
#         ]
        
#         for intent in website_intents + course_intents:
#             if intent in all_scores:
#                 all_scores[intent] += 15  # Significant boost for content intents
        
#         # Heavily penalize identity intent in informational context
#         if 'identity' in all_scores:
#             all_scores['identity'] = max(1, all_scores['identity'] - 20)
    
#     # Phase 5: Special handling for ambiguous cases
#     # If "about" appears but it's clearly asking for information, not identity
#     if 'about' in text and any(word in text for word in ['tell', 'info', 'information', 'details']):
#         if 'identity' in all_scores and any(intent.startswith('website_') for intent in all_scores):
#             # If we have both identity and website intents, prefer website
#             website_scores = {k: v for k, v in all_scores.items() if k.startswith('website_')}
#             if website_scores:
#                 best_website = max(website_scores.items(), key=lambda x: x[1])
#                 if best_website[1] >= all_scores.get('identity', 0):
#                     return best_website[0]
    
#     # Phase 6: Return best match with minimum threshold
#     if all_scores:
#         # Filter out very low scores
#         filtered_scores = {k: v for k, v in all_scores.items() if v >= 3}
        
#         if filtered_scores:
#             best_intent, best_score = max(filtered_scores.items(), key=lambda x: x[1])
            
#             # Additional validation: make sure the match makes sense
#             if best_score >= 8:  # Higher threshold for better accuracy
#                 return best_intent
    
#     # Phase 7: Fuzzy matching as final fallback
#     for intent, keywords in intents.items():
#         # Skip identity for informational queries in fuzzy matching too
#         if query_context == 'informational_query' and intent == 'identity':
#             continue
            
#         matches = get_close_matches(text, keywords, n=1, cutoff=0.85)  # Higher threshold
#         if matches:
#             return intent
    
#     return "unknown"


# def test_improved_detection():
#     """Test the improved detection with problematic cases"""
#     test_cases = [
#         # The main problem case
#         ("tell me about", "unknown"),  # Should not trigger identity
#         ("tell me about sfac", "website_about"),
#         ("tell me about the school", "website_about"),
        
#         # Computer Science variations
#         ("tell me about cs", "computer_science"),
#         ("tell me about computer science", "computer_science"),
#         ("tell me about programming", "computer_science"),
#         ("tell me about coding", "computer_science"),
        
#         # Business & Tourism (the main issue)
#         ("tell me about hm", "hospitality"),  # This was failing!
#         ("tell me about hospitality", "hospitality"),
#         ("tell me about hospitality management", "hospitality"),
#         ("tell me about tourism", "tourism"),
#         ("tell me about business", "business_admin"),
#         ("tell me about bsba", "business_admin"),
        
#         # Senior High Tracks
#         ("tell me about stem", "stem"),
#         ("tell me about abm", "abm"),
#         ("tell me about humss", "humss"),
#         ("tell me about ga", "ga"),
#         ("tell me about he", "he"),
        
#         # Education Programs
#         ("tell me about pe", "physical_education"),
#         ("tell me about physical education", "physical_education"),
        
#         # Basic Education Levels
#         ("tell me about preschool", "preschool"),
#         ("tell me about elementary", "grade_school"),
#         ("tell me about junior high", "junior_high"),
#         ("tell me about senior high", "senior_high"),
        
#         # Website navigation
#         ("tell me about departments", "website_departments"),
#         ("tell me about student services", "website_student_services"),
        
#         # About page specific
#         ("about us", "website_about"),
#         ("about sfac", "website_about"),
#         ("about the college", "website_about"),
        
#         # Identity should still work in proper context
#         ("who are you", "identity"),
#         ("what are you", "identity"),
#         ("introduce yourself", "identity"),
        
#         # Course inquiries without "tell me about"
#         ("what is cs", "computer_science"),
#         ("what is hm", "hospitality"),
#         ("info about programming", "computer_science"),
#         ("details about stem track", "stem"),
        
#         # Website navigation
#         ("where is student services", "website_student_services"),
#         ("how to check online grades", "website_online_grade"),
#         ("contact information", "website_contact"),
#     ]
    
#     print("\n" + "="*70)
#     print("Testing Improved Context-Aware Intent Detection:")
#     print("="*70)
    
#     correct = 0
#     total = len(test_cases)
    
#     for test_input, expected in test_cases:
#         detected_intent = enhanced_detect_intent(test_input)
#         status = "✅ PASS" if detected_intent == expected else "❌ FAIL"
#         if detected_intent == expected:
#             correct += 1
#         print(f"{status} '{test_input}' -> {detected_intent} (expected: {expected})")
    
#     print("="*70)
#     print(f"Results: {correct}/{total} ({correct/total*100:.1f}%) tests passed")
    
#     return correct == total
# def jarvis_response(user_input, session_id):
#     """Generate JARVIS response with enhanced logic"""
#     session = session_manager.get_session(session_id)
    
#     # Check for memory intent first
#     if detect_memory_intent(user_input):
#         return handle_memory(user_input, session_id)
    
#     # Enhanced intent detection with scoring
#     intent = enhanced_detect_intent(user_input)
    
#     # Get user's preferred identifier (name or title)
#     identifier = session.get("name", session.get("title", "Sir"))
    
#     # Get response and format it
#     reply = random.choice(responses.get(intent, responses["unknown"]))
    
#     # Handle time-aware greetings
#     if intent == "greeting":
#         time_greeting = get_time_aware_greeting()
#         reply = reply.format(
#             title=identifier, 
#             time_greeting=time_greeting,
#             time_greeting_lower=time_greeting.lower()
#         )
#     else:
#         reply = reply.format(title=identifier)
    
#     return reply

# # Test function to verify the improved scoring
# def test_improved_scoring():
#     """Test the improved scoring system"""
#     test_cases = [
#         # CS variations - should all return computer_science
#         ("tell me about cs", "computer_science"),
#         ("tell me about the cs course", "computer_science"),
#         ("about cs", "computer_science"),
#         ("cs program", "computer_science"),
#         ("what is cs", "computer_science"),
#         ("cs degree", "computer_science"),
#         ("computer science", "computer_science"),
        
#         # Other courses
#         ("tell me about stem", "stem"),
#         ("about tourism", "tourism"),
#         ("business administration", "business_admin"),
#         ("tell me about programming", "computer_science"),
        
#         # Website navigation - should still work
#         ("about us", "website_about"),
#         ("about sfac", "website_about"),
#         ("about the school", "website_about"),
        
#         # Edge cases
#         ("programming course", "computer_science"),
#         ("coding program", "computer_science"),
#         ("hospitality management", "hospitality"),
#     ]
    
#     print("\nTesting Improved Scoring System:")
#     print("="*50)
    
#     correct = 0
#     total = len(test_cases)
    
#     for test_input, expected in test_cases:
#         detected_intent = enhanced_detect_intent(test_input)
#         status = "✅ PASS" if detected_intent == expected else "❌ FAIL"
#         if detected_intent == expected:
#             correct += 1
#         print(f"{status} '{test_input}' -> {detected_intent} (expected: {expected})")
    
#     print("="*50)
#     print(f"Results: {correct}/{total} ({correct/total*100:.1f}%) tests passed")
    
#     # Debug specific case
#     print("\nDebug 'tell me about cs':")
#     debug_scoring("tell me about cs")
    
#     return correct == total

# def debug_scoring(user_input):
#     """Debug function to show scoring breakdown"""
#     text = user_input.lower().strip()
#     text_words = set(text.split())
    
#     print(f"Input: '{user_input}'")
#     print(f"Text words: {text_words}")
    
#     # Show scoring for relevant intents
#     relevant_intents = ['computer_science', 'website_about', 'course']
    
#     for intent in relevant_intents:
#         if intent in intents:
#             score = 0
#             matched_words = []
            
#             for keyword in intents[intent]:
#                 keyword_words = set(keyword.split())
#                 matches = keyword_words.intersection(text_words)
                
#                 if matches:
#                     for word in matches:
#                         if word == 'cs':
#                             word_score = 20
#                         elif word == 'about':
#                             word_score = 1
#                         elif word == 'course':
#                             word_score = 3
#                         else:
#                             word_score = 5
                        
#                         score += word_score
#                         matched_words.append(f"{word}({word_score})")
            
#             # Context bonus
#             if intent == 'computer_science' and "tell me about" in text:
#                 score += 10
#                 matched_words.append("context_bonus(10)")
            
#             print(f"{intent}: {score} points - {matched_words}")

# if __name__ == '__main__':
#     test_improved_scoring()

# # Flask routes
# @app.route('/')
# def home():
#     return jsonify({
#         "message": "JARVIS API v2.3 - SFAC Enhanced Edition with Website Navigation is online and ready to assist.",
#         "version": "2.3",
#         "status": "operational",
#         "features": [
#             "Comprehensive SFAC curriculum coverage",
#             "Enhanced intent detection with plural handling",
#             "Multi-word phrase recognition",
#             "Session-based personalization",
#             "Rate limiting protection",
#             "Fixed course inquiry handling",
#             "Website navigation assistance"
#         ]
#     })

# @app.route('/chat', methods=['POST'])
# def chat():
#     client_ip = request.environ.get('REMOTE_ADDR', 'unknown')
    
#     # Rate limiting
#     if is_rate_limited(client_ip):
#         return jsonify({
#             'error': 'Too many requests. Please wait a moment before trying again.',
#             'status': 'rate_limited'
#         }), 429
    
#     try:
#         data = request.get_json()
        
#         if not data or 'message' not in data:
#             return jsonify({'error': 'No message provided'}), 400
        
#         user_message = data['message']
#         session_id = data.get('session_id', f'default_{int(time.time())}')
        
#         # Validate inputs
#         validated_message = validate_input(user_message)
#         if not validated_message:
#             return jsonify({'error': 'Invalid message format or too long'}), 400
        
#         if not validate_session_id(session_id):
#             return jsonify({'error': 'Invalid session ID'}), 400
        
#         # Check for shutdown words
#         shutdown_words = ["quit", "exit", "goodbye", "bye", "bye bye", "shutdown", "power off", "log off", "sign out", "okay bye", "ok bye", "alright bye", "well bye", "thanks bye", "thank you bye", "cool bye", "see ya", "see you", "cya", "later", "gtg", "gotta go", "talk later", "catch you later"]
#         if validated_message.lower() in shutdown_words:
#             session = session_manager.get_session(session_id)
#             identifier = session.get("name", session.get("title", "Sir"))
#             goodbye_responses = [
#                 f"Shutting down systems. Until next time, {identifier}. SFAC looks forward to serving you again.",
#                 f"Powering off. Farewell, {identifier}. Remember, excellence in education awaits at SFAC.",
#                 f"System offline. Goodbye, {identifier}. Feel free to contact SFAC anytime for your educational needs.",
#             ]
#             return jsonify({
#                 'response': random.choice(goodbye_responses),
#                 'status': 'shutdown'
#             })
        
#         # Generate JARVIS response
#         bot_response = jarvis_response(validated_message, session_id)
        
#         return jsonify({
#             'response': bot_response,
#             'status': 'success'
#         })
    
#     except Exception as e:
#         print(f"Error in chat endpoint: {e}")
#         return jsonify({
#             'error': 'System malfunction detected. Please try again.',
#             'status': 'error'
#         }), 500

# @app.route('/set_title', methods=['POST'])
# def set_title():
#     """Allow users to set their preferred title"""
#     client_ip = request.environ.get('REMOTE_ADDR', 'unknown')
    
#     if is_rate_limited(client_ip):
#         return jsonify({'error': 'Too many requests'}), 429
    
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({'error': 'No data provided'}), 400
            
#         session_id = data.get('session_id', f'default_{int(time.time())}')
#         title_choice = data.get('title', '').lower()
        
#         if not validate_session_id(session_id):
#             return jsonify({'error': 'Invalid session ID'}), 400
        
#         title = "Ma'am" if "ma" in title_choice or "miss" in title_choice else "Sir"
        
#         session_manager.update_session(session_id, {"title": title})
        
#         return jsonify({
#             'response': f"Acknowledged, {title}. JARVIS is fully operational and ready to assist with SFAC inquiries.",
#             'status': 'success'
#         })
    
#     except Exception as e:
#         print(f"Error in set_title endpoint: {e}")
#         return jsonify({'error': 'Could not set title'}), 500

# @app.route('/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     return jsonify({
#         'status': 'healthy',
#         'timestamp': int(time.time()),
#         'active_sessions': len(session_manager.sessions),
#         'version': '2.3',
#         'features_active': True
#     })

# @app.route('/stats', methods=['GET'])
# def get_stats():
#     """Statistics endpoint for monitoring"""
#     return jsonify({
#         'active_sessions': len(session_manager.sessions),
#         'total_intents': len(intents),
#         'total_responses': sum(len(responses[key]) for key in responses),
#         'rate_limit_settings': {
#             'requests_per_minute': RATE_LIMIT,
#             'window_seconds': RATE_WINDOW
#         },
#         'session_settings': {
#             'cleanup_interval_seconds': session_manager.cleanup_interval,
#             'session_timeout_seconds': session_manager.session_timeout
#         }
#     })

# @app.route('/test_intent', methods=['POST'])
# def test_intent():
#     """Test endpoint to check intent detection (for debugging)"""
#     try:
#         data = request.get_json()
#         if not data or 'message' not in data:
#             return jsonify({'error': 'No message provided'}), 400
        
#         user_message = data['message']
#         validated_message = validate_input(user_message)
        
#         if not validated_message:
#             return jsonify({'error': 'Invalid message format'}), 400
        
#         detected_intent = enhanced_detect_intent(validated_message)
        
#         return jsonify({
#             'input': validated_message,
#             'detected_intent': detected_intent,
#             'available_intents': list(intents.keys()),
#             'matching_keywords': intents.get(detected_intent, []) if detected_intent != "unknown" else []
#         })
    
#     except Exception as e:
#         print(f"Error in test_intent endpoint: {e}")
#         return jsonify({'error': 'Test failed'}), 500

# def test_grade_detection():
#     """Test function to verify grade level detection works correctly"""
#     test_cases = [
#         # Grade School (1-6)
#         ("grade 1", "grade_school"),
#         ("Grade 2", "grade_school"),
#         ("I'm in grade 3", "grade_school"),
#         ("what about grade 6", "grade_school"),
#         ("1st grade", "grade_school"),
#         ("3rd grade requirements", "grade_school"),
#         ("elementary", "grade_school"),
        
#         # Junior High (7-10)
#         ("grade 7", "junior_high"),
#         ("Grade 8", "junior_high"),
#         ("grade 9 subjects", "junior_high"),
#         ("what about grade 10", "junior_high"),
#         ("7th grade", "junior_high"),
#         ("junior high", "junior_high"),
        
#         # Senior High (11-12)
#         ("grade 11", "senior_high"),
#         ("Grade 12", "senior_high"),
#         ("grade 11 tracks", "senior_high"),
#         ("11th grade", "senior_high"),
#         ("12th grade graduation", "senior_high"),
#         ("senior high", "senior_high"),
        
#         # Website Navigation
#         ("about us", "website_about"),
#         ("student services", "website_student_services"),
#         ("online grades", "website_online_grade"),
#         ("library opac", "website_opac"),
        
#         # Edge cases
#         ("grade 0", "preschool"),
#         ("grade 13", None),  
#         ("grades 1-6", "grade_school"),  
#     ]
    
#     print("\n" + "="*60)
#     print("Testing Grade Level Detection & Website Navigation:")
#     print("="*60)
    
#     for test_input, expected in test_cases:
#         detected_intent = enhanced_detect_intent(test_input)
#         if expected is None:
#             status = "✅ PASS" if detected_intent == "unknown" else "❌ FAIL"
#             print(f"{status} Input: '{test_input}' -> Intent: '{detected_intent}' (Expected: unknown)")
#         else:
#             status = "✅ PASS" if detected_intent == expected else "❌ FAIL"
#             print(f"{status} Input: '{test_input}' -> Intent: '{detected_intent}' (Expected: {expected})")
    
#     print("="*60)

# if __name__ == '__main__':
#     print("=" * 60)
#     print("JARVIS API v2.3 - SFAC Enhanced Edition with Website Navigation")
#     print("=" * 60)
#     print("🚀 Starting up enhanced JARVIS system...")
#     print(f"📚 Loaded {len(intents)} intent categories")
#     print(f"💬 Configured {sum(len(responses[key]) for key in responses)} response variations")
#     print("🏫 Specialized for St. Francis of Assisi College")
#     print("🌐 Website navigation assistance enabled")
#     print("=" * 60)
#     print("🌍 API Endpoints:")
#     print("   • Main API: http://localhost:5000")
#     print("   • Chat: http://localhost:5000/chat")
#     print("   • Health: http://localhost:5000/health")
#     print("   • Stats: http://localhost:5000/stats")
#     print("   • Set Title: http://localhost:5000/set_title")
#     print("   • Test Intent: http://localhost:5000/test_intent")
#     print("=" * 60)
    
#     # Run grade detection test
#     test_grade_detection()
    
#     print("✅ JARVIS is now online and ready to assist!")
#     print("🔧 Course intent detection has been FIXED!")
#     print("🎯 Grade level detection has been ENHANCED!")
#     print("🌐 Website navigation assistance ADDED!")
    
#     app.run(debug=True, host='localhost', port=5000)