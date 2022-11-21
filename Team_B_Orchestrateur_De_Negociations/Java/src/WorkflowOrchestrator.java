import Communication.*;
import utils.*;

public class WorkflowOrchestrator {
    private final IQuoteQueues _quoteQueues;
    private final IPricerQueues _pricerQueues;
    private final QueueListener<Quote> _quoteRequestListener;
    private final QueueListener<QuoteExecutionPrice> _quoteExecuteListener;
    private final QueueListener<Quote> _quoteStopListener;
    private final QueueListener<QuotePrice> _quotePriceListener;

    private final Double ExecutionTolerance = 0.000001;

    public WorkflowOrchestrator(IQuoteQueues quoteQueues, IPricerQueues pricerQueues) {
        _quoteRequestListener = new QueueListener<Quote>(quoteQueues.GetQuoteRequestQueue(), o -> OnQuoteRequest(o));
        _quoteExecuteListener = new QueueListener<QuoteExecutionPrice>(quoteQueues.GetPriceExecutionQueue(), o -> OnExecutionRequest(o));
        _quoteStopListener = new QueueListener<Quote>(quoteQueues.GetQuoteStopQueue(), o -> OnQuoteStop(o));
        _quotePriceListener = new QueueListener<QuotePrice>(pricerQueues.GetPricingReplyQueue(), o -> OnQuotePriceUpdate(o));

        _quoteQueues = quoteQueues;
        _pricerQueues = pricerQueues;

    }

    private void OnQuoteRequest(Quote o) {

    }
    private void OnQuotePriceUpdate(QuotePrice o) {
    }

    private void OnExecutionRequest(QuoteExecutionPrice o) {

    }
    private void OnQuoteStop(Quote o) {
    }

    public void Start() {
        _quoteRequestListener.Start();
        _quoteExecuteListener.Start();
        _quoteStopListener.Start();
        _quotePriceListener.Start();
    }

    public void Stop() {
        _quoteRequestListener.Stop();
        _quoteExecuteListener.Stop();
        _quoteStopListener.Stop();
        _quotePriceListener.Stop();
    }
}
