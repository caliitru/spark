from pydantic import BaseModel

class GenerateRequest(BaseModel):
    username: str
    platform: str
    company: str
    event: str
    title: str
    product_description: str
    
    num_images: int = 2
    num_captions: int = 4
    brand_name: str | None = None
    color: str | None = None

    want_images: bool = True
    want_captions: bool = False

    Target_audience: str | None = None
    Product: str | None = None
    Style: str | None = None
    campaign_message: str | None = None

    features: list[str] | None = None
    layout: str | None = None
    mood: str | None = None
    call_to_action: str | None = None