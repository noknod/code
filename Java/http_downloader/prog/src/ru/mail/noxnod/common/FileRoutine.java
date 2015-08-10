/**
 * 
 */
package ru.mail.noxnod.common;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URL;
import java.net.URLConnection;
import java.util.Date;


/**
 * @author MF
 *
 */
public class FileRoutine {

	public boolean deleteFile(String dest) {
		File file = new File(dest);
        if (file.exists()) {
        	return file.delete();
        }
        return false;
	}

	public int copy(String dest, String source, boolean aoverwrite) throws IOException {
        return copy(dest, (InputStream) new FileInputStream(source), aoverwrite);
	}

	public int copy(String dest, InputStream input, boolean aoverwrite) throws FileNotFoundException, IOException {
		File file = new File(dest);
        if (file.exists()) {
        	if (!aoverwrite) {
        		return -1;
        	}
        	file.delete();
        }
        file.createNewFile();
		return doCopy(new FileOutputStream(dest), input);
	}

	public int download(String dest, String aurl, boolean aoverwrite) throws IOException {
        return copy(dest, new URL(aurl).openConnection().getInputStream(),
        		aoverwrite);
	}

	public int download(String dest, URLConnection aurl, boolean aoverwrite) throws IOException {
        return copy(dest, aurl.getInputStream(), aoverwrite);
	}

	public int downloadLimited(String dest, String aurl, boolean aoverwrite, int aspeed) throws IOException, InterruptedException {
		File file = new File(dest);
        if (file.exists()) {
        	if (!aoverwrite) {
        		return -1;
        	}
        	file.delete();
        }
        file.createNewFile();
		int ret = 0;
        OutputStream output = new FileOutputStream(dest);
    	try {
			InputStream input = new URL(aurl).openConnection().getInputStream();
    		try {
    			byte[] bytes = new byte[30];
    			int bytesRead = 0;
    			long start = new Date().getTime();
    			long estimate = 0;
    			long current = 0;
    			int bytesWrited = 0;
    			while((bytesRead = input.read(bytes)) > 0) {
    				output.write(bytes, 0, bytesRead);
    				bytesWrited += bytesRead;
    				ret += bytesRead;
    				current = new Date().getTime();
    				estimate = 1000 - (current - start);
    				if (estimate <= 0) {
    					start = current;
    					bytesWrited = 0;
    				}
    				else {
    					if (bytesWrited >= aspeed) {
    						Thread.sleep(estimate);
    					}
    				}
    			}
    		}
    		finally {
    	        input.close();
    		}
    	}
    	finally {
	        output.close();
    	}
    	return ret;
	}

	private int doCopy(OutputStream output, InputStream input) throws IOException {
		int ret = 0;
    	byte[] bytes = new byte[30];
    	int bytesRead = 0;
    	try {
        	while((bytesRead = input.read(bytes)) > 0) {
        		output.write(bytes, 0, bytesRead);
        		ret += bytesRead;
        	}
    	}
    	finally {
	        input.close();
	        output.close();
    	}
    	return ret;
	}
}
