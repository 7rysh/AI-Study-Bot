def chunk_text(text: str, chunk_size=500, overlap=50) -> list[str]:

    chunks = []

    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            for sep in ['. ', '\n', ' ']:
                idc = text.rfind(sep,start,end)

                if idc != -1 and idc + 1 > start:
                    end = idc + 1
                    break

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        new_start = end - overlap            
                
        start = new_start if new_start > start else start + chunk_size

    return chunks