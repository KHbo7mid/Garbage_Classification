from enum import Enum
from typing import Dict

class WasteCategory(str, Enum):
    BIODEGRADABLE = "biodegradable"
    RECYCLABLE = "recyclable"
    NON_RECYCLABLE = "non_recyclable"

# List of class names predicted by your model
CLASS_NAMES = [
    'BIODEGRADABLE', 'CARDBOARD', 'GLASS', 'METAL', 'PAPER', 'PLASTIC'
]

# Mapping from classes to waste categories
WASTE_CATEGORY_MAPPING: Dict[str, WasteCategory] = {
    'BIODEGRADABLE': WasteCategory.BIODEGRADABLE,
    'CARDBOARD': WasteCategory.RECYCLABLE,
    'GLASS': WasteCategory.RECYCLABLE,
    'METAL': WasteCategory.RECYCLABLE,
    'PAPER': WasteCategory.RECYCLABLE,
    'PLASTIC': WasteCategory.RECYCLABLE,
}

# Recycling tips per class
RECYCLING_TIPS: Dict[str, str] = {
    'BIODEGRADABLE': "Compost with other organic waste. Avoid mixing with plastics.",
    'CARDBOARD': "Flatten boxes to save space. Remove any tape or plastic.",
    'GLASS': "Rinse containers before recycling. Separate by color if required.",
    'METAL': "Clean cans before recycling. Aluminum and steel can be recycled together.",
    'PAPER': "Keep dry and clean. Remove any plastic windows from envelopes.",
    'PLASTIC': "Check recycling symbols. Rinse and crush containers to save space.",
}
