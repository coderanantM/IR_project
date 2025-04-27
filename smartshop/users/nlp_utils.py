import re

def extract_preferences_from_text(text):
    extracted_data = {}
    text_lower = text.lower()

    # Department
    if re.search(r"\b(men|man|male)\b", text_lower):
        extracted_data['preferred_department'] = 'Men'
    elif re.search(r"\b(women|woman|female)\b", text_lower):
        extracted_data['preferred_department'] = 'Women'

    # Height (convert various inputs to cm)
    height_match = re.search(r"(\d+)\s*(?:cm|centimeters)\b", text_lower)
    if height_match:
        extracted_data['height_cm'] = int(height_match.group(1))
    else:
        # Example: 5 feet 10 inches -> cm
        feet_match = re.search(r"(\d+)\s*(?:'|foot|feet)\s*(\d+)?\s*(?:\"|inch|inches)?", text_lower)
        if feet_match:
            feet = int(feet_match.group(1))
            inches = int(feet_match.group(2) or 0)
            extracted_data['height_cm'] = int((feet * 30.48) + (inches * 2.54))

    # Weight (convert various inputs to kg)
    weight_match = re.search(r"(\d+)\s*(?:kg|kilograms)\b", text_lower)
    if weight_match:
        extracted_data['weight_kg'] = int(weight_match.group(1))
    else:
        pounds_match = re.search(r"(\d+)\s*(?:lb|lbs|pounds)\b", text_lower)
        if pounds_match:
            extracted_data['weight_kg'] = int(int(pounds_match.group(1)) * 0.453592)

    # Age Group (simple mapping)
    age_match = re.search(r"(\d+)\s*years old", text_lower)
    if age_match:
        age = int(age_match.group(1))
        if 18 <= age <= 24: extracted_data['age_group'] = '18-24'
        elif 25 <= age <= 34: extracted_data['age_group'] = '25-34'
        # ... add other age groups

    # Fit
    if re.search(r"slim\s*fit", text_lower): extracted_data['preferred_fit'] = 'slim'
    elif re.search(r"regular\s*fit", text_lower): extracted_data['preferred_fit'] = 'regular'
    elif re.search(r"relaxed\s*fit", text_lower): extracted_data['preferred_fit'] = 'relaxed'
    elif re.search(r"loose\s*fit", text_lower): extracted_data['preferred_fit'] = 'loose'
