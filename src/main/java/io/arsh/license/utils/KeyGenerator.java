package io.arsh.license.utils;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Base64;

public class KeyGenerator {

    public static String generateKey(String SALT, String ip, int port, String uuid) throws Exception {
        String input = ip + ":" + port + ":" + uuid + ":" + SALT;
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(hash);
    }

}
