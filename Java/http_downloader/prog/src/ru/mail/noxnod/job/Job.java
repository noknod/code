/**
 * 
 */
package ru.mail.noxnod.job;

import java.util.concurrent.BlockingQueue;

/**
 * @author MF
 *
 */
public abstract class Job {

	public Job(BlockingQueue<JobItem> aqueue, int athread) {
		queue = aqueue;
		numberThread = athread;
	}

	public void work() {
		begin();
		try {
			boolean done = queue.isEmpty();
			while (!done) {
				current = queue.take();
				if (current.isDummy()) {
					queue.put(current);
					done = true;
				}
				else {
					newJob();
					current.doJob();
					endJob();
				}
			}
		}
		catch (InterruptedException e) {
		}
		done();
	}

	protected abstract void begin();
	protected abstract void newJob();
	protected abstract void endJob();
	protected abstract void done();

	protected int numberThread = 0;
	protected BlockingQueue<JobItem> queue = null;
	protected JobItem current = null;
}
