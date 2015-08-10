/**
 * 
 */
package kya.test;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.HashMap;

import ru.mail.noxnod.common.CmdArgsManager;
import ru.mail.noxnod.common.MsgOutManager;
import ru.mail.noxnod.common.OSChar;
import ru.mail.noxnod.common.ResultCode;
import ru.mail.noxnod.job.RunnableJobManagerEx;

/**
 * @author MF
 *
 */
public class Do {

	public Do(String[] aargs) {
		System.out.println("Initializing...");
		args = new CmdArgsManager().convert(aargs);
		System.out.println(args);
		String tmp = args.get(KEY_OUTLOG);
		if (tmp == null) {
			msgMngr = new MsgOutManager();
			msgMngr.setOut(null);
			msgMngr.setEr(null);
		}
		else if (tmp.compareToIgnoreCase("sys") == 0) {
			msgMngr = new MsgOutManager(System.out);
		}
		else {
			File file = new File(tmp);
	        if (file.exists()) {
	        	file.delete();
	        }
			boolean done = false;
			OutputStream os = null;
	        msgMngr = new MsgOutManager();
			try {
				file.createNewFile();
				os = new FileOutputStream(tmp);
				done = true;
			} catch (IOException e) {
				e.printStackTrace();
			}
			if (done) {
		        msgMngr.setOut(os);
			}
		}
		tmp = args.get(KEY_OUTERR);
		if (tmp != null) {
			if (tmp.toLowerCase() == "sys") {
				msgMngr.setEr(System.out);
			}
			else {
				File file = new File(tmp);
				if (file.exists()) {
					file.delete();
				}
				boolean done = false;
				OutputStream os = null;
				try {
					file.createNewFile();
					os = new FileOutputStream(tmp);
					done = true;
				} catch (IOException e) {
					e.printStackTrace();
				}
				if (done) {
					msgMngr.setEr(os);
				}
			}
		}
		msgMngr.logln("- - - - - -");
		msgMngr.logln("*** Initialize");
		tmp = args.get(KEY_DIR);
		if (tmp == null) {
			tmp = VALUE_DIR;
			args.put(KEY_DIR, tmp);
		}
		else {
			if (!tmp.endsWith(OSChar.dirSeparator)) {
				tmp += OSChar.dirSeparator;
				args.put(KEY_DIR, tmp);
			}
		}
		msgMngr.logln("dirStore = " + tmp);
		tmp = args.get(KEY_FILE);
		if (tmp == null) {
			tmp = VALUE_FILE;
			args.put(KEY_FILE, tmp);
		}
		msgMngr.logln("urlFile = " + tmp);
		int numberThread = VALUE_THREAD;
		if (args.containsKey(KEY_THREAD)) {
			numberThread = Integer.parseInt(args.get(KEY_THREAD));
		}
		msgMngr.logln("numberThread = " + numberThread);
		tmp = args.get(KEY_SPEED);
		if (tmp == null) {
			tmp = VALUE_SPEED;
			args.put(KEY_SPEED, tmp);
		}
		else {
			int coef = 1;
			String speedS = tmp;
			if (tmp.toLowerCase().endsWith("k")) {
				speedS = tmp.substring(0, tmp.length() - 1);
				if (speedS == "") {
					speedS = "1024";
				}
				else {
					coef = 1024;
				}
			}
			else if (tmp.toLowerCase().endsWith("m")) {
				speedS = tmp.substring(0, tmp.length() - 1);
				if (speedS == "") {
					speedS = String.valueOf(1024 * 1024);
				}
				else {
					coef = 1024 * 1024;
				}
			}
			tmp = String.valueOf(coef * Integer.parseInt(speedS));
			args.put(KEY_SPEED, tmp);
		}
		msgMngr.logln("speedDownload = " + tmp);
		jobMngr = new DownloadManager(numberThread, 
				new DownloadInitializer(args, msgMngr), msgMngr);
		if (jobMngr.getStatus() == ResultCode.READY.getValue()) {
			status = ResultCode.READY;
		}
		msgMngr.logln("*** Initialize end");
		System.out.println("Initialize done");
	}

	public boolean download() {
		if (status == ResultCode.READY) {
			jobMngr.doJob();
			status = ResultCode.OK;
		}
		else {
			status = ResultCode.INITIALIZE;
		}
		return (status == ResultCode.OK);
	}

	public static final String KEY_DIR = "-o";
	public static final String KEY_SPEED = "-l";
	public static final String KEY_FILE = "-f";
	public static final String KEY_THREAD = "-n";
	public static final String KEY_OUTLOG = "-ml";
	public static final String KEY_OUTERR = "-me";
	private final String VALUE_DIR = ".";
	private final int    VALUE_THREAD = 3;
	private final String VALUE_SPEED = Integer.toString(1024 * 1024);
	private final String VALUE_FILE = System.getProperty("user.dir") + OSChar.dirSeparator + "test.txt";

	private HashMap<String, String> args = null;
	private MsgOutManager msgMngr = null;
	private ResultCode status = ResultCode.INITIALIZE;
	private RunnableJobManagerEx<int[]> jobMngr = null;
}