package com.dhconnelly.pong;

import java.awt.Color;
import java.awt.Shape;
import java.awt.geom.Point2D;
import java.awt.geom.Rectangle2D;

import com.dhconnelly.pong.physics.PhysicalObject;
import com.dhconnelly.pong.render.Drawable;

public class Ball implements Drawable, PhysicalObject {

    private static final Color COLOR = Color.YELLOW;
    private static final double RADIUS = 15;
    private static final double LAUNCH_BALL_VX = 150.0;
    private static final double LAUNCH_BALL_VY = 150.0;

    private boolean launched;

    private double x;
    private double y;
    
    private double vx;
    private double vy;
    
    public Ball(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public synchronized Point2D getPosition() {
        return new Point2D.Double(x, y);
    }

    @Override
    public Color getColor() {
        return COLOR;
    }

    @Override
    public synchronized Shape getShape() {
        return new Rectangle2D.Double(x, y, RADIUS, RADIUS);
    }

    @Override
    public synchronized double getX() {
        return x;
    }

    @Override
    public synchronized double getY() {
        return y;
    }

    @Override
    public synchronized double getVx() {
        return vx;
    }

    @Override
    public synchronized double getVy() {
        return vy;
    }

    @Override
    public synchronized void setX(double x) {
        this.x = x;
    }

    @Override
    public synchronized void setY(double y) {
        this.y = y;
    }

    @Override
    public synchronized void setVx(double vx) {
        this.vx = vx;
    }

    @Override
    public synchronized void setVy(double vy) {
        this.vy = vy;
    }

    @Override
    public double getWidth() {
        return RADIUS;
    }

    @Override
    public double getHeight() {
        return RADIUS;
    }
    
    public synchronized boolean isLaunched() {
        return launched;
    }

    public synchronized void launch() {
        vx = LAUNCH_BALL_VX;
        vy = LAUNCH_BALL_VY;
        launched = true;
    }
    
    public synchronized void stop() {
        vx = 0;
        vy = 0;
        launched = false;
    }
}
