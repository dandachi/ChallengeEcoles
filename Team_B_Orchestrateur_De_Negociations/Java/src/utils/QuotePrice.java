package utils;

public class QuotePrice {
    public Quote Quote;
    public Double Price;

    @Override
    public String toString() {
        return Quote +": Price=" + Price;
    }
}
