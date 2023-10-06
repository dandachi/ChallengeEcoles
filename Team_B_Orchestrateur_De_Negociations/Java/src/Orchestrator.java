import Communication.IPricerQueues;
import Communication.IQuoteQueues;
import utils.*;

import java.util.concurrent.*;

public class Orchestrator extends OrchestratorBase {
    protected final Double ExecutionTolerance = 0.000001;
    // add code

    public Orchestrator(IQuoteQueues quoteQueues, IPricerQueues pricerQueues) {
        super(quoteQueues, pricerQueues);
        // TODO Initialize data structure to hold quotes, and to hold quote prices
    }

    @Override
    protected void OnQuoteRequest(Quote o) {
        // TODO Add quotes to the data structure
        NotifyQuoteReceived(o);
    }

    @Override
    protected void OnQuotePriceUpdate(QuotePrice o) {
        // TODO Update quote prices in quote prices data structure
        NotifyPriceUpdated(o);
    }

    @Override
    protected void OnExecutionRequest(QuoteExecutionPrice o) {
        
        var anyValidPrice = false;
        // TODO check if there is a quote price  from the last 3 quote prices
        //  that is equal to execution price within EXECUTION Tolerance

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

        // TODO clean unwanted quotes and quote prices
    }

    @Override
    protected void OnQuoteStop(Quote o) {

        // TODO clean unwanted quotes and quote prices
        NotifyQuoteStopped(o);
    }

    @Override
    public void Start() {
        super.Start();
        
        _scheduler = Executors.newScheduledThreadPool(1);
        _scheduler.scheduleAtFixedRate(new Runnable() {
            @Override
            public void run() {
                // TODO Schedule a pricing task
                // We should ask for a pricing for each quote that we have in memory
                // Communication with pricer can be done using the method RequestNewPrice
            }
        }, 1, 2, TimeUnit.SECONDS);

    }

    @Override
    public void Stop() {
        super.Stop();
        _scheduler.shutdown();
    }
}
