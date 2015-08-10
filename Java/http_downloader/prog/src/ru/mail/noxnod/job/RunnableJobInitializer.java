/**
 * 
 */
package ru.mail.noxnod.job;

import java.util.HashMap;

/**
 * @author MF
 *
 */
public abstract class RunnableJobInitializer extends JobInitializer implements Runnable{

	public RunnableJobInitializer(HashMap<String, String> aargs) {
		super(aargs);
	}

	@Override
	public void run() {
		init();
	}
}