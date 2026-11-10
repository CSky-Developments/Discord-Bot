from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class LicenseData:
    salt: str
    aes_key: str
    aes_iv: str

class LicenseType(Enum):
    LoreSMP = LicenseData(
        salt="iXkMYovoMcRZTUIO3YrDcmfjyzsNfFP7",
        aes_key="OWCYiekqWNX4zLGh",
        aes_iv="a2mezIEWVRhdpXh5"
    )
    DeckCardSMP = LicenseData(
        salt="A7Ov7w4C3saacYv1ADO9J8qwqU8uvhvw",
        aes_key="qtA5ZHahGWTyiFkp",
        aes_iv="gM0qnSBSg7KptIer"
    )
    RisingSMP = LicenseData(
        salt="1hGqAJwOzMGcjdkGtGHw3eQqNE5IP1D9",
        aes_key="s3Fp2q7q380SuWf7",
        aes_iv="JIQnvOBKaVOw947m"
    )
    ScoreSMP = LicenseData(
        salt="rmOewRf8CxzwofRFzhMjo0pLung1Gxhf",
        aes_key="avwu5ussgnRmIgo8",
        aes_iv="bl1ejPqZ3xsB9T3S"
    )
    DarkSideSMP = LicenseData(
        salt="8gduA7UFnoWf941EihFEMLUuNaSld6VI",
        aes_key="hnvOb8Jqm8ZY14dT",
        aes_iv="GEamIHJrrOZyFo0N"
    )

    @property
    def license_data(self) -> LicenseData:
        return self.value
