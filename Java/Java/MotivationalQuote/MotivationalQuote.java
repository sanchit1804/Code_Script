import java.io.*;
import java.net.*;
import java.util.*;

public class MotivationalQuote {

    private static final String QUOTE_FILE = "quotes.txt";

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Choose an option:");
        System.out.println("1. Show random local quote");
        System.out.println("2. Fetch quote from API");
        System.out.print("Enter choice: ");

        int choice = scanner.nextInt();
        scanner.close();

        switch (choice) {
            case 1:
                showRandomLocalQuote();
                break;
            case 2:
                fetchQuoteFromAPI();
                break;
            default:
                System.out.println("Invalid choice!");
        }
    }

    // Option 1: Read from local file
    private static void showRandomLocalQuote() {
        List<String> quotes = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(QUOTE_FILE))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (!line.trim().isEmpty()) {
                    quotes.add(line.trim());
                }
            }

            if (quotes.isEmpty()) {
                System.out.println("No quotes found in file!");
                return;
            }

            Random random = new Random();
            int index = random.nextInt(quotes.size());
            System.out.println("\n💬 Random Quote:\n" + quotes.get(index));

        } catch (IOException e) {
            System.out.println("Error reading quotes file: " + e.getMessage());
        }
    }

    // Option 2: Fetch from public API
    private static void fetchQuoteFromAPI() {
        try {
            URL url = new URL("https://api.quotable.io/random");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");

            if (conn.getResponseCode() == 200) {
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(conn.getInputStream()));
                StringBuilder response = new StringBuilder();
                String line;

                while ((line = in.readLine()) != null) {
                    response.append(line);
                }
                in.close();

                // Simple extraction of the "content" field
                String json = response.toString();
                String quote = json.split("\"content\":\"")[1].split("\",")[0];
                System.out.println("\n🌐 Fetched Quote:\n" + quote);
            } else {
                System.out.println("Failed to fetch quote from API.");
            }

        } catch (Exception e) {
            System.out.println("Error fetching quote: " + e.getMessage());
        }
    }
}
