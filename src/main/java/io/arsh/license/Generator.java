package io.arsh.license;

import io.arsh.license.models.License;
import io.arsh.license.utils.AESEncrypter;
import io.arsh.license.utils.KeyGenerator;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.regex.Pattern;

public class Generator {

    private static final Pattern IP_PATTERN = Pattern.compile(
            "^((25[0-5]|2[0-4]\\d|1?\\d?\\d)(\\.|$)){4}$"
    );

    private static final Pattern UUID_PATTERN = Pattern.compile(
            "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
    );

    private static File getLicenseFile(License license, String ip, int port, String uuid) {
        try {
            String plainLicense = KeyGenerator.generateKey(
                    license.getLicenseData().getSALT(), ip, port, uuid
            );
            String encrypted = AESEncrypter.encrypt(
                    license.getLicenseData().getAES_KEY(),
                    license.getLicenseData().getAES_IV(),
                    plainLicense
            );
            return writeLicenseFile(encrypted);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        return null;
    }

    private static File writeLicenseFile(String encrypted) throws IOException {
        File file = new File("license.key");
        try (FileWriter writer = new FileWriter(file)) {
            writer.write("-----BEGIN LICENSE KEY-----\n");
            writer.write(encrypted + "\n");
            writer.write("-----END LICENSE KEY-----\n\n");

            writer.write("© 2025 CSky Developments\n\n");
            writer.write("All rights reserved.\n\n");
            writer.write("This Plugin License Agreement (\"Agreement\") is made between CSky Developments\n");
            writer.write("and the Licensee who purchases and uses the software. Unauthorized use,\n");
            writer.write("reproduction, or distribution is strictly prohibited and may result in legal action.\n\n");
            writer.write("CSky Developments retains full rights and intellectual property ownership.\n");
        }
        return file;
    }

}
