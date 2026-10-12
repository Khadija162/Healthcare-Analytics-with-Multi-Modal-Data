"""Image processing/VLM research demonstrator. NOT a radiology classifier or diagnosis."""
import os
from io import BytesIO
from PIL import Image,ImageStat
MAX_IMAGE_BYTES=5_000_000

def inspect_image(content:bytes)->dict:
    if len(content)>MAX_IMAGE_BYTES: raise ValueError("Image too large (max 5 MB)")
    try:
        image=Image.open(BytesIO(content))
        image.verify()
        image=Image.open(BytesIO(content)).convert("RGB")
    except Exception as exc:
        raise ValueError("Invalid image") from exc
    if image.width*image.height>16_000_000: raise ValueError("Image dimensions too large")
    gray=image.convert("L")
    result={"width":image.width,"height":image.height,
       "mean_intensity":round(float(ImageStat.Stat(gray).mean[0]),2),
       "mode":os.getenv("VLM_MODE","metadata"),
       "disclaimer":"Research image observation only; not diagnostic"}
    if result["mode"]=="blip":
        try:
            from transformers import pipeline
            captioner=pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")
            result["caption"]=captioner(image,max_new_tokens=40)[0]["generated_text"]
            result["model_note"]="General-domain caption, not a clinical finding"
        except ImportError as exc:
            raise RuntimeError("Install torch and transformers for VLM_MODE=blip") from exc
    elif result["mode"]!="metadata": raise ValueError("Unsupported VLM_MODE")
    return result
