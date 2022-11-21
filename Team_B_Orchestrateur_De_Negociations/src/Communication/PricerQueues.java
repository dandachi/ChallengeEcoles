package Communication;

import utils.Quote;
import utils.QuotePrice;

import java.util.concurrent.LinkedBlockingQueue;

public class PricerQueues implements IPricerQueues {
    LinkedBlockingQueue<Quote> _requestQueue = new LinkedBlockingQueue<Quote>();
    LinkedBlockingQueue<QuotePrice> _replyQueue = new LinkedBlockingQueue<QuotePrice>();
    @Override
    public LinkedBlockingQueue<Quote> GetPricingRequestQueue() {
        return _requestQueue;
    }

    @Override
    public LinkedBlockingQueue<QuotePrice> GetPricingReplyQueue() {
        return _replyQueue;
    }
}
