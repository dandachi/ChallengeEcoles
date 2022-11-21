package Pricer;

import Communication.IPricerQueues;
import Communication.QueueListener;
import utils.CurrencyPair;
import utils.Quote;
import utils.QuotePrice;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Random;

public class SpotPricer {
    private IPricerQueues _pricerQueue;
    private QueueListener _queueListener;

    public SpotPricer(IPricerQueues pricerQueue) {
        _pricerQueue = pricerQueue;
    }


    public void Start() {
        _queueListener = new QueueListener<Quote>(_pricerQueue.GetPricingRequestQueue(),  quote -> {
            var quotePrice = PriceQuote(quote);
            _pricerQueue.GetPricingReplyQueue().add(quotePrice);
        });

        _queueListener.Start();
    }

    public void Stop() {
        _queueListener.Stop();
    }

    private QuotePrice PriceQuote(Quote quote) {
        var random = new Random();
        var variation = (((Double) random.nextDouble()) * 2.0 - 1.0) / 100.0;
        var newPrice = GetCurrencyPairCoefficient(quote.getCurrencyPair()) + variation;
        BigDecimal bigDecimal = new BigDecimal(newPrice).setScale(5, RoundingMode.DOWN);
        var roundedNewPrice = bigDecimal.doubleValue();
        var quotePrice = new QuotePrice();
        quotePrice.Quote = quote;
        quotePrice.Price = roundedNewPrice;
        return quotePrice;
    }

    private Double GetCurrencyPairCoefficient(CurrencyPair currencyPair) {
        return GetCurrencyCoefficient(currencyPair.getCurrency1()) / GetCurrencyCoefficient(currencyPair.getCurrency2());
    }

    private Double GetCurrencyCoefficient(String currency) {
        switch (currency) {
            case "EUR":
                return 0.99;
            case "USD":
                return 1.0;
            case "CAD":
                return 0.74;
            case "GBP":
                return 1.13;
            case "JPY":
                return 0.0068;
        }
        return 1.0;
    }
}
