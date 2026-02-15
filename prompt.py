from models import GenerateRequest

def build_image_prompt(req:GenerateRequest) -> str:
   
    company = req.company or "the brand"
    event = req.event or "a promotional campaign"
    title = req.title or "Marketing Campaign"
    description = req.product_description or "a modern digital product"
    audience = req.Target_audience or "modern digital users"
    color = req.color or "dynamic gradient tones"
    style = req.Style or "modern digital illustration"
    mood = req.mood or "bold, innovative, premium"

    base = f"""
Create a high-impact, visually striking social media campaign image.

Brand context:
Company: {company}
Campaign/Event: {event}
Theme: {title}

Product essence:
{description}

Target audience:
{audience}

Call to action:
{req.call_to_action or "Engage with our latest offering!"}
Art direction:
- Style: {style}
- Mood: {mood}
- Color palette inspiration: {color}
- Cinematic lighting and strong depth
- Clear focal point with dynamic composition
- Layered background elements for richness
- Avoid flat generic stock-photo look

Creative variation rules:
- Each generated image must use a different concept and layout
- Vary camera angle (close-up, wide, top-down, dramatic side)
- Vary lighting (soft glow, dramatic contrast, ambient, neon accent)
- Use abstract, symbolic, or lifestyle-based interpretations where suitable
- Explore depth, shadows, reflections, motion blur, or subtle 3D feel
Generate premium-quality, original artwork suitable for social media marketing.

Avoid if not mentioned:
- Text overlays, logos, or watermarks
- if logo is given, still don't change it, logo should be as it is, don't change it, just use it as it is in the image, don't modify it in any way
""".strip()
    platform = (req.platform or "").lower()
    match platform.lower():
        case "linkedin":
            return (
                base + " Professional corporate design, clean minimal layout, ample whitespace, "
                "subtle gradients, premium look, safe margins (keep key elements within center 70%)."
            )
        case "instagram":
            return (
                base + " Modern vibrant aesthetic, bold composition, lifestyle-friendly look, "
                "rich visuals, high contrast, trendy but clean, safe margins."
            )
        case "twitter" | "x":
            return (
                base + " Bold, simple, high-contrast design, minimal elements, clear focal point, "
                "optimized for fast scrolling, safe margins."
            )
        case _:
            return base + " Clean modern design, safe margins, high quality."


def build_caption_prompt(platform: str, company: str, event: str, title: str, details: str, n: int, target_audience: str | None = None, product: str | None = None, call_to_action: str | None = None) -> str:
    context = f"{company} — {event}. Title: {title}. Details: {details}."

    if target_audience:
        context += f" Target audience: {target_audience}"
    if product:
        context += f" Product: {product}"
    if call_to_action:
        context += f" Call to action: {call_to_action}"

    match platform.lower():
        case "linkedin":
            return (
                f"Write {n} professional LinkedIn captions for: {context}\n"
                "- 3–5 lines each\n- confident, business-friendly\n- include 3–8 relevant hashtags\n"
                "- avoid excessive emojis\nReturn each caption separated by a blank line."
            )
        case "instagram":
            return (
                f"Write {n} Instagram captions for: {context}\n"
                "- friendly and catchy\n- 1–3 short paragraphs\n- can use a few emojis\n"
                "- include 8–15 hashtags\nReturn each caption separated by a blank line."
            )
        case "twitter" | "x":
            return (
                f"Write {n} X (Twitter) posts for: {context}\n"
                "- max ~200 characters each\n- punchy\n- 1–3 hashtags\n"
                "Return each post separated by a blank line."
            )
        case _:
            return (
                f"Write {n} captions for: {context}\n"
                "- include hashtags\nReturn each caption separated by a blank line."
            )
