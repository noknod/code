/**
 * 
 */
package kya.test;

import java.io.IOException;
import java.util.Vector;

import ru.mail.noxnod.common.FileRoutine;
import ru.mail.noxnod.common.MsgOutManager;
import ru.mail.noxnod.common.ResultCode;
import ru.mail.noxnod.job.RunnableJobItem;

/**
 * @author MF
 *
 */
public class DownloadItem extends RunnableJobItem {


	public DownloadItem(String aurl, String afile, MsgOutManager amngr) {
		url = aurl;
		files = new Vector<String>();
		addFile(afile);
		msgMngr = amngr;
		status = ResultCode.READY;
	}

	public static void setSpeed(int aspeed) {
		speedDownload = aspeed;
	}

	public void addFile(String afile) {
		files.add(afile);
		statistic[2] += 1; 
	}

	@Override
	public String toString() {
		String ret = "url = " + url + " - files =";
		for (String file : files) {
			ret += " " + file + ";";
		}
		return ret;
	}

	/**
	 * @return the speedDownload
	 */
	public static int getSpeed() {
		return speedDownload;
	}

	/**
	 * @return the array of 4 element of int:
	 * statistic[0] - bytes downloaded
	 * statistic[1] - files copied
	 * statistic[2] - files total to copy
	 */
	public int[] getStatistic() {
		return statistic;
	}

	/* (non-Javadoc)
	 * @see ru.mail.noxnod.job.JobItem#work()
	 */
	@Override
	protected void work() {
		if (status != ResultCode.READY) {
			return;
		}
		boolean was = false;
		String firstFile = "";
		FileRoutine fileCopy = new FileRoutine(); 
		statistic[0] = 0;
		statistic[1] = 0;
		int tmp = 0;
		for (String file : files) {
			tmp = 0;
			if (!was) {
		        try {
		        	tmp = fileCopy.downloadLimited(file, url, true, speedDownload);
				} catch (IOException e) {
					msgMngr.error("!*! doJob download url = " + url, e);
					status = ResultCode.ERROR_CREATE_FILE;
					fileCopy.deleteFile(file);
					return;
				} catch (InterruptedException e) {
					msgMngr.error("!*! doJob cancel download url = " + url, e);
					status = ResultCode.ERROR_CREATE_FILE;
					fileCopy.deleteFile(file);
					return;
				}
				firstFile = file;
				was = true;
				statistic[0] = tmp;
			}
			else
			{
				try {
					fileCopy.copy(file, firstFile, true);
					tmp = 1;
				} catch (IOException e) {
					msgMngr.error("!*! doJob copy url = " + url + " to file '" + file + "'", e);
					fileCopy.deleteFile(file);
				}
				statistic[1] += tmp;
			}
		}
		status = ResultCode.OK;
	}

	private static int speedDownload = 0;
	private String url = "";
	private Vector<String> files = null;
	private int[] statistic = {0, 0, 0};
	private MsgOutManager msgMngr = null;
}
