/**
 * 
 */
package ru.mail.noxnod.job;

import ru.mail.noxnod.common.ResultCode;


/**
 * @author MF
 *
 */
public abstract class JobItem {

	protected JobItem() {
		super();
		status = ResultCode.INITIALIZE;
	}

	public void doJob() {
		work();
	}

	public void setDummy() {
		dummy = true;
	}

	public boolean isDummy() {
		return dummy;
	}

	public int getStatus() {
		return status.getValue();
	}

	protected abstract void work();

	protected ResultCode status = ResultCode.INITIALIZE;
	
	private boolean dummy = false;
}