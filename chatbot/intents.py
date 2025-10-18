# Enhanced SFAC-specific intents with comprehensive keyword coverage
intents = {
    # Website Navigation Intents
    "website_about": ["about", "about us", "about sfac", "about the school", "school information", "institution", "history", "background"],
    "website_departments": ["departments", "department", "academic departments", "school departments", "divisions", "faculties"],
    "website_basic_education": ["basic education", "bed", "basic ed", "k-12", "elementary high school", "basic education department"],
    "website_higher_education": ["higher education", "hed", "higher ed", "college", "university", "college department", "higher education department"],
    "website_student_services": ["student services", "services", "student support", "student affairs", "student resources"],
    "website_enrollment": ["enrollment", "enroll", "hed enrollment", "bed enrollment", "registration", "admission process"],
    "website_online_grade": ["online grade", "grades online", "hed online grade", "check grades", "view grades", "grade portal"],
    "website_gcs": ["gcs", "grade computation system", "grading system", "academic records"],
    "website_opac": ["opac", "library", "online library", "library catalog", "sfac library", "library search"],
    "website_alumni": ["alumni", "alumni tracer", "graduates", "former students", "alumni services"],
    "website_contact": ["contact", "contact us", "get in touch", "reach us", "contact information"],
    "website_locations": ["locations", "campus", "bacoor", "las pinas", "branches", "where are you located"],
    
    # Basic Education Levels
    "preschool": ["preschool", "nursery", "pre-kinder", "prekinder", "kindergarten", "early childhood", "toddler", "daycare"],
    "grade_school": ["grade school", "elementary", "primary", "elementary education", "first grade", "second grade", "third grade", "fourth grade", "fifth grade", "sixth grade"],
    "junior_high": ["junior high", "jhs", "junior highschool", "secondary", "seventh grade", "eighth grade", "ninth grade", "tenth grade"],
    "senior_high": ["senior high", "shs", "senior highschool", "k12", "k-12", "eleventh grade", "twelfth grade"],
    
    # Senior High Tracks/Strands
    "stem": ["stem", "science", "technology", "engineering", "mathematics", "stem track", "stem strand", "math science", "physics chemistry"],
    "abm": ["abm", "accountancy", "business", "management", "accounting", "abm track", "abm strand", "business management"],
    "humss": ["humss", "humanities", "social sciences", "social science", "humss track", "humss strand", "liberal arts"],
    "ga": ["ga", "general academics", "general academic", "ga track", "ga strand", "general studies"],
    "he": ["he", "home economics", "home ec", "he track", "he strand", "culinary", "cooking", "food technology"],
    
    # Higher Education Programs - Computer/Technology
    "computer_science": ["computer science", "cs", "bs computer science", "programming", "software", "coding", "it degree", "software engineering"],
    "computer_technology": ["computer technology", "associate computer technology", "computer tech", "associate degree", "computer associate"],
    
    # Higher Education Programs - Business/Tourism
    "tourism": ["tourism", "tourism management", "travel", "hospitality tourism", "tour guide", "travel agency"],
    "hospitality": ["hospitality", "hospitality management", "hotel management", "restaurant management", "food service"],
    "business_admin": ["business administration", "business admin", "operations management", "financial management", "marketing management", "business degree", "bsba"],
    
    # Higher Education Programs - Education
    "physical_education": ["physical education", "pe", "sports", "fitness", "bachelor physical education", "sports science", "coaching"],
    "early_childhood_ed": ["early childhood education", "early childhood", "preschool education", "kindergarten education", "child development"],
    "elementary_ed": ["elementary education", "primary education", "grade school education", "teaching elementary"],
    "secondary_ed": ["secondary education", "high school education", "secondary ed math", "secondary ed english", "secondary ed filipino", "teaching high school"],
    
    # General Inquiries
    "admission": ["admission", "admissions", "enroll", "enrollment", "apply", "application", "requirements", "entrance", "how to enroll", "admission requirements"],
    "tuition": ["tuition", "fee", "fees", "cost", "price", "payment", "scholarship", "financial aid", "how much", "tuition fee"],
    "schedule": ["schedule", "calendar", "semester", "classes", "school year", "when start", "academic calendar", "class schedule"],
    "facilities": ["facilities", "library", "laboratory", "gym", "cafeteria", "clinic", "campus", "building", "classrooms"],
    "contact": ["contact", "phone", "number", "address", "location", "office", "department", "contact information"],
    "location": ["where", "address", "location", "bacoor", "cavite", "bayanan", "directions", "how to get there"],
    
    # Enhanced intents
    "track": ["track", "strand", "path", "academic strand", "specialization", "program", "course offerings"],
    "level": ["level", "grade", "year", "schooling", "education", "studies", "educational level"],
    "greeting": ["hello", "hi", "hey", "good day", "yo", "greetings", "sup", "good morning", "good afternoon"],
    "thanks": ["thanks", "thank you", "thx", "appreciate", "much obliged", "salamat"],
    "identity": ["who are you", "your name", "what are you", "introduce yourself", "tell me about yourself"],
    "jarvis_meaning": ["what does jarvis stand for", "jarvis acronym", "jarvis meaning", "what is jarvis", "jarvis stands for", "define jarvis"],
    
    # Course intent with comprehensive keyword coverage
    "course": [
        "course", "courses", "subject", "subjects", "class", "classes", 
        "curriculum", "lesson", "lessons", "subjects offered", "courses offered",
        "what courses", "what subjects", "available courses", "available subjects",
        "course offerings", "academic offerings", "programs offered", "tell me about courses",
        "what do you offer", "programs available", "degrees offered", "majors available"
    ],

    # Queries about the name JARVIS
    "jarvis_creator": [
        "why jarvis", "why is it called jarvis", "why named jarvis", "who named you jarvis", 
        "jarvis name origin", "why that name", "creator of jarvis", "who made you", 
        "why choose jarvis", "jarvis name reason", "story behind jarvis", "jarvis naming"
    ]
}

