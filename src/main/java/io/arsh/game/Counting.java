package io.arsh.game;

import com.fasterxml.jackson.databind.ObjectMapper;
import io.arsh.utils.Config;
import io.arsh.utils.Logger;
import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.entities.User;
import net.dv8tion.jda.api.entities.emoji.Emoji;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class Counting extends ListenerAdapter {

    private static final List<Integer> countingGoals = Arrays.asList(10, 50, 100, 200, 300, 400, 500, 1000, 1500, 2000, 2500, 5000, 7500, 10000);

    private static final File COUNTING_DATA_FILE = new File("./data/counting_data.json");
    private static final ObjectMapper mapper = new ObjectMapper();
    private int currentCount;
    private String lastCounterID;

    public Counting() {
        Logger.info("Loading counting minigames...", false);
        loadCountingData();
        Logger.info("Successfully loaded counting minigames!", false);
    }

    private void loadCountingData() {
        if (!COUNTING_DATA_FILE.exists()) {
            currentCount = 1;
            lastCounterID = null;
            saveCountingData();
            return;
        }
        try {
            CountingData data = mapper.readValue(COUNTING_DATA_FILE, CountingData.class);
            currentCount = data.currentCount;
            lastCounterID = data.lastCounterID;
        } catch (IOException ex) {
            Logger.error("An error occurred while loading counting data. Error: " + ex.getMessage(), false);
            currentCount = 1;
            lastCounterID = null;
        }
    }

    private void saveCountingData() {
        CountingData data = new CountingData(currentCount, lastCounterID);
        try {
            mapper.writerWithDefaultPrettyPrinter().writeValue(COUNTING_DATA_FILE, data);
        } catch (IOException ex) {
            Logger.info("An error occurred while saving counting data. Error: " + ex.getMessage(), false);
        }
    }

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        if (!event.getChannel().getId().equals(Config.COUNTING_CHANNEL_ID)) {
            return;
        }
        Message message = event.getMessage();
        User user = message.getAuthor();

        if (user.isBot()) {
            return;
        }

        String content = message.getContentRaw().trim();
        int number;
        try {
            number = Integer.parseInt(content);
        } catch (NumberFormatException e) {
            return;
        }

        if (number <= 0 || number != currentCount) {
            message.reply("**Sike!** That's the wrong number. Number should be " + currentCount + ".").queue();
            Logger.info("Oops! Looks like `" + user.getName() + "` made a slip in the counting. The count was at `" + currentCount + "` in `" + message.getChannel().getName() + "`.", true);
            message.addReaction(Emoji.fromCustom("XMark", 1120422570773184685L, false)).queue();
            resetCount();
            return;
        }

        if (user.getId().equals(lastCounterID)) {
            message.reply("**Uh-oh!** " + user.getAsMention() + ", you can't count twice in a row. The count has been reset.").queue();
            Logger.info("`" + user.getName() + "` counted twice in a row. The current count was at `" + currentCount + "` in `" + message.getChannel().getName() + "`.", true);
            message.addReaction(Emoji.fromCustom("XMark", 1120422570773184685L, false)).queue();
            resetCount();
            return;
        }

        if (countingGoals.contains(currentCount)) {
            String goalMessage = getGoalMessage(currentCount, user);
            for (String reaction : getGoalReactions(currentCount)) {
                message.addReaction(Emoji.fromUnicode(reaction)).queue();
            }
            Logger.info("`" + user.getName() + "` helped us reach the goal of `" + currentCount + "` in `" + message.getChannel().getName() + "`.", true);
            message.reply(goalMessage).queue();
        } else {
            message.addReaction(Emoji.fromCustom("OMark", 1120422566725701692L, false)).queue();
        }

        currentCount++;
        lastCounterID = user.getId();
        saveCountingData();
    }

    private void resetCount() {
        currentCount = 1;
        lastCounterID = null;
        saveCountingData();
    }

    private String getGoalMessage(int number, User user) {
        String mention = user.getAsMention();
        return switch (number) {
            case 10 -> "🎉 **Hooray!** " + mention + " helped us reach the goal of " + number + "! Keep up the good work!";
            case 50 -> "🎊 **Amazing!** " + mention + " contributed to the goal of " + number + "! Let's keep counting!";
            case 100 -> "🎈 **Congratulations,** " + mention + "! We've hit the big " + number + "! Keep the count going!";
            case 200 -> "🥳 **Woohoo!** " + mention + " has helped us achieve the milestone of " + number + "! Great work!";
            case 300 -> "🌟 **Incredible!** " + mention + " pushed us to the goal of " + number + "! Let's keep counting higher!";
            case 400 -> "🔥 **Astonishing progress,** " + mention + "! We've reached " + number + "! Keep up the great work!";
            case 500 -> "🚀 **Spectacular!** " + mention + " has helped us reach the grand " + number + " milestone! Keep counting!";
            case 1000 -> "💀 **Unbelievable!** " + mention + " propelled us to the epic goal of " + number + "! Thank you!";
            case 10000 -> "❓ **How did we get here?** " + mention + "? Don’t tell me you’re hacking... Nah... Man, a score of **" + number + "** is hard to believe.";
            default -> "💀 **Goal reached!** " + mention + " helped us reach " + number + "! Keep it up!";
        };
    }

    private List<String> getGoalReactions(int number) {
        return switch (number) {
            case 10 -> Collections.singletonList("🎉");
            case 50 -> Collections.singletonList("🎊");
            case 100 -> Collections.singletonList("🎈");
            case 200 -> Collections.singletonList("🥳");
            case 300 -> Collections.singletonList("🌟");
            case 400 -> Collections.singletonList("🔥");
            case 500 -> Collections.singletonList("🚀");
            case 10000 -> Collections.singletonList("❓");
            default -> Collections.singletonList("💀");
        };
    }


    private static class CountingData {
        public int currentCount;
        public String lastCounterID;
        public CountingData() {}
        public CountingData(int currentCount, String lastCounterID) {
            this.currentCount = currentCount;
            this.lastCounterID = lastCounterID;
        }
    }

}