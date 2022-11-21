package QuoteSource;

import Communication.IQuoteQueues;
import Communication.QueueListener;
import Communication.QuoteQueues;
import utils.CurrencyPair;
import utils.Quote;
import utils.QuoteExecutionPrice;
import utils.QuotePrice;

import java.io.*;
import java.util.HashMap;
import java.util.concurrent.ConcurrentHashMap;

public class QuotePlatform {
    String ScenarioFilePath = "Resources/SmallScenario.txt";
    IQuoteQueues _quoteQueues;
    private HashMap<Integer, Quote> ProcessingQuotes = new HashMap<Integer, Quote>();
    private ConcurrentHashMap<Integer, Double> QuotePrices = new ConcurrentHashMap<Integer, Double>();

    public QuotePlatform(IQuoteQueues quoteQueues) {
        _quoteQueues = quoteQueues;
    }

    public void Run() {
        var priceUpdateQuoteListener = new QueueListener<QuotePrice>(_quoteQueues.GetPriceUpdateQueue(), quotePrice -> {
            // price updated
            QuotePrices.compute(quotePrice.Quote.getQuoteId(), (k, v) -> quotePrice.Price);
            System.out.println("Price update for " + quotePrice);
        });

        var stopReplyListener = new QueueListener<Quote>(_quoteQueues.GetQuoteStopReplyQueue(), quote -> {
            System.out.println("Stopped " + quote);
        });

        var executionReplyQueue = new QueueListener<QuoteExecutionPrice>(_quoteQueues.GetPriceExecutionReplyQueue(), quote -> {
            System.out.println("Execution of " + quote);
        });

        var quoteReplyQueue = new QueueListener<Quote>(_quoteQueues.GetQuoteReplyQueue(), quote -> {
            System.out.println("Started " + quote);
        });

        priceUpdateQuoteListener.Start();
        stopReplyListener.Start();
        executionReplyQueue.Start();
        quoteReplyQueue.Start();

        try(BufferedReader br = new BufferedReader(new FileReader(ScenarioFilePath))) {
            var scenarioProcessSpeed = Integer.parseInt(br.readLine());
            String line = br.readLine();

            while (line != null) {
                Process(line);
                line = br.readLine();
                Thread.sleep(scenarioProcessSpeed);
            }
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }

        priceUpdateQuoteListener.Stop();
        stopReplyListener.Stop();
        executionReplyQueue.Stop();
        quoteReplyQueue.Stop();
    }

    private void Process(String line) {
        //Examples:
        // 1000
        // CREATE 1 EUR USD
        // EXECUTE 1 0.001
        // STOP 1
        // WAIT
        // END
        var splittedLine = line.split(" ");

        switch (splittedLine[0]) {
            case "CREATE":
                var createQuoteId = Integer.parseInt(splittedLine[1]);
                var currency1 = splittedLine[2];
                var currency2 = splittedLine[3];
                var quote = new Quote(createQuoteId, new CurrencyPair(currency1, currency2));
                ProcessingQuotes.put(createQuoteId, quote);
                _quoteQueues.GetQuoteRequestQueue().add(quote);
                break;
            case "EXECUTE":
                var executeQuoteId = Integer.parseInt(splittedLine[1]);
                var executionDelta = Double.parseDouble(splittedLine[2]);
                var lastPrice = QuotePrices.getOrDefault(executeQuoteId, 0.0);

                QuoteExecutionPrice quoteExecutionPrice = new QuoteExecutionPrice();
                quoteExecutionPrice.Quote = ProcessingQuotes.get(executeQuoteId);
                quoteExecutionPrice.ExecutionPrice = lastPrice + executionDelta;

                ProcessingQuotes.remove(executeQuoteId);
                _quoteQueues.GetPriceExecutionQueue().add(quoteExecutionPrice);
                break;
            case "STOP":
                var stopQuoteId = Integer.parseInt(splittedLine[1]);
                var stopQuote = ProcessingQuotes.get(stopQuoteId);
                ProcessingQuotes.remove(stopQuoteId);
                _quoteQueues.GetQuoteStopQueue().add(stopQuote);
                break;
            case "WAIT":
                break;
            case "END":
                for (var endId:ProcessingQuotes.keySet())
                {   var endQuote = ProcessingQuotes.get(endId);
                    _quoteQueues.GetQuoteStopQueue().add(endQuote);
                }
                ProcessingQuotes.clear();
                break;
            default:
                throw new IllegalArgumentException("Can't process scenario, unknown command");
        }
    }
}
