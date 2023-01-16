import Communication.IPricerQueues;
import Communication.IQuoteQueues;
import utils.*;

import java.util.concurrent.*;

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
        NotifyQuoteReceived(o);
    }

    @Override
    protected void OnQuotePriceUpdate(QuotePrice o) {
        // add code
        NotifyPriceUpdated(o);
    }

    @Override
    protected void OnExecutionRequest(QuoteExecutionPrice o) {
        // add code
        var anyValidPrice = false;
        if (anyValidPrice)
        {
            o.Status = ExecutionStatus.Success;
            NotifyQuoteExecuted(o);
        }
        else
        {
            o.Status = ExecutionStatus.Fail;
            NotifyQuoteExecuted(o);
        }
    }

    @Override
    protected void OnQuoteStop(Quote o) {
        // add code
        NotifyQuoteStopped(o);
    }

    @Override
    public void Start() {
        super.Start();
        // add code

    }

    @Override
    public void Stop() {
        super.Stop();
        // add code

    }
}
