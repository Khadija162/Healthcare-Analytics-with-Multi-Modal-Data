from io import BytesIO
from PIL import Image
from fastapi.testclient import TestClient
from backend.main import app
from healthcare.vlm import inspect_image

def test_health():
    assert TestClient(app).get("/health").status_code==200

def test_validation():
    assert TestClient(app).post("/api/heart/score",json={"age":51}).status_code==422

def test_image_inspection():
    image=Image.new("RGB",(32,32),color="white")
    buf=BytesIO();image.save(buf,format="PNG")
    result=inspect_image(buf.getvalue())
    assert result["width"]==32
    assert result["mean_intensity"]==255.0

def test_reject_invalid_image():
    r=TestClient(app).post("/api/images/inspect",files={"file":("a.png",b"not an image","image/png")})
    assert r.status_code==422
