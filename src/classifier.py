from werkzeug.datastructures import FileStorage
from fuzzywuzzy import fuzz

file_name_classifications = set(["drivers_license", "bank_statement", "invoice"])
text_classifications = {
    "drivers_license": [["drivers", "license"], ["driving", "license"], ["driver", "license"]],
    "bank_statement": [["bank", "statement"], ["bank", "stmt"]],
    "invoice": [["invoice"], ["bill"]]
}
def classify_file(file: FileStorage, text: str):
    filename = file.filename.lower()
    
    for classification in file_name_classifications: 
        if classification in filename:
            return classification 
    
    words = set(text.lower().split())
    for classification, keyword_sets in text_classifications.items():
        for keywords in keyword_sets:
            # fuzzy searching
            if all(any(fuzz.ratio(keyword, word) > 85 for word in words) for keyword in keywords):
                return classification
        
    return "unknown file"

