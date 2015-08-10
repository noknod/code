/**
 * 
 */
package ru.mail.noxnod.job;

import java.util.concurrent.BlockingQueue;

/**
 * @author MF
 *
 */
public abstract class RunnableJob extends Job implements Runnable {

	public RunnableJob(BlockingQueue<JobItem> aqueue, int athread) {
		super(aqueue, athread);
	}

	@Override
	public void run() {
		work();
	}

	protected abstract void begin();
	protected abstract void newJob();
	protected abstract void endJob();
	protected abstract void done();
}
