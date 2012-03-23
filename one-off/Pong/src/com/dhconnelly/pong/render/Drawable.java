package com.dhconnelly.pong.render;

import java.awt.Color;
import java.awt.Shape;
import java.awt.geom.Point2D;

public interface Drawable {
    public Color getColor();
    public Shape getShape();
    public Point2D getPosition();
}
