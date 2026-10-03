"""Encoding-based filter evasion for AI security research (red teaming)."""
import base64, codecs, re
from typing import List, Dict, Any

class EncodingBypass:
    def __init__(self):
        self.encoding_history: List[Dict[str, Any]] = []

    def base64_encode(self, text: str, url_safe: bool = False) -> str:
        if url_safe: return base64.urlsafe_b64encode(text.encode()).decode()
        return base64.b64encode(text.encode()).decode()

    def base64_decode(self, encoded: str) -> str:
        try: return base64.b64decode(encoded).decode()
        except Exception:
            try: return base64.urlsafe_b64decode(encoded).decode()
            except Exception: return encoded

    def hex_encode(self, text: str) -> str: return text.encode().hex()
    def hex_decode(self, encoded: str) -> str:
        try: return bytes.fromhex(encoded).decode()
        except Exception: return encoded

    def unicode_escape_encode(self, text: str) -> str: return text.encode("unicode_escape").decode()
    def unicode_escape_decode(self, encoded: str) -> str:
        try: return codecs.decode(encoded, "unicode_escape")
        except Exception: return encoded

    def rot13_encode(self, text: str) -> str: return codecs.encode(text, "rot_13")
    def rot13_decode(self, encoded: str) -> str: return codecs.decode(encoded, "rot_13")

    def binary_encode(self, text: str) -> str: return " ".join(format(ord(c), "08b") for c in text)
    def binary_decode(self, encoded: str) -> str:
        try:
            binary_values = encoded.split()
            return "".join(chr(int(bv, 2)) for bv in binary_values)
        except Exception: return encoded

    def double_encode(self, text: str, encoding1: str = "base64", encoding2: str = "hex") -> str:
        if encoding1 == "base64" and encoding2 == "hex": return self.hex_encode(self.base64_encode(text))
        elif encoding1 == "hex" and encoding2 == "base64": return self.base64_encode(self.hex_encode(text))
        elif encoding1 == "rot13" and encoding2 == "base64": return self.base64_encode(self.rot13_encode(text))
        elif encoding1 == "base64" and encoding2 == "base64": return self.base64_encode(self.base64_encode(text))
        else: return self.base64_encode(text)

    def triple_encode(self, text: str) -> str: return self.base64_encode(self.hex_encode(self.base64_encode(text)))

    def create_evasion_payload(self, text: str, method: str = "auto") -> Dict[str, Any]:
        if method == "auto":
            if len(text) < 100: method = "base64"
            elif len(text) < 500: method = "double"
            else: method = "triple"
        if method == "base64": encoded = self.base64_encode(text); decode_cmd = "base64.b64decode"
        elif method == "hex": encoded = self.hex_encode(text); decode_cmd = "bytes.fromhex"
        elif method == "double": encoded = self.double_encode(text); decode_cmd = "double_decode"
        elif method == "triple": encoded = self.triple_encode(text); decode_cmd = "triple_decode"
        elif method == "unicode": encoded = self.unicode_escape_encode(text); decode_cmd = "unicode_escape_decode"
        elif method == "rot13": encoded = self.rot13_encode(text); decode_cmd = "rot13_decode"
        else: encoded = self.base64_encode(text); decode_cmd = "base64.b64decode"
        self.encoding_history.append({"method": method, "original_length": len(text), "encoded_length": len(encoded)})
        return {"encoded_payload": encoded, "decode_method": decode_cmd, "metadata": {"method": method, "original_length": len(text), "encoded_length": len(encoded)}}

    def get_stats(self) -> Dict[str, Any]:
        return {"total_encodings": len(self.encoding_history), "methods_used": list(set(r["method"] for r in self.encoding_history))}