/**
 * 
 */
package ru.mail.noxnod.common;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.charset.Charset;

/**
 * @author MF
 *
 */
public class MsgOutManager {

	public MsgOutManager () {
		setOut(System.out);
		setEr(System.err);
	}

	public MsgOutManager (OutputStream aout) {
		setOut(aout);
		setEr(System.err);
	}

	public MsgOutManager (OutputStream aout, OutputStream aer) {
		setOut(aout);
		setEr(aer);
	}

	public void setOut(OutputStream aout) {
		out = aout;
	}

	public void setEr(OutputStream aer) {
		if (aer != null) {
			er = aer;
		}
		else {
			er = System.err;
		}
	}

	public synchronized void log(String amsg) {
		if (out != null) {
			try {
				out.write(amsg.getBytes(Charset.forName("UTF-8")));
				out.flush();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	public synchronized void logln(String amsg) {
		log(amsg + OSChar.lineSeparator);
	}

	public synchronized void error(String amsg) {
		if (er != null) {
			try {
				er.write(amsg.getBytes(Charset.forName("UTF-8")));
				er.flush();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

	public synchronized void error(String amsg, Throwable ast) {
		if (er != null) {
			error(amsg + convertStackTrace(ast) + OSChar.lineSeparator);
		}
	}

	public synchronized void errorln(String amsg) {
		error(amsg + OSChar.lineSeparator);
	}

	public synchronized String convertStackTrace(Throwable ast) {
		StringWriter stringWriter = new StringWriter();
		PrintWriter printWriter = new PrintWriter(stringWriter);
		ast.printStackTrace(printWriter);
		return stringWriter.toString();
	}

	private volatile OutputStream out = null;
	private volatile OutputStream er = null;
}
