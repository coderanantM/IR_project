import re

def extract_preferences_from_text(text):
    extracted_data = {}
    text_clean = re.sub(r'[^a-zA-Z0-9\.\'\"]', ' ', text).lower()  # Clean special chars
    
    # Department detection
    department_map = {
        r'\b(male|man|men|boys?)\b': 'Men',
        r'\b(female|woman|women|girls?)\b': 'Women'
    }
    for pattern, dept in department_map.items():
        if re.search(pattern, text_clean):
            extracted_data['preferred_department'] = dept
            break

    # Height parsing (supports cm/m/ft/in combinations)
    height_cm = None
    
    # Metric formats (cm/m)
    metric_match = re.search(
        r'(\d+\.?\d*)\s*(?:cm|centimetres?|meters?|m)\b', text_clean)
    if metric_match:
        value = float(metric_match.group(1))
        if 'm' in metric_match.group(0):  # Convert meters to cm
            height_cm = round(value * 100, 2)
        else:
            height_cm = round(value, 2)

    # Imperial formats (ft/in)
    if not height_cm:
        imperial_match = re.search(
            r'(?:(\d+)\s*[\'\u2032]?\s*(\d+\.?\d*)?[\"\u2033]?|'
            r'(\d+\.?\d*)\s*(?:ft|foot|feet|in|inch|inches))\b', text_clean)
        if imperial_match:
            feet = float(imperial_match.group(1) or 0)
            inches = float(imperial_match.group(2) or imperial_match.group(3) or 0)
            if feet > 10:  # Likely inches-only input
                inches = feet
                feet = 0
            height_cm = round((feet * 30.48) + (inches * 2.54), 2)

    if height_cm:
        extracted_data['height_cm'] = height_cm

    # Weight parsing
    weight_kg = None
    
    # Metric weights
    kg_match = re.search(
        r'(\d+\.?\d*)\s*(?:kgs?|kilograms?|kilo)\b', text_clean)
    if kg_match:
        weight_kg = round(float(kg_match.group(1)), 2)

    # Imperial weights
    if not weight_kg:
        lbs_match = re.search(
            r'(\d+\.?\d*)\s*(?:lbs?|pounds?)\b', text_clean)
        if lbs_match:
            weight_kg = round(float(lbs_match.group(1)) * 0.453592, 2)

    if weight_kg:
        extracted_data['weight_kg'] = weight_kg

    # Age group detection
    age_ranges = {
        (18, 24): '18-24',
        (25, 34): '25-34', 
        (35, 44): '35-44',
        (45, 54): '45-54',
        (55, 120): '55+'
    }
    
    age_match = re.search(
        r'(?:age|aged?)\s*(\d+)\b|'
        r'\b(\d+)\s*(?:years?|yrs?|yo)\b', text_clean)
    if age_match:
        age = int(age_match.group(1) or age_match.group(2))
        for (low, high), group in age_ranges.items():
            if low <= age <= high:
                extracted_data['age_group'] = group
                break

    # Fit preference with synonyms
    fit_map = {
        'slim': r'\b(slim|skinny|tight|close[- ]?fit)\b',
        'regular': r'\b(regular|standard|normal|classic)\b',
        'relaxed': r'\b(relaxed|loose|baggy|comfort)\b',
        'athletic': r'\b(athletic|muscle|sport)\b'
    }
    
    for fit_type, pattern in fit_map.items():
        if re.search(pattern, text_clean):
            extracted_data['preferred_fit'] = fit_type
            break

    # Debugging and validation
    if 'height_cm' in extracted_data and extracted_data['height_cm'] > 300:
        del extracted_data['height_cm']  # Invalid height
        
    if 'weight_kg' in extracted_data and extracted_data['weight_kg'] > 500:
        del extracted_data['weight_kg']  # Invalid weight

    print(f"Processed input: '{text}'")
    print(f"Extracted data: {extracted_data}")
    
    return extracted_data
