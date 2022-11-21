package Communication;

import utils.Quote;
import utils.QuoteExecutionPrice;
import utils.QuotePrice;

import java.util.concurrent.LinkedBlockingQueue;

public interface IQuoteQueues {
    // Input queue to workflow
    LinkedBlockingQueue<Quote> GetQuoteRequestQueue();

    LinkedBlockingQueue<Quote> GetQuoteStopQueue();
    LinkedBlockingQueue<QuoteExecutionPrice>  GetPriceExecutionQueue();

    // Output queue to workflow
    LinkedBlockingQueue<Quote> GetQuoteReplyQueue();
    LinkedBlockingQueue<QuotePrice>  GetPriceUpdateQueue();
    LinkedBlockingQueue<Quote> GetQuoteStopReplyQueue();
    LinkedBlockingQueue<QuoteExecutionPrice>  GetPriceExecutionReplyQueue();
}
