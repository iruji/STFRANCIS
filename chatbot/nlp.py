# import re
# from datetime import datetime
# from difflib import get_close_matches
# from intents import intents

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

# def detect_specific_course_from_context(user_input):
#     """
#     Detect specific course references in informational queries
#     This is the key function that was missing!
#     """
#     text = user_input.lower().strip()
    
#     # Extract the subject after common informational patterns
#     context_patterns = [
#         r'\b(?:tell me about|about|info (?:on|about))\s+(.+)',
#         r'\bwhat (?:is|are)\s+(.+)',
#         r'\bhow (?:do|can|to)\s+(.+)',
#         r'\bwhere (?:is|are|can)\s+(.+)'
#     ]
    
#     query_subject = None
#     for pattern in context_patterns:
#         match = re.search(pattern, text)
#         if match:
#             query_subject = match.group(1).strip()
#             break
    
#     if not query_subject:
#         return None
    
#     # Direct course/program mapping - this is what was missing!
#     course_indicators = {
#         # Computer Science & Technology
#         'cs': 'computer_science',
#         'computer science': 'computer_science',
#         'programming': 'computer_science',
#         'coding': 'computer_science',
#         'software': 'computer_science',
#         'it': 'computer_science',
#         'information technology': 'computer_science',
#         'computer technology': 'computer_technology',
#         'computer tech': 'computer_technology',
#         'associate computer': 'computer_technology',
#         'act': 'computer_technology',
        
#         # Senior High Tracks
#         'stem': 'stem',
#         'science technology engineering mathematics': 'stem',
#         'abm': 'abm',
#         'accountancy business management': 'abm',
#         'business management': 'abm',
#         'humss': 'humss',
#         'humanities social sciences': 'humss',
#         'ga': 'ga',
#         'general academics': 'ga',
#         'he': 'he',
#         'home economics': 'he',
#         'culinary': 'he',
#         'cookery': 'he',
        
#         # Business & Tourism
#         'tourism': 'tourism',
#         'tm': 'tourism',
#         'tourism management': 'tourism',
#         'travel': 'tourism',
#         'hospitality': 'hospitality',
#         'hm': 'hospitality',  # This was the key missing mapping!
#         'hospitality management': 'hospitality',
#         'hotel management': 'hospitality',
#         'business': 'business_admin',
#         'ba': 'business_admin',
#         'business administration': 'business_admin',
#         'business admin': 'business_admin',
#         'bsba': 'business_admin',
#         'operations management': 'business_admin',
#         'financial management': 'business_admin',
#         'marketing management': 'business_admin',
#         'om': 'business_admin',
#         'fm': 'business_admin',
#         'mm': 'business_admin',
        
#         # Education Programs
#         'physical education': 'physical_education',
#         'pe': 'physical_education',
#         'bped': 'physical_education',
#         'sports': 'physical_education',
#         'coaching': 'physical_education',
#         'early childhood education': 'early_childhood_ed',
#         'early childhood': 'early_childhood_ed',
#         'ece': 'early_childhood_ed',
#         'preschool education': 'early_childhood_ed',
#         'elementary education': 'elementary_ed',
#         'elem ed': 'elementary_ed',
#         'beed': 'elementary_ed',
#         'primary education': 'elementary_ed',
#         'grade school education': 'elementary_ed',
#         'secondary education': 'secondary_ed',
#         'sec ed': 'secondary_ed',
#         'bsed': 'secondary_ed',
#         'high school education': 'secondary_ed',
#         'teaching': 'secondary_ed',
#         'education': 'secondary_ed',
        
#         # Basic Education Levels
#         'preschool': 'preschool',
#         'nursery': 'preschool',
#         'kindergarten': 'preschool',
#         'kinder': 'preschool',
#         'elementary': 'grade_school',
#         'elem': 'grade_school',
#         'grade school': 'grade_school',
#         'primary': 'grade_school',
#         'junior high': 'junior_high',
#         'jhs': 'junior_high',
#         'junior highschool': 'junior_high',
#         'secondary': 'junior_high',
#         'senior high': 'senior_high',
#         'shs': 'senior_high',
#         'senior highschool': 'senior_high',
        
#         # Website content (lower priority in this context)
#         'sfac': 'website_about',
#         'school': 'website_about',
#         'the school': 'website_about',
#         'the college': 'website_about',
#         'departments': 'website_departments',
#         'student services': 'website_student_services',
#         'services': 'website_student_services',
#         'enrollment': 'website_enrollment',
#         'online grades': 'website_online_grade',
#         'grades': 'website_online_grade',
#         'gcs': 'website_gcs',
#         'opac': 'website_opac',
#         'library': 'website_opac',
#         'alumni': 'website_alumni',
#         'contact': 'website_contact',
#         'locations': 'website_locations',
#         'location': 'website_locations'
#     }
    
