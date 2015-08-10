/**
 * 
 */
package kya.test;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import ru.mail.noxnod.common.MsgOutManager;
import ru.mail.noxnod.common.ResultCode;
import ru.mail.noxnod.job.JobItem;
import ru.mail.noxnod.job.RunnableJobInitializer;

/**
 * @author MF
 *
 */
public class DownloadInitializer extends RunnableJobInitializer {

	public DownloadInitializer(HashMap<String, String> aargs, MsgOutManager amngr) {
		super(aargs);
		msgMngr = amngr;
	}

	/* (non-Javadoc)
	 * @see ru.mail.noxnod.job.JobInitializer#init()
	 */
	@Override
	protected void init() {
		String dirStore = args.get(Do.KEY_DIR);
		DownloadItem.setSpeed(Integer.parseInt(args.get(Do.KEY_SPEED)));
		HashMap<String, JobItem> tmp = new HashMap<String, JobItem>();
		if (jobs == null) {
			jobs = readQueue();
		}
		jobs.clear();
		DownloadItem job = null;
		BufferedReader input = null;
		try {
			input = new BufferedReader(new FileReader(args.get(Do.KEY_FILE)));
		} catch (FileNotFoundException e) {
			msgMngr.error("!*! Initialize ERROR_OPEN_FILE", e);
			status = ResultCode.ERROR_OPEN_FILE;
			return;
		}
		try {
			String line = null;
			try {
				line = input.readLine();
			} catch (IOException e) {
				msgMngr.error("!*! Initialize input.readLine()", e);
			}
			while (line != null) {
				String[] tokens = line.split("\\s");
				String url = tokens[0].toLowerCase();
				String loadFile = dirStore + tokens[1];
				job = (DownloadItem) tmp.get(url);
				if (job == null) {
					job = new DownloadItem(url, loadFile, msgMngr);
					tmp.put(url, job);
				}
				else {
					job.addFile(loadFile);
				}
				msgMngr.logln("-");
				msgMngr.logln("read in url = " + tokens[0] + " - file = " + tokens[1]);
				msgMngr.logln(job.toString());
				try {
					line = input.readLine();
				} catch (IOException e) {
					msgMngr.error("!*! Initialize input.readLine()", e);
				}
			}
		} finally {
			try {
				input.close();
			} catch (IOException e) {
				msgMngr.error("!*! Initialize input.close()", e);
			}
		}
		jobs.addAll(tmp.values());
		job = new DownloadItem("", "", msgMngr);
		job.setDummy();
		jobs.add(job);
		status = ResultCode.OK;
	}

	/* (non-Javadoc)
	 * @see ru.mail.noxnod.job.JobInitializer#readQueue()
	 */
	@Override
	protected BlockingQueue<JobItem> readQueue() {
		return new LinkedBlockingQueue<JobItem>();
	}

	private MsgOutManager msgMngr = null;
}
