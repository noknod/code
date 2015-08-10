/**
 * 
 */
package ru.mail.noxnod.job;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.Callable;

/**
 * @author MF
 * @param <T>
 *
 */
public abstract class CallableJob<T> extends Job implements Callable<T> {

	public CallableJob(BlockingQueue<JobItem> aqueue, int athread) {
		super(aqueue, athread);
	}

	@Override
	public T call() {
		work();
		return result;
	}
	
	protected T result;
}
