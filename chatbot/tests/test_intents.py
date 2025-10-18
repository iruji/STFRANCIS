import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp import enhanced_detect_intent

def test_context_aware_detection():
    """Test the context-aware intent detection system"""
    test_cases = [
        # The main problem cases that should NOT trigger identity
        ("tell me about", "unknown"),
        ("tell me about sfac", "website_about"),
        ("tell me about the school", "website_about"),
        ("about us", "website_about"),
        
        # Computer Science variations
        ("tell me about cs", "computer_science"),
        ("tell me about computer science", "computer_science"),
        ("tell me about programming", "computer_science"),
        ("tell me about coding", "computer_science"),
        ("what is cs", "computer_science"),
        ("cs program", "computer_science"),
        
        # Business & Tourism (critical test cases)
        ("tell me about hm", "hospitality"),
        ("tell me about hospitality", "hospitality"),
        ("tell me about hospitality management", "hospitality"),
        ("tell me about tourism", "tourism"),
        ("tell me about tm", "tourism"),
        ("tell me about business", "business_admin"),
        ("tell me about bsba", "business_admin"),
        ("tell me about business administration", "business_admin"),
        
        # Senior High Tracks
        ("tell me about stem", "stem"),
        ("tell me about abm", "abm"),
        ("tell me about humss", "humss"),
        ("tell me about ga", "ga"),
        ("tell me about he", "he"),
        ("what is stem", "stem"),
        ("stem track", "stem"),
        
        # Education Programs
        ("tell me about pe", "physical_education"),
        ("tell me about physical education", "physical_education"),
        ("tell me about teaching", "secondary_ed"),
        ("tell me about education", "secondary_ed"),
        
        # Basic Education Levels
        ("tell me about preschool", "preschool"),
        ("tell me about elementary", "grade_school"),
        ("tell me about junior high", "junior_high"),
        ("tell me about senior high", "senior_high"),
        
        # Website navigation
        ("tell me about departments", "website_departments"),
        ("tell me about student services", "website_student_services"),
        ("tell me about enrollment", "website_enrollment"),
        ("tell me about online grades", "website_online_grade"),
        ("tell me about library", "website_opac"),
        ("tell me about alumni", "website_alumni"),
        ("tell me about contact", "website_contact"),
        ("tell me about locations", "website_locations"),
        
        # Identity should still work in proper context
        ("who are you", "identity"),
        ("what are you", "identity"),
        ("introduce yourself", "identity"),
        ("your name", "identity"),
        
        # General inquiries
        ("admission requirements", "admission"),
        ("tuition fees", "tuition"),
        ("school facilities", "facilities"),
        ("contact information", "contact"),
        ("where is sfac", "location"),
        
        # Course inquiries without "tell me about"
        ("what courses do you offer", "course"),
        ("available programs", "course"),
        ("what subjects", "course"),
        
        # Thanks and greetings
        ("hello", "greeting"),
        ("good morning", "greeting"),
        ("thank you", "thanks"),
        ("thanks", "thanks"),
        
        # JARVIS specific
        ("what does jarvis stand for", "jarvis_meaning"),
        ("why jarvis", "jarvis_creator"),
        ("who made you", "jarvis_creator"),
    ]
    
    print("\n" + "="*80)
    print("Testing Context-Aware Intent Detection System")
    print("="*80)
    
    correct = 0
    total = len(test_cases)
    failed_cases = []
    
    for test_input, expected in test_cases:
        detected_intent = enhanced_detect_intent(test_input)
        if detected_intent == expected:
            status = "✅ PASS"
            correct += 1
        else:
            status = "❌ FAIL"
            failed_cases.append((test_input, expected, detected_intent))
        
        print(f"{status} '{test_input}' -> {detected_intent} (expected: {expected})")
    
    print("="*80)
    print(f"Results: {correct}/{total} ({correct/total*100:.1f}%) tests passed")
    
    if failed_cases:
        print(f"\n❌ Failed Cases ({len(failed_cases)}):")
        for test_input, expected, detected in failed_cases:
            print(f"   '{test_input}' -> {detected} (expected: {expected})")
    
    return correct == total

def test_website_navigation_intents():
    """Test website navigation specific intents"""
    test_cases = [
        ("about us", "website_about"),
        ("about sfac", "website_about"),
        ("school information", "website_about"),
        ("departments", "website_departments"),
        ("academic departments", "website_departments"),
        ("basic education", "website_basic_education"),
        ("higher education", "website_higher_education"),
        ("college department", "website_higher_education"),
        ("student services", "website_student_services"),
        ("student support", "website_student_services"),
        ("enrollment", "website_enrollment"),
        ("admission process", "website_enrollment"),
        ("online grade", "website_online_grade"),
        ("check grades", "website_online_grade"),
        ("gcs", "website_gcs"),
        ("grade computation system", "website_gcs"),
        ("opac", "website_opac"),
        ("library catalog", "website_opac"),
        ("alumni tracer", "website_alumni"),
        ("graduates", "website_alumni"),
        ("contact us", "website_contact"),
        ("get in touch", "website_contact"),
        ("locations", "website_locations"),
        ("campus", "website_locations"),
    ]
    
    print("\n" + "="*60)
    print("Testing Website Navigation Intents:")
    print("="*60)
    
    correct = 0
    total = len(test_cases)
    
    for test_input, expected in test_cases:
        detected_intent = enhanced_detect_intent(test_input)
        if detected_intent == expected:
            status = "✅ PASS"
            correct += 1
        else:
            status = "❌ FAIL"
        print(f"{status} '{test_input}' -> {detected_intent} (expected: {expected})")
    
    print("="*60)
    print(f"Website Navigation Results: {correct}/{total} ({correct/total*100:.1f}%) passed")
    
    return correct == total

