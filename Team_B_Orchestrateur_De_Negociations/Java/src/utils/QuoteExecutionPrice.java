package utils;

public class QuoteExecutionPrice {
    public Quote Quote;
    public Double ExecutionPrice;

    public ExecutionStatus Status;
    @Override
    public String toString() {
        return Quote + ": ExecutionPrice=" + ExecutionPrice + " Execution Status="+Status;
    }
}
