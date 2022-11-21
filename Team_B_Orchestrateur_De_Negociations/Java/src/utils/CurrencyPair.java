package utils;

import java.util.Objects;

public class CurrencyPair {
    public CurrencyPair(String currency1, String currency2)
    {
        Currency1 = currency1;
        Currency2 = currency2;
    }

    @Override
    public String toString() {
        return Currency1 + '/' + Currency2;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        CurrencyPair that = (CurrencyPair) o;
        return Objects.equals(Currency1, that.Currency1) && Objects.equals(Currency2, that.Currency2);
    }

    @Override
    public int hashCode() {
        return Objects.hash(Currency1, Currency2);
    }

    public String getCurrency1() {
        return Currency1;
    }

    public String getCurrency2() {
        return Currency2;
    }

    private final String Currency1;
    private final String Currency2;
}
