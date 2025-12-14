<?php
/**
 * NLP Functions for Intent Detection
 * Converted from Python nlp.py to PHP
 */

require_once 'intents.php';

// Constants
define('MAX_MESSAGE_LENGTH', 500);
define('MAX_NAME_LENGTH', 50);

/**
 * Generate time-appropriate greeting
 * 
 * @return string Time-aware greeting
 */
date_default_timezone_set('Asia/Manila');

function getTimeAwareGreeting() {
    $hour = (int)date('G');
    
    if ($hour >= 5 && $hour < 12) {
        return "Good morning";
    } elseif ($hour >= 12 && $hour < 18) {
        return "Good afternoon";
    } else {
        return "Good evening";
    }
}

/**
 * Extract name from user input safely
 * 
 * @param string $userInput User's message
 * @return string|null Extracted name or null
 */
function extractNameSafely($userInput) {
    $text = strtolower(trim($userInput));
    
    $patterns = [
        '/my name is\s+([a-zA-Z\s]{2,20})/' => 1,
        '/call me\s+([a-zA-Z\s]{2,20})/' => 1,
        "/i(?:'m|\s+am)\s+([a-zA-Z]{2,15})(?:\s|$)/" => 1,
    ];
    
    foreach ($patterns as $pattern => $group) {
        if (preg_match($pattern, $text, $matches)) {
            $potentialName = trim($matches[$group]);
            $potentialName = ucwords($potentialName);
            
            if (isValidName($potentialName)) {
                return $potentialName;
            }
        }
    }
    
    return null;
}

/**
 * Validate if a string is a valid name
 * 
 * @param string $name Potential name to validate
 * @return bool True if valid name
 */
function isValidName($name) {
    if (empty($name) || strlen(trim($name)) < 2 || strlen($name) > MAX_NAME_LENGTH) {
        return false;
    }
    
    // Allow letters, spaces, hyphens, apostrophes
    if (!preg_match("/^[a-zA-Z\s\-']{2,50}$/", $name)) {
        return false;
    }
    
    // No multiple consecutive spaces
    if (strpos($name, '  ') !== false) {
        return false;
    }
    
    // Max 3 words
    if (count(explode(' ', $name)) > 3) {
        return false;
    }
    
    // Don't accept common non-name words
    $commonWords = [
        'happy', 'sad', 'confused', 'sure', 'okay', 'fine', 'good', 'bad',
        'interested', 'excited', 'worried', 'concerned', 'ready', 'done',
        'sorry', 'welcome', 'thanks', 'here', 'there', 'studying', 'learning'
    ];
    
    if (in_array(strtolower($name), $commonWords)) {
        return false;
    }
    
    return true;
}

/**
 * Detect if user is trying to share their name
 * 
 * @param string $userInput User's message
 * @return bool True if memory intent detected
 */
function detectMemoryIntent($userInput) {
    $patterns = [
        '/my name is/',
        "/i(?:'m|\s+am)\s+[a-zA-Z]{2,15}(?:\s|$)/",
        '/call me\s+[a-zA-Z]/',
        '/you can call me/'
    ];
    
    $text = strtolower($userInput);
    
    foreach ($patterns as $pattern) {
        if (preg_match($pattern, $text)) {
            return true;
        }
    }
    
    return false;
}

/**
 * Simple plural normalization
 * 
 * @param string $word Word to normalize
 * @return string Normalized word
 */
function normalizeWord($word) {
    if (strlen($word) > 3 && substr($word, -1) === 's') {
        return substr($word, 0, -1);
    }
    return $word;
}

/**
 * Detect specific grade numbers
 * 
 * @param string $userInput User's message
 * @return array [grade_number, level_category] or [null, null]
 */
function detectSpecificGrade($userInput) {
    $text = strtolower(trim($userInput));
    
    $gradePatterns = [
        '/\bgrade\s*(\d{1,2})\b/',
        '/\b(\d{1,2})(?:st|nd|rd|th)?\s*grade\b/',
        '/\blevel\s*(\d{1,2})\b/',
        '/\byear\s*(\d{1,2})\b/'
    ];
    
    foreach ($gradePatterns as $pattern) {
        if (preg_match($pattern, $text, $matches)) {
            $gradeNum = (int)$matches[1];
            
            if ($gradeNum == 0) {
                return [$gradeNum, "preschool"];
            } elseif ($gradeNum >= 1 && $gradeNum <= 6) {
                return [$gradeNum, "grade_school"];
            } elseif ($gradeNum >= 7 && $gradeNum <= 10) {
                return [$gradeNum, "junior_high"];
            } elseif ($gradeNum >= 11 && $gradeNum <= 12) {
                return [$gradeNum, "senior_high"];
            } else {
                return [$gradeNum, null];
            }
        }
    }
    
    return [null, null];
}

