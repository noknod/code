/**
 * 
 */
package ru.mail.noxnod.job;

/**
 * @author MF
 *
 */
public abstract class RunnableJobItem extends JobItem implements Runnable{

	@Override
	public void run() {
		work();
	}
}
