package com.simplbug.sikulimonkey;

import java.awt.AWTException;
import java.awt.Rectangle;

import org.python.core.PyFloat;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.sikuli.script.Debug;
import org.sikuli.script.FindFailed;
import org.sikuli.script.IRobot;
import org.sikuli.script.IScreen;
import org.sikuli.script.Location;
import org.sikuli.script.Region;
import org.sikuli.script.ScreenImage;

import com.android.monkeyrunner.MonkeyDevice;
import com.android.monkeyrunner.MonkeyRunner;

public class AndroidScreen extends AndroidRegion implements IScreen {

    public AndroidScreen(String serialNumber) throws AWTException {
        MonkeyDevice device = MonkeyRunner.waitForConnection(new PyObject[] { new PyFloat(15), new PyString(serialNumber) }, null);

        try { // waitForConnection() never returns null, even the connection cannot be created.
            String model = device.getProperty(new PyObject[] {new PyString("build.model")}, null);
            Debug.history("Successfully connect to a device. MODEL: " + model);
        } catch (Throwable e) {
            throw new RuntimeException("Failed to connect to a device (within timeout).", e);
        }
        _robot = new AndroidRobot(device);

        // Region's default constructor doesn't use this screen as the default one.
        Rectangle bounds = getBounds();
        super.init(bounds.x, bounds.y, bounds.width, bounds.height, this);
    }

    @Override
    public ScreenImage capture() {
        return _robot.captureScreen(getBounds());
    }

    @Override
    public ScreenImage capture(int x, int y, int width, int height) {
        return _robot.captureScreen(new Rectangle(x, y, width, height));
    }

    @Override
    public ScreenImage capture(Rectangle rect) {
        return _robot.captureScreen(rect);
    }

    @Override
    public ScreenImage capture(Region reg) {
        return _robot.captureScreen(reg.getROI());
    }

    @Override
    public Rectangle getBounds() {
        return _robot.getBounds();
    }

    @Override
    public IRobot getRobot() {
        return _robot;
    }

    public <PSRML> int type(String text) throws FindFailed {
        return _robot.type(text);
    }

    @Override
    public Region newRegion(Rectangle rect) {
        return super.newRegion(rect);
    }

    @Override
    public void showClick(Location loc) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void showDropTarget(Location loc) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void showMove(Location loc) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void showTarget(Location loc) {
        throw new UnsupportedOperationException();
    }

}