/**
 * Detect specific course from context
 * 
 * @param string $userInput User's message
 * @return string|null Detected course intent or null
 */
function detectSpecificCourseFromContext($userInput) {
    $text = strtolower(trim($userInput));
    
    // Extract the subject after common informational patterns
    $contextPatterns = [
        '/\b(?:tell me about|about|info (?:on|about))\s+(.+)/',
        '/\bwhat (?:is|are)\s+(.+)/',
        '/\bhow (?:do|can|to)\s+(.+)/',
        '/\bwhere (?:is|are|can)\s+(.+)/'
    ];
    
    $querySubject = null;
    foreach ($contextPatterns as $pattern) {
        if (preg_match($pattern, $text, $matches)) {
            $querySubject = trim($matches[1]);
            break;
        }
    }
    
    if (!$querySubject) {
        return null;
    }
    
    // Direct course/program mapping
    $courseIndicators = [
        // Computer Science & Technology
        'cs' => 'computer_science',
        'computer science' => 'computer_science',
        'programming' => 'computer_science',
        'coding' => 'computer_science',
        'software' => 'computer_science',
        'it' => 'computer_science',
        'information technology' => 'computer_science',
        'computer technology' => 'computer_technology',
        'computer tech' => 'computer_technology',
        'associate computer' => 'computer_technology',
        'act' => 'computer_technology',
        
        // Senior High Tracks
        'stem' => 'stem',
        'science technology engineering mathematics' => 'stem',
        'abm' => 'abm',
        'accountancy business management' => 'abm',
        'business management' => 'abm',
        'humss' => 'humss',
        'humanities social sciences' => 'humss',
        'ga' => 'ga',
        'general academics' => 'ga',
        'he' => 'he',
        'home economics' => 'he',
        'culinary' => 'he',
        'cookery' => 'he',
        
        // Business & Tourism
        'tourism' => 'tourism',
        'tm' => 'tourism',
        'tourism management' => 'tourism',
        'travel' => 'tourism',
        'hospitality' => 'hospitality',
        'hm' => 'hospitality',
        'hospitality management' => 'hospitality',
        'hotel management' => 'hospitality',
        'business' => 'business_admin',
        'ba' => 'business_admin',
        'business administration' => 'business_admin',
        'business admin' => 'business_admin',
        'bsba' => 'business_admin',
        'operations management' => 'business_admin',
        'financial management' => 'business_admin',
        'marketing management' => 'business_admin',
        'om' => 'business_admin',
        'fm' => 'business_admin',
        'mm' => 'business_admin',
        
        // Education Programs
        'physical education' => 'physical_education',
        'pe' => 'physical_education',
        'bped' => 'physical_education',
        'sports' => 'physical_education',
        'coaching' => 'physical_education',
        'early childhood education' => 'early_childhood_ed',
        'early childhood' => 'early_childhood_ed',
        'ece' => 'early_childhood_ed',
        'preschool education' => 'early_childhood_ed',
        'elementary education' => 'elementary_ed',
        'elem ed' => 'elementary_ed',
        'beed' => 'elementary_ed',
        'primary education' => 'elementary_ed',
        'grade school education' => 'elementary_ed',
        'secondary education' => 'secondary_ed',
        'sec ed' => 'secondary_ed',
        'bsed' => 'secondary_ed',
        'high school education' => 'secondary_ed',
        'teaching' => 'secondary_ed',
        'education' => 'secondary_ed',
        
        // Basic Education Levels
        'preschool' => 'preschool',
        'nursery' => 'preschool',
        'kindergarten' => 'preschool',
        'kinder' => 'preschool',
        'elementary' => 'grade_school',
        'elem' => 'grade_school',
        'grade school' => 'grade_school',
        'primary' => 'grade_school',
        'junior high' => 'junior_high',
        'jhs' => 'junior_high',
        'junior highschool' => 'junior_high',
        'secondary' => 'junior_high',
        'senior high' => 'senior_high',
        'shs' => 'senior_high',
        'senior highschool' => 'senior_high',
        
        // Website content
        'sfac' => 'website_about',
        'school' => 'website_about',
        'the school' => 'website_about',
        'the college' => 'website_about',
        'departments' => 'website_departments',
        'student services' => 'website_student_services',
        'services' => 'website_student_services',
        'enrollment' => 'website_enrollment',
        'online grades' => 'website_online_grade',
        'grades' => 'website_online_grade',
        'gcs' => 'website_gcs',
        'opac' => 'website_opac',
        'library' => 'website_opac',
        'alumni' => 'website_alumni',
        'contact' => 'website_contact',
        'locations' => 'website_locations',
        'location' => 'website_locations'
    ];
    
    // Check for exact matches first
    if (isset($courseIndicators[$querySubject])) {
        return $courseIndicators[$querySubject];
    }
    
    // Check for partial matches with word boundaries
    foreach ($courseIndicators as $indicator => $intent) {
        $pattern = '/\b' . preg_quote($indicator, '/') . '\b/';
        if (preg_match($pattern, $querySubject)) {
            return $intent;
        }
    }
    
    return null;
}

