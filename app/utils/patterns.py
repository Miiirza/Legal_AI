import re

def extract_pattern_schemme(text):
    pattern = r"(ESQUEMA.?\s*(\s*[\w\s\(\)\+\-\.\,\?\¿áéíóúÁÉÍÓÚñÑ\/\\]+:\s*null;?)*\s*)"
    find = re.findall(pattern, text)

    if len(find) > 0:
        return str(find[0])
    elif "ESQUEMA" in text or "null" in text:
        return "ERROR"
    else:
        return "NO"

def extract_pattern_list_values(text):
    text = text.replace("\\n", ";")
    text = text.replace("\n", ";")
    text = text.replace("\r\n", ";")
    text = text.replace("*", ";")

    pattern_values_null = r"\w[\w\s\(\)\+\-\.\,\?\¿áéíóúÁÉÍÓÚñÑ\/\\]*:\s*null"
    pattern_values_done = r"\w[\w\s\(\)\+\-\.\,\?\¿áéíóúÁÉÍÓÚñÑ\/\\]*:\s*(?!null\b)[\w\s\(\)\+\-\.\,\?\¿áéíóúÁÉÍÓÚñÑ]+"

    find_null = re.findall(pattern_values_null, text)
    find_done = re.findall(pattern_values_done, text)
    find_done = [done for done in find_done if "null" not in done]

    return {"Done": find_done, "Null": find_null}

def delete_headers(text):
    return re.sub(r'^#.*\n?', '', text, flags=re.MULTILINE)