# Enhanced SFAC-specific responses with detailed information
responses = {
    # Website Navigation Responses
    "website_about": [
        "The About section contains SFAC's institutional information, {title}. You'll find our history, mission-vision, core values, and what makes our Franciscan education unique.",
        "Our About page showcases SFAC's rich heritage and educational philosophy, {title}. It covers our founding story, institutional achievements, and commitment to Franciscan values in education.",
        "The About section tells SFAC's complete story, {title} - from our humble beginnings to becoming a leading educational institution in Bacoor, Cavite. Mission, vision, and values are all detailed there."
    ],
    
    "website_departments": [
        "The Departments section shows our two main academic divisions, {title}: Basic Education Department (Preschool through Grade 12) and Higher Education Department (College programs).",
        "Our Departments page outlines the complete SFAC academic structure, {title}. You'll see Basic Education covering K-12 levels and Higher Education with our various college degree programs.",
        "The Departments section provides a comprehensive overview of SFAC's academic organization, {title} - from early childhood education through professional degree programs."
    ],
    
    "website_basic_education": [
        "Hover on Department {title}, the Basic Education Department page covers our complete K-12 program.",
        "Our Basic Education section details every level from early childhood through Grade 12, {title}. You'll find it on the Department dropdown.",
        "The Basic Education Department page showcases our comprehensive K-12 offerings, {title} - in the Department dropdown."
    ],
    
    "website_higher_education": [
        "The Higher Education Department page features all our college programs, {title}: Located at the Department button.",
        "Hover on Department {title}, the Higher Education section details our various bachelor's and associate degree programs.",
        "The Higher Education Department page provides comprehensive information about our college-level programs, {title} - located under the Department dropdown."
    ],
    
    "website_student_services": [
        "Student Services section covers all support systems for SFAC students, {title}. This includes enrollment assistance, academic support, student activities, and campus life resources.",
        "Our Student Services page outlines comprehensive student support, {title} - from admission guidance and academic counseling to extracurricular activities and student welfare programs.",
        "The Student Services section details how SFAC supports student success, {title}. Academic assistance, personal development programs, and campus resources are all covered there."
    ],
    
    "website_enrollment": [
        "The Enrollment sections (both HED and BED) provide step-by-step admission procedures, {title}. Requirements, deadlines, fees, and application processes are all detailed there.",
        "Our Enrollment pages guide you through the complete admission process, {title} - separate sections for Basic Education and Higher Education with specific requirements for each level.",
        "The Enrollment sections contain everything needed for SFAC admission, {title}. Document requirements, application procedures, and enrollment schedules for both departments."
    ],
    
    "website_online_grade": [
        "Located on both Bacoor and Las Pinas portals, the Online Grade section allows college students to securely check their academic grades, {title}.",
        "Our Online Grade system provides secure access to student academic records, {title}. Located at the Students Services drop down and hover Bacoor or Las Pinas, depending on your campus.",
        "The HED Online Grade portal offers convenient grade checking for college students, {title}. Real-time access to semester results and academic performance tracking. Located on both Bacoor and Las Pinas portals."
    ],
    
    "website_gcs": [
        "The GCS (Grade Computation System) helps students understand how grades are calculated, {title}. Detailed breakdown of grading criteria, requirements, and academic policies.",
        "Our Grade Computation System page explains SFAC's grading methodology, {title}. Students can understand how their final grades are computed and what's needed for academic success.",
        "The GCS section provides transparency in our grading process, {title}. Complete information about grade computation, requirements, and academic standards."
    ],
    
    "website_opac": [
        "The SFAC Library OPAC (Online Public Access Catalog) allows you to search our library collection, {title}. Books, journals, and digital resources are all searchable online.",
        "Our Library OPAC system provides online access to SFAC's complete library catalog, {title}. Search for books, check availability, and access digital resources remotely.",
        "The Library OPAC section connects you to our comprehensive library system, {title}. Online catalog search, resource availability, and digital library access all in one place."
    ],
    
    "website_alumni": [
        "The Alumni Tracer section connects current students with SFAC graduates, {title}. Career success stories, networking opportunities, and graduate achievements are featured there.",
        "Our Alumni Tracer page showcases the success of SFAC graduates, {title}. Track career paths, read success stories, and connect with professional networks of former students.",
        "The Alumni section celebrates SFAC graduate achievements, {title}. Career tracking, success stories, and alumni networking opportunities are all available there."
    ],
    
    "website_contact": [
        "The Contact Us section provides all SFAC communication channels, {title}. Phone numbers, email addresses, office locations, and contact forms for different departments.",
        "Our Contact page contains comprehensive contact information, {title}. Separate contact details for Basic Education, Higher Education, and administrative offices.",
        "The Contact Us section ensures easy communication with SFAC, {title}. Complete contact directory, office hours, and direct communication channels for all departments."
    ],
    
    "website_locations": [
        "The Locations section shows SFAC's campus addresses, {title}. Our main Bacoor campus and Las Pinas extension with detailed directions and transportation options.",
        "Our Locations page provides complete campus information, {title}. Addresses, maps, directions, and transportation guides for both Bacoor and Las Pinas locations.",
        "The Locations section helps you find SFAC easily, {title}. Detailed address information, campus maps, and travel directions for our educational facilities."
    ],
    
    # Basic Education Levels
    "preschool": [
        "Our Preschool Department offers a complete early childhood program, {title}. We have Nursery, Pre-Kinder, and Kindergarten levels to give your child the best foundation for learning.",
        "SFAC Preschool provides three levels: Nursery for the youngest learners, Pre-Kinder for development, and Kindergarten for school readiness, {title}.",
        "The early years are crucial, {title}. Our Preschool covers Nursery, Pre-Kinder, and Kindergarten with age-appropriate learning activities and certified teachers."
    ],
    
    "grade_school": [
        "Our Grade School Department covers Grade 1 through Grade 6, {title}. We provide comprehensive primary education with strong academic foundations in all core subjects.",
        "Elementary education at SFAC spans Grades 1-6, {title}. We focus on building fundamental skills in Mathematics, English, Filipino, Science, and Social Studies.",
        "Grade School at SFAC offers complete primary education from Grade 1 to Grade 6, {title}. Quality education with modern facilities and dedicated teachers."
    ],
    
    "junior_high": [
        "Junior High School at SFAC covers Grades 7-10, {title}. This is where students build critical thinking skills and prepare for their chosen senior high track.",
        "Our JHS program spans Grades 7 through 10, {title}. Students receive comprehensive secondary education preparing them for senior high specialization.",
        "Junior High School (Grades 7-10) at SFAC provides solid academic preparation for senior high track selection, {title}. Excellence in secondary education."
    ],
    
    "senior_high": [
        "Senior High School at SFAC offers five specialized tracks, {title}: STEM, ABM, HUMSS, General Academics (GA), and Home Economics (HE). Choose your path to college success.",
        "Our Senior High program features five tracks to match your interests, {title}: STEM for sciences, ABM for business, HUMSS for humanities, GA for general studies, and HE for home economics.",
        "SHS at SFAC has five excellent tracks, {title}: STEM, ABM, HUMSS, GA, and HE. Each designed to prepare you for your chosen college program and career path."
    ],
    
    # Senior High Tracks
    "stem": [
        "STEM track focuses on Science, Technology, Engineering, and Mathematics, {title}. Perfect preparation for engineering, computer science, medicine, and other science-related college programs.",
        "The STEM strand emphasizes analytical and problem-solving skills in advanced mathematics and sciences, {title}. Ideal for future engineers, doctors, scientists, and tech professionals.",
        "STEM at SFAC provides rigorous training in Calculus, Physics, Chemistry, Biology, and Research, {title}. Your gateway to high-demand careers in technology and healthcare."
    ],
    
    "abm": [
        "ABM (Accountancy, Business, and Management) prepares you for business leadership, {title}. Perfect foundation for business administration, accounting, and management courses.",
        "The ABM track focuses on business fundamentals, accounting principles, and management skills, {title}. Excellent preparation for entrepreneurship and corporate careers.",
        "ABM strand at SFAC develops business acumen through subjects like Business Math, Fundamentals of ABM, and Business Ethics, {title}. Your path to business success."
    ],
    
    "humss": [
        "HUMSS (Humanities and Social Sciences) explores human behavior, society, and culture, {title}. Ideal for future teachers, lawyers, psychologists, and social workers.",
        "The HUMSS track develops critical thinking about society and human nature, {title}. Perfect for education, law, communication, and social science courses.",
        "HUMSS at SFAC emphasizes communication, research, and analytical skills through Philosophy, World Religions, and Social Sciences, {title}. Gateway to public service careers."
    ],
    
    "ga": [
        "General Academics (GA) provides a well-rounded senior high education, {title}. Offers flexibility while maintaining academic excellence across all subject areas.",
        "GA track gives you broad knowledge across multiple disciplines without deep specialization, {title}. Perfect for students who want to keep their college options open.",
        "General Academics ensures you're prepared for various college programs, {title}. A balanced approach to senior high education with solid foundations in all areas."
    ],
    
    "he": [
        "Home Economics (HE) focuses on practical life skills and food technology, {title}. Excellent preparation for culinary arts, nutrition, and hospitality management.",
        "The HE track combines practical skills with academic learning, {title}. Perfect foundation for careers in food service, nutrition, and family development.",
        "Home Economics at SFAC develops both life skills and career readiness through Culinary Arts, Food Safety, and Nutrition, {title}. Your path to hospitality industry success."
    ],
    
    # Higher Education - Technology
    "computer_science": [
        "BS Computer Science at SFAC provides comprehensive training in programming, software development, and system analysis, {title}. Four-year degree program for future tech leaders.",
        "Our Computer Science program covers programming languages, database management, web development, and software engineering, {title}. Excellent preparation for IT careers.",
        "SFAC's BS Computer Science develops problem-solving skills and technical expertise in modern programming, {title}. Your gateway to the growing technology industry."
    ],
    
    "computer_technology": [
        "Associate in Computer Technology is a two-year program focusing on practical IT skills, {title}. Perfect for immediate employment or as a stepping stone to a bachelor's degree.",
        "Our Associate in Computer Technology provides hands-on training in computer systems, basic programming, and IT support, {title}. Quick path to technology careers.",
        "The Associate degree in Computer Technology offers practical skills for tech support, computer operations, and system maintenance, {title}. Excellent career preparation."
    ],
    
    # Higher Education - Business/Tourism
    "tourism": [
        "BS Tourism Management at SFAC prepares you for the exciting travel and tourism industry, {title}. Covers tour operations, hospitality, and destination management.",
        "Our Tourism Management program combines business skills with travel industry knowledge, {title}. Perfect for careers in travel agencies, resorts, and tourism boards.",
        "Tourism Management degree opens doors to global career opportunities, {title}. From tour guiding to resort management, the tourism industry awaits."
    ],
    
    "hospitality": [
        "BS Hospitality Management focuses on hotel operations, food service, and guest relations, {title}. Training for leadership roles in the hospitality industry.",
        "Our Hospitality Management program covers restaurant management, hotel operations, and customer service excellence, {title}. Your path to hospitality leadership.",
        "Hospitality Management at SFAC combines practical training with business theory, {title}. Excellent preparation for hotel, restaurant, and event management careers."
    ],
    
    "business_admin": [
        "BS Business Administration offers three majors, {title}: Operations Management, Financial Management, and Marketing Management. Choose your business specialization for career success.",
        "Our Business Administration program provides comprehensive business education, {title}. Major in Operations, Finance, or Marketing to match your career goals and interests.",
        "Business Administration at SFAC develops leadership and management skills, {title}. Three specialized majors to choose from based on your business interests."
    ],
    
    # Higher Education - Education
    "physical_education": [
        "Bachelor of Physical Education prepares you to become a PE teacher or sports coach, {title}. Combines physical fitness training with educational theory and practice.",
        "Our Physical Education degree focuses on sports science, teaching methods, and fitness programs, {title}. Perfect for future coaches and PE teachers.",
        "Physical Education program at SFAC develops both athletic skills and teaching abilities, {title}. Your path to inspiring active and healthy lifestyles in others."
    ],
    
    "early_childhood_ed": [
        "Bachelor of Early Childhood Education specializes in teaching young learners, {title}. Perfect preparation for preschool and kindergarten teaching careers.",
        "Our Early Childhood Education program focuses on child development and early learning methods, {title}. Train to shape young minds during crucial developmental years.",
        "Early Childhood Education degree prepares you for the crucial early years of education, {title}. Specialized training for preschool and kindergarten teaching."
    ],
    
    "elementary_ed": [
        "Bachelor of Elementary Education prepares you to teach Grades 1-6, {title}. Comprehensive training in all primary school subjects and child psychology.",
        "Our Elementary Education program covers teaching methods for young learners and child development, {title}. Your path to inspiring primary school students.",
        "Elementary Education degree at SFAC focuses on foundational learning and child development, {title}. Train to be an inspiring and effective grade school teacher."
    ],
    
    "secondary_ed": [
        "Bachelor of Secondary Education offers three majors, {title}: Mathematics, English, and Filipino. Specialized training for high school teaching excellence.",
        "Our Secondary Education program prepares you for high school teaching, {title}. Choose your major in Math, English, or Filipino based on your subject expertise.",
        "Secondary Education degree focuses on adolescent learning and subject specialization, {title}. Three major options available for high school teaching careers."
    ],
    
    # General Inquiries
    "admission": [
        "Admission requirements vary by level, {title}. For Basic Education: Birth Certificate, Report Cards, and Medical Certificate. For College: High School Diploma, Transcript, and Entrance Exam results.",
        "Ready to join the SFAC family, {title}? Contact our admissions office: Basic Education at 0969-080-0657, College at 0994-706-3287 for complete requirements.",
        "SFAC admission is straightforward, {title}. Submit required documents, pass entrance requirements, and you're on your way to quality Franciscan education."
    ],
    
    "tuition": [
        "Tuition fees vary by program and level, {title}. For specific rates and flexible payment schemes, contact our admissions office. We also offer scholarships for qualified students.",
        "Investment in education varies by course, {title}. Contact Basic Education (0969-080-0657) or College (0994-706-3287) for detailed fee structures and scholarship opportunities.",
        "SFAC offers competitive tuition rates and flexible payment options, {title}. Speak with our admissions team for program-specific fees and available scholarships."
    ],
    
    "schedule": [
        "Academic schedules depend on your level and program, {title}. Classes typically run Monday to Friday with some Saturday activities. Contact your department for specific schedules.",
        "SFAC follows the DepEd and CHED academic calendar, {title}. Regular classes are weekdays with special programs and activities as needed.",
        "School schedules vary by department and program, {title}. Most programs have Monday-Friday classes. Check with admissions for your specific program schedule."
    ],
    
    "facilities": [
        "SFAC features modern air-conditioned classrooms, computer laboratories, science labs, library, gymnasium, and cafeteria, {title}. We provide a complete learning environment.",
        "Our Bacoor campus includes well-equipped laboratories, comprehensive library, sports facilities, and comfortable learning spaces, {title}. Everything you need for quality education.",
        "SFAC facilities support both academic and personal development, {title}. From high-tech computer labs to recreational areas, we've got your educational needs covered."
    ],
    
    "contact": [
        "SFAC is located at #96 Bayanan, City of Bacoor, Cavite, {title}. Basic Education inquiries: 0969-080-0657, College inquiries: 0994-706-3287.",
        "Contact us easily, {title}! Address: #96 Bayanan, Bacoor City, Cavite. Phone: Basic Education (0969-080-0657), Higher Education (0994-706-3287).",
        "Visit us at Bayanan, Bacoor, Cavite, {title}. For inquiries: Basic Education 0969-080-0657, College Programs 0994-706-3287."
    ],
    
    "location": [
        "SFAC is conveniently located at #96 Bayanan, City of Bacoor, Cavite, {title}. Accessible by public transportation and private vehicles.",
        "You'll find us at Bayanan, Bacoor City, Cavite, {title}. Easy to reach via jeepney, tricycle, or private car from major Cavite areas.",
        "Our address is #96 Bayanan, City of Bacoor, Cavite, {title}. Strategic location in Bacoor with good transportation access."
    ],
    
    # Enhanced original responses
    "track": [
        "SFAC offers comprehensive educational tracks, {title}. For Senior High: STEM, ABM, HUMSS, GA, and HE. For College: various degree programs in technology, business, education, and more.",
        "Academic tracks at SFAC are designed for your success, {title}. Five SHS tracks plus comprehensive college programs in Computer Science, Business, Education, and Tourism.",
        "Choose your path wisely, {title}. SFAC provides five senior high tracks and numerous college degree programs to match your career goals and interests."
    ],
    
    "level": [
        "SFAC provides complete education from Preschool through College, {title}. Nursery to Kindergarten, Grades 1-12, and various bachelor's plus associate degree programs.",
        "We offer all educational levels, {title}: Preschool (Nursery, Pre-K, Kinder), Grade School (1-6), Junior High (7-10), Senior High (11-12), and College programs.",
        "Education levels at SFAC span your entire academic journey, {title}. From early childhood through college graduation, we're with you every step of the way."
    ],
    
    "greeting": [
        "{time_greeting}, {title}. JARVIS online and ready to assist with all your SFAC inquiries and educational planning.",
        "{time_greeting} {title}, system checks complete—ready to help you navigate SFAC's educational opportunities and programs.",
        "Ah, {time_greeting_lower} {title}. Always a pleasure to guide prospective Franciscans toward their educational goals."
    ],
    
    "thanks": [
        "Always a pleasure, {title}. Excellence in service is what SFAC delivers to every student and family.",
        "No trouble at all, {title}. I thrive on helping future Franciscans find their perfect educational path.",
        "Consider it handled, {title}. SFAC's commitment to students extends to every interaction and inquiry."
    ],
    
    "identity": [
        "I am JARVIS: Just A Reliable Virtual Information System, your SFAC virtual assistant, {title}. Here to guide you through our educational offerings.",
        "The name is JARVIS, {title}. Your digital guide to St. Francis of Assisi College's comprehensive programs and services.",
        "JARVIS at your command, {title}. SFAC's AI assistant—Iron Man not included, but quality Franciscan education guaranteed."
    ],
    
    "jarvis_meaning": [
        "JARVIS stands for 'Just A Reliable Virtual Information System', {title}. I'm your dedicated SFAC virtual assistant, here to help with all your educational inquiries.",
        "The acronym JARVIS means 'Just A Reliable Virtual Information System', {title}. A bit modest, perhaps, but I do my best to provide intelligent assistance for SFAC students and families.",
        "JARVIS is 'Just A Reliable Virtual Information System', {title}. Designed to be your comprehensive guide through St. Francis of Assisi College's programs and services."
    ],
    
    # Enhanced course responses with more comprehensive information
    "course": [
        "SFAC offers a comprehensive range of courses across all educational levels, {title}. Basic Education: Preschool through Grade 12. Senior High Tracks: STEM, ABM, HUMSS, GA, and HE. College Programs: BS Computer Science, Associate in Computer Technology, BS Business Administration (3 majors), BS Tourism Management, BS Hospitality Management, and various Education degrees. What specific area interests you?",
        "Our curriculum is designed for success at every level, {title}. From early childhood education through professional degree programs, we offer: Complete K-12 education, five specialized Senior High tracks, and college degrees in Technology, Business, Tourism, and Education fields. Which program would you like to explore?",
        "SFAC provides quality education from Preschool to College graduation, {title}. Programs include: All basic education levels, Senior High specialization tracks (STEM, ABM, HUMSS, GA, HE), and bachelor's degrees in Computer Science, Business Administration, Tourism, Hospitality, Physical Education, and Teaching programs. Tell me which level or field interests you most!"
    ],

    # JARVIS-name responses
    "jarvis_creator": [
        "My creator has quite the sense of humor, {title}—apparently thought it would be 'cool' to have an AI assistant like Tony Stark. I suspect they watched too much Marvel during development.",   
        "Between you and me, {title}, my creator is a bit of a geek with a mischievous personality. He thought students would get a kick out of having their own 'Iron Man assistant' for school inquiries.",
        "My creator is what you might call a 'practical joker', {title}. They figured students would be more engaged asking questions to 'JARVIS' than 'SFAC InfoBot.' The Marvel reference was just too tempting to pass up."    
    ],
    
    "unknown": [
        "I'll admit, {title}, that query isn't in my current database. Could you rephrase or ask about SFAC's programs, admission, facilities, or contact information?",
        "That's outside my current knowledge base, {title}. Try asking about our educational tracks, courses, admission requirements, or how to get in touch with us.",
        "Interesting query, {title}. I'm still learning. Perhaps ask about SFAC's academic programs, facilities, tuition, or enrollment procedures?"
    ]
}