#     # Check for exact matches first
#     if query_subject in course_indicators:
#         return course_indicators[query_subject]
    
#     # Check for partial matches WITH WORD BOUNDARIES to avoid false matches
#     # This prevents 'he' from matching 'the', 'tm' issues, etc.
#     for indicator, intent in course_indicators.items():
#         # Use word boundaries to prevent false matches like 'he' in 'the'
#         pattern = r'\b' + re.escape(indicator) + r'\b'
#         if re.search(pattern, query_subject):
#             return intent
    
#     return None

# def calculate_intent_scores(user_input):
#     """
#     Calculate scores for all intents based on keyword matching
#     Returns dictionary of intent: score pairs
#     """
#     text = user_input.lower().strip()
#     text_words = set(text.split())
#     normalized_text_words = {normalize_word(word) for word in text_words}
#     normalized_text = ' '.join(normalized_text_words)
    
#     all_scores = {}
    
#     # Phase 1: Exact phrase matching (highest priority)
#     for intent, keywords in intents.items():
#         phrase_score = 0
#         for keyword in keywords:
#             if keyword in text:
#                 word_count = len(keyword.split())
#                 if word_count > 1:
#                     phrase_score += word_count * 10  # Multi-word phrases get high scores
#                 else:
#                     phrase_score += 5  # Single word exact matches
        
#         if phrase_score > 0:
#             all_scores[intent] = phrase_score
    
#     # Phase 2: Individual word matching with smart weighting
#     for intent, keywords in intents.items():
#         word_score = 0
#         matched_words = set()
        
#         for keyword in keywords:
#             keyword_words = set(keyword.split())
#             matches = keyword_words.intersection(text_words)
            
#             if matches:
#                 for word in matches:
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
#                         word_score += 2   # Low for generic query words
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
    
#     return all_scores

# def apply_context_adjustments(scores, user_input):
#     """
#     Apply context-specific score adjustments
#     """
#     text = user_input.lower().strip()
    
#     # Context pattern detection
#     informational_patterns = [
#         r'\b(?:tell me about|about|info (?:on|about))\s+',
#         r'\bwhat (?:is|are)\s+',
#         r'\bhow (?:do|can|to)\s+',
#         r'\bwhere (?:is|are|can)\s+'
#     ]
    
#     is_informational_query = any(re.search(pattern, text) for pattern in informational_patterns)
    
#     if is_informational_query:
#         # FIRST: Check for specific course detection - this takes absolute priority!
#         specific_course = detect_specific_course_from_context(user_input)
#         if specific_course and specific_course in scores:
#             # Massively boost the specific course intent
#             scores[specific_course] += 50  # Much higher than any other boost
            
#             # Suppress generic "about" responses when we have specific course matches
#             if specific_course != 'website_about':
#                 if 'website_about' in scores:
#                     scores['website_about'] = max(1, scores['website_about'] - 30)
#                 if 'identity' in scores:
#                     scores['identity'] = max(1, scores['identity'] - 30)
        
#         # THEN: Apply general boosts (but they won't overcome the specific course boost)
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
#             if intent in scores:
#                 scores[intent] += 15  # Standard boost for content intents
        
#         # Penalize identity intent in informational context
#         if 'identity' in scores:
#             scores['identity'] = max(1, scores['identity'] - 20)
    
#     return scores

# def fuzzy_match_fallback(user_input):
#     """
#     Fuzzy matching as final fallback for intent detection
#     """
#     text = user_input.lower().strip()
    
#     for intent, keywords in intents.items():
#         matches = get_close_matches(text, keywords, n=1, cutoff=0.85)
#         if matches:
#             return intent
    
#     return None

# def enhanced_detect_intent(user_input):
#     """
#     Enhanced intent detection with modular scoring system
#     """
#     text = user_input.lower().strip()
    
#     # PRIORITY CHECK: Handle specific grade numbers first
#     grade_num, grade_level = detect_specific_grade(user_input)
#     if grade_num is not None and grade_level is not None:
#         return grade_level
    
#     # PRIORITY CHECK 2: Direct course detection for informational queries
#     if any(pattern in text for pattern in ['tell me about', 'about', 'what is', 'info about']):
#         specific_course = detect_specific_course_from_context(user_input)
#         if specific_course:
#             return specific_course
    
#     # Calculate base scores for all intents
#     all_scores = calculate_intent_scores(user_input)
    
#     # Apply context-specific adjustments
#     all_scores = apply_context_adjustments(all_scores, user_input)
    