/**
 * Calculate intent scores for all intents
 * 
 * @param string $userInput User's message
 * @return array Intent scores
 */
function calculateIntentScores($userInput) {
    global $intents;
    
    $text = strtolower(trim($userInput));
    $textWords = array_unique(explode(' ', $text));
    
    $normalizedTextWords = [];
    foreach ($textWords as $word) {
        $normalizedTextWords[] = normalizeWord($word);
    }
    $normalizedTextWords = array_unique($normalizedTextWords);
    $normalizedText = implode(' ', $normalizedTextWords);
    
    $allScores = [];
    
    // Phase 1: Exact phrase matching
    foreach ($intents as $intent => $keywords) {
        $phraseScore = 0;
        
        foreach ($keywords as $keyword) {
            if (strpos($text, $keyword) !== false) {
                $wordCount = count(explode(' ', $keyword));
                if ($wordCount > 1) {
                    $phraseScore += $wordCount * 10;
                } else {
                    $phraseScore += 5;
                }
            }
        }
        
        if ($phraseScore > 0) {
            $allScores[$intent] = $phraseScore;
        }
    }
    
    // Phase 2: Individual word matching
    foreach ($intents as $intent => $keywords) {
        $wordScore = 0;
        $matchedWords = [];
        
        foreach ($keywords as $keyword) {
            $keywordWords = explode(' ', $keyword);
            $matches = array_intersect($keywordWords, $textWords);
            
            if (!empty($matches)) {
                foreach ($matches as $word) {
                    // Smart weighting based on word specificity
                    $specificAbbreviations = ['cs', 'stem', 'abm', 'humss', 'ga', 'he', 'jhs', 'shs', 'bsba', 'opac', 'gcs'];
                    $courseSpecific = ['programming', 'coding', 'tourism', 'hospitality', 'culinary', 'coaching'];
                    $fieldSpecific = ['science', 'technology', 'engineering', 'mathematics', 'business', 'management'];
                    $schoolSpecific = ['enrollment', 'admission', 'tuition', 'facilities'];
                    $navigation = ['department', 'departments', 'services', 'contact', 'location'];
                    $academic = ['education', 'degree', 'program', 'course'];
                    $level = ['preschool', 'elementary', 'junior', 'senior', 'grade', 'level'];
                    $generic = ['about', 'tell', 'what', 'how', 'where'];
                    
                    if (in_array($word, $specificAbbreviations)) {
                        $wordScore += 25;
                    } elseif (in_array($word, $courseSpecific)) {
                        $wordScore += 20;
                    } elseif (in_array($word, $fieldSpecific)) {
                        $wordScore += 15;
                    } elseif (in_array($word, $schoolSpecific)) {
                        $wordScore += 12;
                    } elseif (in_array($word, $navigation)) {
                        $wordScore += 10;
                    } elseif (in_array($word, $academic)) {
                        $wordScore += 8;
                    } elseif (in_array($word, $level)) {
                        $wordScore += 7;
                    } elseif (in_array($word, $generic)) {
                        $wordScore += 2;
                    } else {
                        $wordScore += 5;
                    }
                    
                    $matchedWords[] = $word;
                }
            }
        }
        
        // Bonus for multiple word matches
        if (count(array_unique($matchedWords)) > 1) {
            $wordScore += count(array_unique($matchedWords)) * 3;
        }
        
        // Add to total scores
        if ($wordScore > 0) {
            if (isset($allScores[$intent])) {
                $allScores[$intent] += $wordScore;
            } else {
                $allScores[$intent] = $wordScore;
            }
        }
    }
    
    return $allScores;
}

/**
 * Apply context-specific adjustments to scores
 * 
 * @param array $scores Current intent scores
 * @param string $userInput User's message
 * @return array Adjusted scores
 */
