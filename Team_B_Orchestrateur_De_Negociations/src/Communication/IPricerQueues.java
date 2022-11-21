package Communication;

import utils.Quote;
import utils.QuotePrice;

import java.util.concurrent.LinkedBlockingQueue;

public interface IPricerQueues {
    // Output queue to workflow
    LinkedBlockingQueue<Quote> GetPricingRequestQueue();

    // Input queue to workflow
    LinkedBlockingQueue<QuotePrice>  GetPricingReplyQueue();
}
