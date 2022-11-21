package utils;

import java.util.Objects;

public class Quote {
    private final int QuoteId;
    private final CurrencyPair CurrencyPair;

    public Quote(int quoteId, utils.CurrencyPair currencyPair) {
        QuoteId = quoteId;
        CurrencyPair = currencyPair;
    }

    public int getQuoteId() {
        return QuoteId;
    }

    public utils.CurrencyPair getCurrencyPair() {
        return CurrencyPair;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Quote quote = (Quote) o;
        return QuoteId == quote.QuoteId && Objects.equals(CurrencyPair, quote.CurrencyPair);
    }

    @Override
    public int hashCode() {
        return Objects.hash(QuoteId, CurrencyPair);
    }

    @Override
    public String toString() {
        return "Quote [" +
                "Id=" + QuoteId +
                ", CurrencyPair=" + CurrencyPair +
                ']';
    }
}
