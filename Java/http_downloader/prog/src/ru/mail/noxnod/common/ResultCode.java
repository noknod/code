/**
 * 
 */
package ru.mail.noxnod.common;

/**
 * @author MF
 *
 */
public enum ResultCode {
	OK(0),
	INITIALIZE(1),
	READY(2),
	SOMETHING_WRONG(-1),
	ERROR_CREATE_FILE(-2),
	ERROR_OPEN_FILE(-3),
	ERROR_COPY_FILE(-4),
	ERROR_PARSE_FILE(-5),
	ERROR_OPEN_URL(-6);

	private ResultCode(int avalue) {
	    value = avalue;
	}

	public int getValue() {
		return value;
	}

	@Override
	public String toString() {
	    switch(this) {
	        case OK:
	            return "OK: " + value;
	        case INITIALIZE:
	            return "INITIALIZE: " + value;
	        case READY:
	            return "READY: " + value;
	        case ERROR_OPEN_FILE:
	            return "ERROR_OPEN_FILE: " + value;
	        case ERROR_PARSE_FILE:
	            return "ERROR_PARSE_FILE: " + value;
	        case SOMETHING_WRONG:
	            return "SOMETHING_WRONG: " + value;
	        case ERROR_CREATE_FILE:
	            return "ERROR_CREATE_FILE: " + value;
	        case ERROR_OPEN_URL:
	            return "ERROR_OPEN_URL: " + value;
	        case ERROR_COPY_FILE:
	            return "ERROR_COPY_FILE: " + value;
	        default:
	            return null;
	    }
	}

	private int value;
}
