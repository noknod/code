/**
 * 
 */
package ru.mail.noxnod.job;

import java.util.concurrent.BlockingQueue;


import ru.mail.noxnod.common.ResultCode;

/**
 * @author MF
 *
 */
public abstract class RunnableJobManager extends RunnableJobItem {

	public RunnableJobManager(JobInitializer ainit) {
		init(ainit);
	}

	public RunnableJobManager(int athreads, JobInitializer ainit) {
		countThread = athreads;
		init(ainit);
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

	protected void work() {
		if (status != ResultCode.READY) {
			return;
		}
		begin();
		if (countThread == 0) {
			JobItem job = null;
			while ((job = queue.poll()) != null ) {
				if (!job.isDummy()) {
					job.doJob();
				}
			}
		}
		else {
			for (int i = 1; i <= countThread; ++i) {
				Thread thread = new Thread(readJob(i));
				thread.start();
			}
		}
		status = ResultCode.OK;
		done();
	}

	protected abstract RunnableJob readJob(int athread);
	protected abstract void begin();
	protected abstract void done();

	protected BlockingQueue<JobItem> queue = null;

	private int countThread = 0;
}
