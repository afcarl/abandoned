package com.dhconnelly.pong.physics;

public interface PhysicalObject {
    public double getX();
    public double getY();
    public double getVx();
    public double getVy();
    public void setX(double x);
    public void setY(double y);
    public void setVx(double x);
    public void setVy(double y);
    public double getWidth();
    public double getHeight();
}
