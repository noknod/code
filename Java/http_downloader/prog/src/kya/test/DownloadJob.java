/**
 * 
 */
package kya.test;

import java.util.concurrent.BlockingQueue;

import ru.mail.noxnod.common.MsgOutManager;
import ru.mail.noxnod.job.CallableJob;
import ru.mail.noxnod.job.JobItem;

/**
 * @author MF
 *
 */
public class DownloadJob extends CallableJob<int[]> {

	public DownloadJob(BlockingQueue<JobItem> aqueue, int athread, MsgOutManager amngr) {
		super(aqueue, athread);
		mngr = amngr;
		result = new int[6];
	}

	/* (non-Javadoc)
	 * @see ru.mail.noxnod.job.RunnableJob#begin()
	 */
	@Override
	protected void begin() {
		mngr.logln("> thread " + numberThread + " begin");
	}

	/* (non-Javadoc)
	 * @see ru.mail.noxnod.job.RunnableJob#newJob()
	 */
	@Override
	protected void newJob() {
		mngr.logln(">-- thread " + numberThread + " start job " + current.toString());
	}

	/* (non-Javadoc)
	 * @see ru.mail.noxnod.job.RunnableJob#endJob()
	 */
	@Override
	protected void endJob() {
		int[] tmp = ((DownloadItem) current).getStatistic();
		if (tmp[0] > 0) {
			result[0] += 1;
			result[1] += tmp[0];
		}
		else {
			result[4] += 1;
		}
		result[2] += tmp[1];
		result[3] += tmp[2];
		result[5] += tmp[2] - tmp[1] - 1;
		mngr.logln(">-- thread " + numberThread + " end job");
	}

	/* (non-Javadoc)
	 * @see ru.mail.noxnod.job.RunnableJob#done()
	 */
	@Override
	protected void done() {
		String error = "";
		if (result[4] > 0 || result[5] > 0) {
			error = " (errors: download " + result[4] + " and copy " + result[5] + ")";
		}
		mngr.logln("> thread " + numberThread + " done with downloaded " + result[0] +
				" file(s) by " + result[1] + " bytes and copied " + result[2] + 
				" file(s) from needed " + result[3] + error);
	}

	private MsgOutManager mngr = null;
}
