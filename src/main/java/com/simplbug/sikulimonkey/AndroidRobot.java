package com.simplbug.sikulimonkey;

import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.IOException;

import javax.imageio.ImageIO;

import org.python.core.PyInteger;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.core.PyTuple;
import org.python.core.PyUnicode;
import org.sikuli.script.Debug;
import org.sikuli.script.IRobot;
import org.sikuli.script.Location;
import org.sikuli.script.ScreenImage;

import com.android.monkeyrunner.MonkeyDevice;

public class AndroidRobot implements IRobot {

    private MonkeyDevice _device;

    public AndroidRobot(MonkeyDevice dev) {
        _device = dev;
    }

    @Override
    public ScreenImage captureScreen(Rectangle rect) {
        try {
            Debug.history("Take a screenshot from the device...");
            byte[] bytes = _device.takeSnapshot().convertToBytes(new PyObject[0], null); // PNG
            BufferedImage screen = ImageIO.read(new ByteArrayInputStream(bytes));
            BufferedImage part = screen.getSubimage(rect.x, rect.y, rect.width, rect.height);
            return new ScreenImage(rect, part);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private Rectangle _bounds; // cache

    public Rectangle getBounds() {
        if (_bounds != null)
            return _bounds;

        int width = Integer.parseInt(_device.getProperty(new PyObject[] { new PyString("display.width") }, null));
        int height = Integer.parseInt(_device.getProperty(new PyObject[] { new PyString("display.height") }, null));
        _bounds = new Rectangle(0, 0, width, height);

        return _bounds;
    }

    private String _model; // cache

    public String getModel() {
        if (_model != null) return _model;

        _model = _device.getProperty(new PyObject[] { new PyString("build.model") }, null);
        return _model;
    }

    public int type(String text) {
        _device.type(new PyObject[] { new PyUnicode(text) }, null);
        return 1;
    }

    public void tap(int x, int y) {
        _device.touch(new PyObject[] { new PyInteger(x), new PyInteger(y), new PyString("DOWN_AND_UP")}, null);
    }

    public void longPress(int x, int y) {
        PyTuple point = new PyTuple(new PyInteger(x), new PyInteger(y));
        _device.drag(new PyObject[] { point, point, new PyInteger(2), new PyInteger(2) }, null);
    }

    public void pressHome() {
        pressHome(0);
    }

    public void pressHome(float durationSec) {
        press("KEYCODE_HOME", durationSec);
    }

    public void pressMenu() {
        press("KEYCODE_MENU", 0);
    }

    public void pressBack() {
        press("KEYCODE_BACK", 0);
    }

    public void pressSearch() {
        press("KEYCODE_SEARCH", 0);
    }

    public void pressEnter() {
        press("KEYCODE_ENTER", 0);
    }

    public void pressBackspace() {
        press("KEYCODE_DEL", 0);
    }

    public void pressDpadUp() {
        press("KEYCODE_DPAD_UP", 0);
    }

    public void pressDpadDown() {
        press("KEYCODE_DPAD_DOWN", 0);
    }

    public void pressDpadLeft() {
        press("KEYCODE_DPAD_LEFT", 0);
    }

    public void pressDpadRight() {
        press("KEYCODE_DPAD_RIGHT", 0);
    }

    public void pressDpadCenter() {
        pressDpadCenter(0);
    }

    public void pressDpadCenter(float durationSec) {
        press("KEYCODE_DPAD_CENTER", durationSec);
    }

    private void press(String keycodeName, float durationSec) {
        sleep(1);
        if (durationSec == 0) {
            _device.press(new PyObject[] { new PyString(keycodeName), new PyString(MonkeyDevice.DOWN_AND_UP) }, null);
        } else {
            _device.press(new PyObject[] { new PyString(keycodeName), new PyString(MonkeyDevice.DOWN) }, null);
            sleep(durationSec);
            _device.press(new PyObject[] { new PyString(keycodeName), new PyString(MonkeyDevice.UP) }, null);
        }
    }

    private static void sleep(float seconds) {
        try {
            Thread.sleep((long)(seconds * 1000));
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void delay(int ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public Object getDevice() {
        return _device;
    }

    @Override
    public void dragDrop(Location start, Location end, int steps, long ms, int buttons) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void keyPress(int keycode) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void keyRelease(int keycode) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void mouseMove(int x, int y) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void mousePress(int buttons) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void mouseRelease(int buttons) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void mouseWheel(int wheelAmt) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void pressModifiers(int modifiers) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void releaseModifiers(int modifiers) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void setAutoDelay(int ms) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void smoothMove(Location dest) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void smoothMove(Location src, Location dest, long ms) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void typeChar(char character, KeyMode mode) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void waitForIdle() {
        throw new UnsupportedOperationException();
    }

}
