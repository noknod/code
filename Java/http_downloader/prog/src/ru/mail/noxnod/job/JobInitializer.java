/**
 * 
 */
package ru.mail.noxnod.job;

import java.util.HashMap;
import java.util.concurrent.BlockingQueue;

import ru.mail.noxnod.common.ResultCode;

/**
 * @author MF
 *
 */
public abstract class JobInitializer {

	protected JobInitializer() {
		status = ResultCode.INITIALIZE;
	}

	public JobInitializer(HashMap<String, String> aargs) {
		super();
		setArgs(aargs);
		status = ResultCode.READY;
	}

	public int doInit() {
		init();
		return getStatus();
	}

	public void setArgs(HashMap<String, String> aargs) {
		args = aargs;
	}

	public int getStatus() {
		return status.getValue();
	}

	public BlockingQueue<JobItem> getJobs() {
		if (status != ResultCode.OK) {
			return null;
		}
		BlockingQueue<JobItem> ret = readQueue();
		ret.addAll(jobs);
		jobs.clear();
		status = ResultCode.READY;
		return ret;
	}

	protected abstract void init();
	protected abstract BlockingQueue<JobItem> readQueue();

	protected ResultCode status = ResultCode.INITIALIZE;
	protected BlockingQueue<JobItem> jobs = null;
	protected HashMap<String, String> args = null;
}
