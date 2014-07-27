package com.simplbug.sikulimonkey;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.python.util.PythonInterpreter;

import com.google.common.base.Predicate;

public class MonkeyPlugin implements Predicate<PythonInterpreter> {

    @Override
    public boolean apply(PythonInterpreter anInterpreter) {
        anInterpreter.exec(readInitScript());
        return true;
    }

    private static String readInitScript() {
        BufferedReader reader = new BufferedReader(
                new InputStreamReader(MonkeyPlugin.class.getResourceAsStream("initenv.py")));

        StringBuffer buffer = new StringBuffer();
        try {
            String line = reader.readLine();
            while (line != null) {
                buffer.append(line).append('\n');
                line = reader.readLine();
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return buffer.toString();
    }

}
