"""Build a concise Week 4 capstone slide deck as a PDF."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


BASE_DIR = Path(__file__).resolve().parent
OUTPUT = BASE_DIR / "presentation.pdf"
NAVY = RGBColor(24, 49, 83)
BLUE = RGBColor(38, 88, 216)
LIGHT = RGBColor(239, 246, 255)
INK = RGBColor(39, 51, 72)
MUTED = RGBColor(95, 111, 137)
WHITE = RGBColor(255, 255, 255)


def add_text(slide, x, y, w, h, text, size=20, color=INK, bold=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.word_wrap = True
    frame.margin_left = Inches(0.03)
    frame.margin_right = Inches(0.03)
    frame.margin_top = Inches(0.02)
    frame.margin_bottom = Inches(0.02)
    for index, line in enumerate(text.split("\n")):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = line
        paragraph.font.name = "Aptos"
        paragraph.font.size = Pt(size)
        paragraph.font.bold = bold
        paragraph.font.color.rgb = color
        paragraph.space_after = Pt(10)
    return box


def add_bullets(slide, bullets, x=0.9, y=1.65, w=11.5, h=4.9, size=21):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.word_wrap = True
    frame.margin_left = Inches(0.05)
    for index, item in enumerate(bullets):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = f"•  {item}"
        paragraph.font.name = "Aptos"
        paragraph.font.size = Pt(size)
        paragraph.font.color.rgb = INK
        paragraph.space_after = Pt(17)


def base_slide(pres, title, section="WEEK 4 CAPSTONE"):
    slide = pres.slides.add_slide(pres.slide_layouts[6])
    background = slide.background.fill
    background.solid()
    background.fore_color.rgb = WHITE
    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, pres.slide_width, Inches(0.16))
    band.fill.solid()
    band.fill.fore_color.rgb = BLUE
    band.line.fill.background()
    add_text(slide, 0.7, 0.42, 5.8, 0.28, section, 10, BLUE, True)
    add_text(slide, 0.7, 0.78, 12.0, 0.64, title, 29, NAVY, True)
    footer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(7.08), Inches(11.95), Inches(0.015))
    footer.fill.solid()
    footer.fill.fore_color.rgb = RGBColor(220, 228, 240)
    footer.line.fill.background()
    add_text(slide, 0.72, 7.15, 8.5, 0.2, "AI Pioneers Internship · Titanic survival prediction", 9, MUTED)
    add_text(slide, 12.05, 7.14, 0.5, 0.2, str(len(pres.slides)), 9, MUTED)
    return slide


def add_card(slide, x, y, w, h, heading, body, accent=BLUE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = LIGHT
    shape.line.color.rgb = RGBColor(216, 228, 247)
    shape.text_frame.clear()
    shape.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    shape.text_frame.margin_left = Inches(0.2)
    shape.text_frame.margin_right = Inches(0.2)
    shape.text_frame.margin_top = Inches(0.1)
    p = shape.text_frame.paragraphs[0]
    p.text = heading
    p.font.name = "Aptos Display"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = accent
    p.space_after = Pt(9)
    q = shape.text_frame.add_paragraph()
    q.text = body
    q.font.name = "Aptos"
    q.font.size = Pt(14)
    q.font.color.rgb = INK
    q.space_after = Pt(0)
    return shape


def main():
    pres = Presentation()
    pres.slide_width = Inches(13.333)
    pres.slide_height = Inches(7.5)

    slide = pres.slides.add_slide(pres.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = NAVY
    add_text(slide, 0.9, 1.0, 4, 0.4, "AI PIONEERS INTERNSHIP · WEEK 4", 12, RGBColor(162, 191, 255), True)
    add_text(slide, 0.9, 1.85, 10.7, 1.45, "Titanic Survival\nPrediction API", 38, WHITE, True)
    add_text(slide, 0.95, 4.0, 10.8, 0.9, "An end-to-end machine-learning capstone: prepare data, train and test a model, serialize it, and serve predictions with FastAPI.", 21, RGBColor(220, 231, 250))
    add_text(slide, 0.95, 6.5, 10.5, 0.35, "Project repository: github.com/shreyas23dev/Week-4", 13, RGBColor(190, 208, 240))

    slide = base_slide(pres, "Problem and objective")
    add_bullets(slide, [
        "Demonstrate a complete supervised-learning workflow using passenger attributes.",
        "Predict the historical target label: survived (yes/no).",
        "Package preprocessing and the Random Forest classifier into one reusable model pipeline.",
        "Expose a validated JSON prediction API and a simple browser form.",
    ])

    slide = base_slide(pres, "Dataset and responsible use")
    add_card(slide, 0.85, 1.72, 3.7, 1.8, "891 passengers", "Historical Titanic records used for an educational example.")
    add_card(slide, 4.85, 1.72, 3.7, 1.8, "7 inputs", "Age, class, sex, family counts, fare, and embarkation port.")
    add_card(slide, 8.85, 1.72, 3.7, 1.8, "Binary output", "Estimated class and probability for the survival target.")
    add_bullets(slide, [
        "A stratified 80/20 split keeps survival proportions similar between train and test sets.",
        "Target duplicates and post-outcome columns are not used as model inputs.",
        "The output is not causal evidence and must not be used for real-world consequential decisions.",
    ], y=4.1, h=2.3, size=17)

    slide = base_slide(pres, "End-to-end architecture")
    blocks = [
        (0.75, "CSV data", "Titanic records"),
        (3.25, "Train / test", "Stratified split"),
        (5.75, "Pipeline", "Impute · encode · scale · train"),
        (8.25, "Joblib", "Serialized pipeline"),
        (10.75, "FastAPI", "Web form + JSON API"),
    ]
    for x, heading, body in blocks:
        add_card(slide, x, 2.55, 1.9, 1.55, heading, body)
    add_text(slide, 2.65, 3.1, 0.45, 0.45, "→", 27, BLUE, True)
    add_text(slide, 5.15, 3.1, 0.45, 0.45, "→", 27, BLUE, True)
    add_text(slide, 7.65, 3.1, 0.45, 0.45, "→", 27, BLUE, True)
    add_text(slide, 10.15, 3.1, 0.45, 0.45, "→", 27, BLUE, True)
    add_text(slide, 1.0, 5.05, 11.3, 0.8, "The preprocessing transformations and classifier travel together in a single saved pipeline, so API requests use the same feature preparation as training.", 18, INK)

    slide = base_slide(pres, "Training, testing, and metrics")
    add_card(slide, 0.9, 1.8, 5.4, 1.8, "Training", "Random Forest · fixed random seed\nMedian/mode imputation · one-hot encoding\nNumeric standardization fitted on training data", BLUE)
    add_card(slide, 7.0, 1.8, 5.4, 1.8, "Held-out test evaluation", "Accuracy · precision · recall\nF1 score · ROC AUC · confusion matrix", BLUE)
    add_bullets(slide, [
        "Metrics describe performance on one test split, not a performance guarantee.",
        "The artifact includes evaluation metadata and feature names for reproducibility.",
        "Tests cover API validation, responses, service readiness, and the browser form.",
    ], y=4.25, h=2.2, size=17)

    slide = base_slide(pres, "Prediction API and demo")
    add_card(slide, 0.9, 1.75, 5.4, 1.55, "Browser", "Open the local homepage, enter passenger features, and view the predicted label and probability.")
    add_card(slide, 7.0, 1.75, 5.4, 1.55, "REST endpoints", "GET /health · readiness\nPOST /predict · validated JSON\n/docs · interactive API schema")
    add_text(slide, 1.05, 4.0, 10.8, 0.45, "Start locally with: uvicorn app:app --host 127.0.0.1 --port 8000", 18, NAVY, True)
    add_text(slide, 1.05, 4.65, 10.9, 0.85, "Before using the API, run train_model.py to create the saved Joblib pipeline. Input validation rejects unsupported categories and invalid numeric ranges.", 17, INK)

    slide = base_slide(pres, "Results, deployment, and next steps")
    add_bullets(slide, [
        "The complete workflow is runnable locally; the ASGI API and prediction form are ready for a hosting platform.",
        "A public deployment needs a selected host, account, and deployment configuration; none is assumed here.",
        "Next steps: add a container, CI checks, model-version metadata, monitoring, and additional fairness review.",
        "Historical training labels make this a learning demonstration only, not a tool for judging real people.",
    ], y=1.8, h=4.5, size=20)

    pres.save(OUTPUT)
    print(f"Saved presentation: {OUTPUT}")


if __name__ == "__main__":
    main()
