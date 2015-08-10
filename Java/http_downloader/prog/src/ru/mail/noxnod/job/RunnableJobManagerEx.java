/**
 * 
 */
package ru.mail.noxnod.job;

import java.util.ArrayList;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;
import java.util.concurrent.FutureTask;

import ru.mail.noxnod.common.ResultCode;

/**
 * @author MF
 *
 */
public abstract class RunnableJobManagerEx<T> extends RunnableJobItem {

	public RunnableJobManagerEx(JobInitializer ainit) {
		init(ainit);
		tasks = new ArrayList<Future<T>>();
	}

	public RunnableJobManagerEx(int athreads, JobInitializer ainit) {
		countThread = athreads;
		init(ainit);
		tasks = new ArrayList<Future<T>>();
	}

	public T getResult() {
		return result;
	}

	protected void init(JobInitializer ainit) {
		status = ResultCode.INITIALIZE;
		if (queue != null) {
			queue.clear(); 
		}
		int tmp = ainit.doInit(); 
		if (tmp == ResultCode.OK.getValue()) {
			queue = ainit.getJobs();
			status = ResultCode.READY;
		}
	}

	/* (non-Javadoc)
	 * @see ru.mail.noxnod.job.JobItem#work()
	 */
	@Override
	protected void work() {
		if (status != ResultCode.READY) {
			return;
		}
		begin();
		tasks.clear();
		FutureTask<T> task = null;
		for (int i = 1; i <= countThread; ++i) {
			Callable<T> job = readJob(i);
			task = new FutureTask<T>(job);
			Thread thread = new Thread(task);
			tasks.add(task);
			thread.start();
		}
		for (int i = 0; i < tasks.size(); ++i) {
			try {
				processResult(tasks.get(i).get());
			} catch (InterruptedException e) {
				handleInterruptedException(i, e);
			} catch (ExecutionException e) {
				handleExecutionException(i, e);
			}
		}
		status = ResultCode.OK;
		done();
	}

	protected abstract CallableJob<T> readJob(int athread);
	protected abstract void processResult(T current);
	protected abstract void begin();
	protected abstract void done();
	protected abstract void handleInterruptedException(int i, Exception e);
	protected abstract void handleExecutionException(int i, Exception e);

	protected BlockingQueue<JobItem> queue = null;
	protected ArrayList<Future<T>> tasks = null;

	protected T result;
	
	private int countThread = 0;
}
