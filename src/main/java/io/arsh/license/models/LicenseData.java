package io.arsh.license.models;

public class LicenseData {
    private final String SALT;
    private final String AES_KEY;
    private final String AES_IV;

    public LicenseData(String SALT, String AES_KEY, String AES_IV) {
        this.SALT = SALT;
        this.AES_KEY = AES_KEY;
        this.AES_IV = AES_IV;
    }

    public String getSALT() {
        return SALT;
    }

    public String getAES_KEY() {
        return AES_KEY;
    }

    public String getAES_IV() {
        return AES_IV;
    }

}

