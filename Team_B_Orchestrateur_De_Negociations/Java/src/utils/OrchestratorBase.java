package utils;

import Communication.*;

public abstract class OrchestratorBase {
    private final IQuoteQueues _quoteQueues;
    private final IPricerQueues _pricerQueues;
    private final QueueListener<Quote> _quoteRequestListener;
    private final QueueListener<QuoteExecutionPrice> _quoteExecuteListener;
    private final QueueListener<Quote> _quoteStopListener;
    private final QueueListener<QuotePrice> _quotePriceListener;

    public OrchestratorBase(IQuoteQueues quoteQueues, IPricerQueues pricerQueues) {
        _quoteRequestListener = new QueueListener<Quote>(quoteQueues.GetQuoteRequestQueue(), o -> OnQuoteRequest(o));
        _quoteExecuteListener = new QueueListener<QuoteExecutionPrice>(quoteQueues.GetPriceExecutionQueue(), o -> OnExecutionRequest(o));
        _quoteStopListener = new QueueListener<Quote>(quoteQueues.GetQuoteStopQueue(), o -> OnQuoteStop(o));
        _quotePriceListener = new QueueListener<QuotePrice>(pricerQueues.GetPricingReplyQueue(), o -> OnQuotePriceUpdate(o));

        _quoteQueues = quoteQueues;
        _pricerQueues = pricerQueues;
    }

    protected abstract void OnQuoteRequest(Quote o);
    protected abstract void OnQuotePriceUpdate(QuotePrice o);
    protected abstract void OnExecutionRequest(QuoteExecutionPrice o);
    protected abstract void OnQuoteStop(Quote o);
    protected void NotifyQuoteReceived(Quote o){
        _quoteQueues.GetQuoteReplyQueue().add(o);
    }
    protected void NotifyPriceUpdated(QuotePrice o){
        _quoteQueues.GetPriceUpdateQueue().add(o);
    }
    protected void NotifyQuoteExecuted(QuoteExecutionPrice o){
        _quoteQueues.GetPriceExecutionReplyQueue().add(o);
    }
    protected void NotifyQuoteStopped(Quote o){
        _quoteQueues.GetQuoteStopReplyQueue().add(o);
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
