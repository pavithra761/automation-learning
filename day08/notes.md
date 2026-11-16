You give the AI the messy letter and the form, and say: “Fill in the boxes. If you can’t find something, leave the box empty.”

The form is called a schema.
Writing the form in Python is done with a tool called Pydantic. The Python class is the form.
If the AI tries to write words in the “total” box, Pydantic says “No, that box only takes numbers.”

PYDANTIC


steps:
crate a mkdir day08
along with notes an other files
now activate the python for day08
install llibrariers of antropic dotenv and pydantic(class to keep the answers in feild)

Structured output gives a clean object, with total as a number and not text.”
"vendor": "Brightwave Supplies Ltd.",
  "invoice_number": "INV-2041",
  "date": "12 March 2026",
  "total": 576.0,
  "currency": "EUR"


  you can also add feild validator by importing from pydantic
  from pydantic import BaseModel, ValidationError, field_validator


class Invoice(BaseModel):
    vendor: Optional[str] = None
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    currency: Optional[str] = None

    @field_validator("total")
    @classmethod
    def total_not_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("total must not be negative")
        return v

    @field_validator("currency")
    @classmethod
    def currency_is_code(cls, v):
        if v is not None and not (len(v) == 3 and v.isalpha() and v.isupper()):
            raise ValueError("currency must be a 3-letter code like EUR")
        return v