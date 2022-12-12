import Communication.IPricerQueues;
import Communication.IQuoteQueues;
import utils.OrchestratorBase;
import utils.Quote;
import utils.QuoteExecutionPrice;
import utils.QuotePrice;

public class Orchestrator extends OrchestratorBase {
    protected final Double ExecutionTolerance = 0.000001;
    // add code

    public Orchestrator(IQuoteQueues quoteQueues, IPricerQueues pricerQueues) {
        super(quoteQueues, pricerQueues);

        // add code to constructor
    }

    @Override
    protected void OnQuoteRequest(Quote o) {
        // add code
    }

    @Override
    protected void OnQuotePriceUpdate(QuotePrice o) {
        // add code
    }

    @Override
    protected void OnExecutionRequest(QuoteExecutionPrice o) {
        // add code
    }

    @Override
    protected void OnQuoteStop(Quote o) {
        // add code
    }
}
