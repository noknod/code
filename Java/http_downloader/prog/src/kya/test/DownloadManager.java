/**
 * 
 */
package kya.test;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.TimeZone;

import ru.mail.noxnod.common.MsgOutManager;
import ru.mail.noxnod.job.CallableJob;
import ru.mail.noxnod.job.JobInitializer;
import ru.mail.noxnod.job.RunnableJobManagerEx;

/**
 * @author MF
 *
 */
public class DownloadManager extends RunnableJobManagerEx<int[]> {

	public DownloadManager(int athreads, JobInitializer ainit, MsgOutManager amngr) {
		super(athreads, ainit);
		msgMngr = amngr;
		result = new int[6];
	}

	/* (non-Javadoc)
	 * @see ru.mail.noxnod.job.RunnableJobManager#readJob(int)
	 */
	@Override
	protected CallableJob<int[]> readJob(int athread) {
		return new DownloadJob(queue, athread, msgMngr);
	}

	/* (non-Javadoc)
	 * @see ru.mail.noxnod.job.RunnableJobManager#begin()
	 */
	@Override
	protected void begin() {
		msgMngr.logln("*** Manager begin");
		System.out.println("Download start");
		start = System.currentTimeMillis();//new Date().getTime();
	}

	/* (non-Javadoc)
	 * @see ru.mail.noxnod.job.RunnableJobManager#done()
	 */
	@Override
	protected void done() {
		msgMngr.logln("*** Manager done");
		String error = "";
		if (result[4] > 0 || result[5] > 0) {
			error = " (errors: download " + result[4] + " and copy " + result[5] + ")";
		}
		DateFormat dateFormat = new SimpleDateFormat("HH:mm:ss:SSS");
		dateFormat.setTimeZone(TimeZone.getTimeZone("GMT+0"));
		Date diff = new Date(System.currentTimeMillis() - start);
		System.out.println("Done by " + dateFormat.format(diff) + " with downloaded " +
		        result[0] + " file(s) by " + result[1] + " bytes and copied " + result[2] + 
				" file(s) from needed " + result[3] + error);
	}

	@Override
	protected void processResult(int[] current) {
		result[0] += current[0];
		result[1] += current[1];
		result[2] += current[2];
		result[3] += current[3];
		result[4] += current[4];
		result[5] += current[5];
	}

	@Override
	protected void handleInterruptedException(int i, Exception e) {
		msgMngr.error("!*! thread " + i + " interrupted while process result", e);
	}

	@Override
	protected void handleExecutionException(int i, Exception e) {
		msgMngr.error("!*! thread " + i + " has ExecutionException while process result", e);
	}

	private MsgOutManager msgMngr;
	private long start = 0;
}
