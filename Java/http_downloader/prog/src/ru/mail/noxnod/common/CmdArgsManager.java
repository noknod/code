/**
 * 
 */
package ru.mail.noxnod.common;

import java.util.HashMap;

/**
 * @author MF
 *
 */
public class CmdArgsManager {

	public HashMap<String, String> convert(String [] args) {
		HashMap<String, String> ret = new HashMap<String, String>();
		if (args == null) {
			return null;
		}
		int cnt = args.length;
		int index = 0;
		while (index < cnt) {
			String key = args[index];
			index += 1;
			if (index >= cnt) {
				ret.put(key, "");
				return ret;
			}
			String arg = args[index];
			if (arg.endsWith("\"") && arg.startsWith("\"")) {
				arg = arg.substring(1, arg.length() - 1);
			}
			ret.put(key, arg);
			index += 1;
		}
		return ret;
	}
}