function applyContextAdjustments($scores, $userInput) {
    $text = strtolower(trim($userInput));
    
    // Context pattern detection
    $informationalPatterns = [
        '/\b(?:tell me about|about|info (?:on|about))\s+/',
        '/\bwhat (?:is|are)\s+/',
        '/\bhow (?:do|can|to)\s+/',
        '/\bwhere (?:is|are|can)\s+/'
    ];
    
    $isInformationalQuery = false;
    foreach ($informationalPatterns as $pattern) {
        if (preg_match($pattern, $text)) {
            $isInformationalQuery = true;
            break;
        }
    }
    
    if ($isInformationalQuery) {
        // Check for specific course detection - absolute priority
        $specificCourse = detectSpecificCourseFromContext($userInput);
        if ($specificCourse && isset($scores[$specificCourse])) {
            $scores[$specificCourse] += 50;
            
            // Suppress generic "about" responses
            if ($specificCourse !== 'website_about') {
                if (isset($scores['website_about'])) {
                    $scores['website_about'] = max(1, $scores['website_about'] - 30);
                }
                if (isset($scores['identity'])) {
                    $scores['identity'] = max(1, $scores['identity'] - 30);
                }
            }
        }
        
        // General boosts
        $websiteIntents = [
            'website_about', 'website_departments', 'website_basic_education', 
            'website_higher_education', 'website_student_services', 'website_enrollment',
            'website_online_grade', 'website_gcs', 'website_opac', 'website_alumni',
            'website_contact', 'website_locations'
        ];
        
        $courseIntents = [
            'computer_science', 'computer_technology', 'tourism', 'hospitality', 
            'business_admin', 'physical_education', 'early_childhood_ed', 
            'elementary_ed', 'secondary_ed', 'stem', 'abm', 'humss', 'ga', 'he',
            'preschool', 'grade_school', 'junior_high', 'senior_high'
        ];
        
        foreach (array_merge($websiteIntents, $courseIntents) as $intent) {
            if (isset($scores[$intent])) {
                $scores[$intent] += 15;
            }
        }
        
        // Penalize identity intent
        if (isset($scores['identity'])) {
            $scores['identity'] = max(1, $scores['identity'] - 20);
        }
    }
    
    return $scores;
}

/**
 * Fuzzy matching as fallback
 * 
 * @param string $userInput User's message
 * @return string|null Matched intent or null
 */
function fuzzyMatchFallback($userInput) {
    global $intents;
    
    $text = strtolower(trim($userInput));
    $bestMatch = null;
    $bestScore = 0;
    
    foreach ($intents as $intent => $keywords) {
        foreach ($keywords as $keyword) {
            similar_text($text, $keyword, $percent);
            if ($percent > 85 && $percent > $bestScore) {
                $bestMatch = $intent;
                $bestScore = $percent;
            }
        }
    }
    
    return $bestMatch;
}

/**
 * Enhanced intent detection with modular scoring system
 * 
 * @param string $userInput User's message
 * @return string Detected intent
 */
function enhancedDetectIntent($userInput) {
    $text = strtolower(trim($userInput));
    
    // PRIORITY CHECK: Handle specific grade numbers first
    list($gradeNum, $gradeLevel) = detectSpecificGrade($userInput);
    if ($gradeNum !== null && $gradeLevel !== null) {
        return $gradeLevel;
    }
    
    // PRIORITY CHECK 2: Direct course detection for informational queries
    $informationalKeywords = ['tell me about', 'about', 'what is', 'info about'];
    foreach ($informationalKeywords as $keyword) {
        if (strpos($text, $keyword) !== false) {
            $specificCourse = detectSpecificCourseFromContext($userInput);
            if ($specificCourse) {
                return $specificCourse;
            }
            break;
        }
    }
    
    // Calculate base scores
    $allScores = calculateIntentScores($userInput);
    
    // Apply context adjustments
    $allScores = applyContextAdjustments($allScores, $userInput);
    
    // Handle special cases for informational queries
    if (strpos($text, 'about') !== false) {
        $hasInfoWords = false;
        foreach (['tell', 'info', 'information', 'details'] as $word) {
            if (strpos($text, $word) !== false) {
                $hasInfoWords = true;
                break;
            }
        }
        
        if ($hasInfoWords) {
            if (isset($allScores['identity'])) {
                $websiteScores = [];
                foreach ($allScores as $intent => $score) {
                    if (strpos($intent, 'website_') === 0) {
                        $websiteScores[$intent] = $score;
                    }
                }
                
                if (!empty($websiteScores)) {
                    arsort($websiteScores);
                    $bestWebsite = key($websiteScores);
                    if ($websiteScores[$bestWebsite] >= ($allScores['identity'] ?? 0)) {
                        return $bestWebsite;
                    }
                }
            }
        }
    }
    
    // Return best match with minimum threshold
    if (!empty($allScores)) {
        $filteredScores = array_filter($allScores, function($score) {
            return $score >= 3;
        });
        
        if (!empty($filteredScores)) {
            arsort($filteredScores);
            reset($filteredScores);
            $bestIntent = key($filteredScores);
            $bestScore = current($filteredScores);
            
            if ($bestScore >= 8) {
                return $bestIntent;
            }
        }
    }
    
    // Fuzzy matching as final fallback
    $fuzzyResult = fuzzyMatchFallback($userInput);
    if ($fuzzyResult) {
        return $fuzzyResult;
    }
    
    return "unknown";
}
?>