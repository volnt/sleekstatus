from app.utils import send_email

def test_send_email():
    assert send_email.delay(
        "trash@volent.fr", "Test subject",
        "Test body", ["trash@volent.fr"]
    )
