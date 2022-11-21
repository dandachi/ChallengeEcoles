import Communication.PricerQueues;
import Communication.QuoteQueues;
import Pricer.SpotPricer;
import QuoteSource.QuotePlatform;

public class Main {
    public static void main(String[] args) {

        System.out.println("Starting Application");
        var pricerQueues = new PricerQueues();
        var quoteQueues = new QuoteQueues();

        var quotePlatform = new QuotePlatform(quoteQueues);
        var spotPricer = new SpotPricer(pricerQueues);

        var workflowOrchestrator = new WorkflowOrchestrator(quoteQueues, pricerQueues);

        spotPricer.Start();
        workflowOrchestrator.Start();
        quotePlatform.Run();
        spotPricer.Stop();
        workflowOrchestrator.Stop();
    }
}