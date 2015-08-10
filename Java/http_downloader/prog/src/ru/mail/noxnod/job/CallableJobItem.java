/**
 * 
 */
package ru.mail.noxnod.job;

import java.util.concurrent.Callable;

/**
 * @author MF
 *
 */
public abstract class CallableJobItem<T> extends JobItem implements Callable<T>{

	public T getResult() {
		return result; 
	}

	@Override
	public T call() {
		work();
		return result;
	}

	protected T result;
}
