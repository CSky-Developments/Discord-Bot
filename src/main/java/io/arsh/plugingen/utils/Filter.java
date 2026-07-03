package io.arsh.plugingen.utils;

import java.util.function.Consumer;
import java.util.regex.*;

public class Filter {

    private static final Pattern BLOCK_PATTERN = Pattern.compile("```(?:\\w+)?\\s*\\n([\\s\\S]*?)```");

    public static void clean(String content, Consumer<String> action) {
        if (content == null)
            return;

        Matcher matcher = BLOCK_PATTERN.matcher(content);
        while (matcher.find()) {
            String code = matcher.group(1);
            if (code != null && !code.trim().isEmpty()) {
                action.accept(code.trim());
            }
        }
    }
}
