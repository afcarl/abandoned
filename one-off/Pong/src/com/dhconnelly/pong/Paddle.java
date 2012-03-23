package com.dhconnelly.pong;

import java.awt.Color;
import java.awt.Shape;
import java.awt.geom.Point2D;
import java.awt.geom.Rectangle2D;

import com.dhconnelly.pong.physics.PhysicalObject;
import com.dhconnelly.pong.render.Drawable;

public class Paddle implements Drawable, PhysicalObject {

    private static final Color COLOR = Color.RED;
    private static final double WIDTH = 100;
    private static final double HEIGHT = 20;
    private static final double SHIFT_VX = 700.0;

	private double x;
	private double y;
	
	private double vx;
	private double vy;
	
	private int score;
	
	public Paddle(double x, double y) {
		this.x = x;
		this.y = y;
	}
	
	public synchronized Point2D getPosition() {
		return new Point2D.Double(x, y);
	}
	
	public synchronized double getX() {
	    return x;
	}
	
	public synchronized void setX(double x) {
	    this.x = x;
	}
	
	public synchronized double getY() {
	    return y;
	}
	
	public synchronized void setY(double y) {
	    this.y = y;
	}

	public synchronized double getVx() {
        return vx;
    }

    public synchronized void setVx(double vx) {
        this.vx = vx;
    }

    public synchronized double getVy() {
        return vy;
    }

    public synchronized void setVy(double vy) {
        this.vy = vy;
    }

    public double getWidth() {
	    return WIDTH;
	}
	
	public double getHeight() {
	    return HEIGHT;
	}
	
    @Override
    public Color getColor() {
        return COLOR;
    }

    @Override
    public synchronized Shape getShape() {
        return new Rectangle2D.Double(x, y, WIDTH, HEIGHT);
    }

    public synchronized void setScore(int score) {
        this.score = score;
    }

    public synchronized int getScore() {
        return score;
    }

    public synchronized void goLeft() {
        this.vx = -SHIFT_VX;
    }
    
    public synchronized void goRight() {
        this.vx = SHIFT_VX;
    }
    
    public synchronized void stop() {
        this.vx = 0.0;
    }
}
