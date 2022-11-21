package Communication;

import utils.Quote;
import utils.QuoteExecutionPrice;
import utils.QuotePrice;

import java.util.concurrent.LinkedBlockingQueue;

public class QuoteQueues implements IQuoteQueues {

    LinkedBlockingQueue<Quote> _requestQueue = new LinkedBlockingQueue<Quote>();
    LinkedBlockingQueue<Quote> _replyQueue = new LinkedBlockingQueue<Quote>();
    LinkedBlockingQueue<QuotePrice> _priceUpdateQueue = new LinkedBlockingQueue<QuotePrice>();
    LinkedBlockingQueue<Quote> _stopQueue = new LinkedBlockingQueue<Quote>();
    LinkedBlockingQueue<Quote> _stopReplyQueue = new LinkedBlockingQueue<Quote>();
    LinkedBlockingQueue<QuoteExecutionPrice> _priceExecutionQueue = new LinkedBlockingQueue<QuoteExecutionPrice>();
    LinkedBlockingQueue<QuoteExecutionPrice> _priceExecutionReplyQueue = new LinkedBlockingQueue<QuoteExecutionPrice>();


    @Override
    public LinkedBlockingQueue<Quote> GetQuoteRequestQueue() {
        return _requestQueue;
    }

    @Override
    public LinkedBlockingQueue<Quote> GetQuoteStopQueue() {
        return _stopQueue;
    }

    @Override
    public LinkedBlockingQueue<Quote> GetQuoteStopReplyQueue() {
        return _stopReplyQueue;
    }
    @Override
    public LinkedBlockingQueue<QuotePrice> GetPriceUpdateQueue() {
        return _priceUpdateQueue;
    }

    @Override
    public LinkedBlockingQueue<QuoteExecutionPrice> GetPriceExecutionQueue() {
        return _priceExecutionQueue;
    }

    @Override
    public LinkedBlockingQueue<Quote> GetQuoteReplyQueue() {
        return _replyQueue;
    }

    @Override
    public LinkedBlockingQueue<QuoteExecutionPrice> GetPriceExecutionReplyQueue() {
        return _priceExecutionReplyQueue;
    }
}