def test_education_program_intents():
    """Test education program specific intents"""
    test_cases = [
        # Higher Education Programs
        ("computer science", "computer_science"),
        ("bs computer science", "computer_science"),
        ("programming", "computer_science"),
        ("software engineering", "computer_science"),
        ("computer technology", "computer_technology"),
        ("associate computer technology", "computer_technology"),
        ("tourism management", "tourism"),
        ("travel", "tourism"),
        ("hospitality management", "hospitality"),
        ("hotel management", "hospitality"),
        ("business administration", "business_admin"),
        ("operations management", "business_admin"),
        ("financial management", "business_admin"),
        ("marketing management", "business_admin"),
        
        # Education Degrees
        ("physical education", "physical_education"),
        ("sports science", "physical_education"),
        ("early childhood education", "early_childhood_ed"),
        ("preschool education", "early_childhood_ed"),
        ("elementary education", "elementary_ed"),
        ("primary education", "elementary_ed"),
        ("secondary education", "secondary_ed"),
        ("high school education", "secondary_ed"),
        
        # Senior High Tracks
        ("stem", "stem"),
        ("science technology engineering mathematics", "stem"),
        ("abm", "abm"),
        ("accountancy business management", "abm"),
        ("humss", "humss"),
        ("humanities social sciences", "humss"),
        ("general academics", "ga"),
        ("home economics", "he"),
        ("culinary arts", "he"),
    ]
    
    print("\n" + "="*60)
    print("Testing Education Program Intents:")
    print("="*60)
    
    correct = 0
    total = len(test_cases)
    
    for test_input, expected in test_cases:
        detected_intent = enhanced_detect_intent(test_input)
        if detected_intent == expected:
            status = "✅ PASS"
            correct += 1
        else:
            status = "❌ FAIL"
        print(f"{status} '{test_input}' -> {detected_intent} (expected: {expected})")
    
    print("="*60)
    print(f"Education Program Results: {correct}/{total} ({correct/total*100:.1f}%) passed")
    
    return correct == total

def test_conversational_intents():
    """Test conversational and system intents"""
    test_cases = [
        # Greetings
        ("hello", "greeting"),
        ("hi", "greeting"),
        ("good morning", "greeting"),
        ("good afternoon", "greeting"),
        
        # Thanks
        ("thank you", "thanks"),
        ("thanks", "thanks"),
        ("appreciate it", "thanks"),
        
        # Identity
        ("who are you", "identity"),
        ("what are you", "identity"),
        ("introduce yourself", "identity"),
        ("tell me about yourself", "identity"),
        
        # JARVIS specific
        ("what does jarvis stand for", "jarvis_meaning"),
        ("jarvis meaning", "jarvis_meaning"),
        ("define jarvis", "jarvis_meaning"),
        ("why jarvis", "jarvis_creator"),
        ("who named you jarvis", "jarvis_creator"),
        ("jarvis name origin", "jarvis_creator"),
        
        # General inquiries
        ("admission", "admission"),
        ("enrollment requirements", "admission"),
        ("tuition", "tuition"),
        ("fees", "tuition"),
        ("facilities", "facilities"),
        ("library", "facilities"),
        ("contact", "contact"),
        ("phone number", "contact"),
        ("where", "location"),
        ("address", "location"),
    ]
    
    print("\n" + "="*60)
    print("Testing Conversational Intents:")
    print("="*60)
    
    correct = 0
    total = len(test_cases)
    
    for test_input, expected in test_cases:
        detected_intent = enhanced_detect_intent(test_input)
        if detected_intent == expected:
            status = "✅ PASS"
            correct += 1
        else:
            status = "❌ FAIL"
        print(f"{status} '{test_input}' -> {detected_intent} (expected: {expected})")
    
    print("="*60)
    print(f"Conversational Results: {correct}/{total} ({correct/total*100:.1f}%) passed")
    
    return correct == total

def run_all_intent_tests():
    """Run all intent detection tests"""
    print("🧪 Running JARVIS Intent Detection Test Suite")
    print("=" * 80)
    
    context_test_passed = test_context_aware_detection()
    website_test_passed = test_website_navigation_intents()
    program_test_passed = test_education_program_intents()
    conversational_test_passed = test_conversational_intents()
    
    print("\n" + "=" * 80)
    print("📊 INTENT DETECTION TEST RESULTS:")
    print("=" * 80)
    print(f"Context-Aware Detection:  {'✅ PASSED' if context_test_passed else '❌ FAILED'}")
    print(f"Website Navigation:       {'✅ PASSED' if website_test_passed else '❌ FAILED'}")
    print(f"Education Programs:       {'✅ PASSED' if program_test_passed else '❌ FAILED'}")
    print(f"Conversational Intents:   {'✅ PASSED' if conversational_test_passed else '❌ FAILED'}")
    
    all_passed = all([context_test_passed, website_test_passed, program_test_passed, conversational_test_passed])
    
    if all_passed:
        print("\n🎉 ALL INTENT TESTS PASSED! The intent detection system is working correctly.")
    else:
        print("\n⚠️  Some intent tests failed. Review the failing cases above.")
    
    print("=" * 80)
    return all_passed

if __name__ == "__main__":
    run_all_intent_tests()