package io.arsh.license.models;

public enum License {

    LoreSMP(new LicenseData(
            "iXkMYovoMcRZTUIO3YrDcmfjyzsNfFP7",
            "OWCYiekqWNX4zLGh",
            "a2mezIEWVRhdpXh5")
    ),

    DeckCardSMP(new LicenseData(
            "A7Ov7w4C3saacYv1ADO9J8qwqU8uvhvw",
            "qtA5ZHahGWTyiFkp",
            "gM0qnSBSg7KptIer")
    ),

    RisingSMP(new LicenseData(
            "1hGqAJwOzMGcjdkGtGHw3eQqNE5IP1D9",
            "s3Fp2q7q380SuWf7",
            "JIQnvOBKaVOw947m")
    ),
    ScoreSMP(new LicenseData(
            "rmOewRf8CxzwofRFzhMjo0pLung1Gxhf",
            "avwu5ussgnRmIgo8",
            "bl1ejPqZ3xsB9T3S")
    ),
    DarkSideSMP(new LicenseData(
            "8gduA7UFnoWf941EihFEMLUuNaSld6VI",
            "hnvOb8Jqm8ZY14dT",
            "GEamIHJrrOZyFo0N")
    );

    private final LicenseData licenseData;

    License(LicenseData licenseData) {
        this.licenseData = licenseData;
    }

    public LicenseData getLicenseData() {
        return licenseData;
    }
}