#     # Handle special cases for informational queries
#     if 'about' in text and any(word in text for word in ['tell', 'info', 'information', 'details']):
#         if 'identity' in all_scores and any(intent.startswith('website_') for intent in all_scores):
#             # If we have both identity and website intents, prefer website
#             website_scores = {k: v for k, v in all_scores.items() if k.startswith('website_')}
#             if website_scores:
#                 best_website = max(website_scores.items(), key=lambda x: x[1])
#                 if best_website[1] >= all_scores.get('identity', 0):
#                     return best_website[0]
    
#     # Return best match with minimum threshold
#     if all_scores:
#         # Filter out very low scores
#         filtered_scores = {k: v for k, v in all_scores.items() if v >= 3}
        
#         if filtered_scores:
#             best_intent, best_score = max(filtered_scores.items(), key=lambda x: x[1])
            
#             # Additional validation: make sure the match makes sense
#             if best_score >= 8:  # Higher threshold for better accuracy
#                 return best_intent
    
#     # Fuzzy matching as final fallback
#     fuzzy_result = fuzzy_match_fallback(user_input)
#     if fuzzy_result:
#         return fuzzy_result
    
#     return "unknown"


# def debug_scoring(user_input):
#     """Debug function to show scoring breakdown for intent detection"""
#     text = user_input.lower().strip()
#     text_words = set(text.split())
    
#     print(f"Input: '{user_input}'")
#     print(f"Text words: {text_words}")
    
#     # Check specific course detection first
#     specific_course = detect_specific_course_from_context(user_input)
#     if specific_course:
#         print(f"SPECIFIC COURSE DETECTED: {specific_course}")
    
#     # Show scoring for relevant intents
#     relevant_intents = ['computer_science', 'website_about', 'course', 'identity', 'hospitality', 'tourism']
    
#     for intent in relevant_intents:
#         if intent in intents:
#             score = 0
#             matched_words = []
            
#             for keyword in intents[intent]:
#                 keyword_words = set(keyword.split())
#                 matches = keyword_words.intersection(text_words)
                
#                 if matches:
#                     for word in matches:
#                         # Smart weighting based on word specificity
#                         if word in ['cs', 'stem', 'abm', 'humss', 'ga', 'he', 'jhs', 'shs', 'bsba', 'opac', 'gcs']:
#                             word_score = 25  # Very high for specific abbreviations
#                         elif word in ['programming', 'coding', 'tourism', 'hospitality', 'culinary', 'coaching']:
#                             word_score = 20  # High for course-specific terms
#                         elif word in ['science', 'technology', 'engineering', 'mathematics', 'business', 'management']:
#                             word_score = 15  # Medium-high for field-specific terms
#                         elif word in ['enrollment', 'admission', 'tuition', 'facilities']:
#                             word_score = 12  # Medium for school-specific terms
#                         elif word in ['department', 'departments', 'services', 'contact', 'location']:
#                             word_score = 10  # Medium for navigation terms
#                         elif word in ['education', 'degree', 'program', 'course']:
#                             word_score = 8   # Medium-low for general academic terms
#                         elif word in ['preschool', 'elementary', 'junior', 'senior', 'grade', 'level']:
#                             word_score = 7   # Medium-low for level terms
#                         elif word in ['about', 'tell', 'what', 'how', 'where']:
#                             word_score = 2   # Low for generic query words
#                         else:
#                             word_score = 5   # Standard score for other words
                        
#                         score += word_score
#                         matched_words.append(f"{word}({word_score})")
            
#             # Context bonus for informational queries
#             if "tell me about" in text and intent in ['computer_science', 'hospitality', 'tourism']:
#                 score += 15
#                 matched_words.append("context_bonus(15)")
            
#             # Specific course bonus
#             if specific_course == intent:
#                 score += 50
#                 matched_words.append("SPECIFIC_COURSE_BONUS(50)")
            
#             if score > 0:
#                 print(f"{intent}: {score} points - {matched_words}")
#             else:
#                 print(f"{intent}: 0 points - no matches")
    
#     print(f"\nFinal detection: {enhanced_detect_intent(user_input)}")


# def test_problematic_cases():
#     """Test cases that were previously problematic"""
#     test_cases = [
#         # The main problem case
#         ("tell me about", "unknown"),  # Should not trigger identity
#         ("tell me about sfac", "website_about"),
#         ("tell me about the school", "website_about"),
        
#         # Computer Science variations
#         ("tell me about cs", "computer_science"),  # This should now work!
#         ("tell me about computer science", "computer_science"),
#         ("tell me about programming", "computer_science"),
#         ("tell me about coding", "computer_science"),
        
#         # Business & Tourism (the main issue)
#         ("tell me about hm", "hospitality"),  # This should now work!
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
#     print("Testing Previously Problematic Cases:")
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