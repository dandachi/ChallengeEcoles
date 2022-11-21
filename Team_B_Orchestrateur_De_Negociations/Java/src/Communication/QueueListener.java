package Communication;

import java.util.concurrent.*;
import java.util.function.Consumer;

public class QueueListener<T> {
    private FutureTask _listenerTask;
    private final ExecutorService _executorService;

    private QueueListener() {
        _executorService = Executors.newSingleThreadExecutor();
    }

    public QueueListener(BlockingQueue<T> blockingQueue, Consumer<T> queueConsumer){
        this();

        _listenerTask = new FutureTask(new Callable() {
            @Override
            public Object call() throws Exception {
                try{
                    while(true) {
                        T element = blockingQueue.take();
                        queueConsumer.accept(element);
                    }

                }
                catch (InterruptedException ex){
                    return null;
                }
            }
        });
    }

    public void Start(){
        _executorService.submit(_listenerTask);
    }

    public void Stop(){
        _listenerTask.cancel(true);
        _executorService.shutdown();
    }

}
