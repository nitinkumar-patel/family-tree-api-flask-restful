schema = {
    "type": "object",
    "properties": {
        "firstname":        {"type": "string"},
        "lastname":         {"type": "string"},
        "birthdate":        {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"},
        "email":            {"type": "string"},
        "street_address":   {"type": "string"},
        "city":             {"type": "string"},
        "state":            {"type": "string", "pattern": "^[A-Z]{2}$"},
        "zip":              {"type": "string", "pattern": "^[0-9]{5}$"},
        "phone":            {"type": "string", "pattern": "^[0-9]{3}-[0-9]{3}-[0-9]{4}$"},
        "parents":          {"type": "array"},
        "children":         {"type": "array"},
        "spouse":           {"type": "array"}
    },
    "required": ["firstname", "lastname", "birthdate", "email", "street_address", "city", "state", "zip", "phone"]
}