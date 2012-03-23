package com.dhconnelly.pong;

import java.util.Arrays;
import java.util.List;

import com.dhconnelly.pong.physics.PhysicalObject;
import com.dhconnelly.pong.render.Drawable;

public class World {

	private static final double DEFAULT_PLAYER_X = 650;
	private static final double DEFAULT_PLAYER_Y = 530;
	private static final double DEFAULT_OPPONENT_X = 50;
	private static final double DEFAULT_OPPONENT_Y = 50;
	private static final double DEFAULT_BALL_X = 400;
	private static final double DEFAULT_BALL_Y = 300;
    
	private final Paddle player = new Paddle(DEFAULT_PLAYER_X, DEFAULT_PLAYER_Y);
	private final Paddle opponent = new Paddle(DEFAULT_OPPONENT_X, DEFAULT_OPPONENT_Y);
	private final Ball ball = new Ball(DEFAULT_BALL_X, DEFAULT_BALL_Y);
	private final double leftBoundary;
	private final double rightBoundary;
	private final double topBoundary;
	private final double bottomBoundary;

	public World(double leftBoundary, double rightBoundary, double topBoundary, double bottomBoundary) {
	    this.leftBoundary = leftBoundary;
	    this.rightBoundary = rightBoundary;
	    this.topBoundary = topBoundary;
	    this.bottomBoundary = bottomBoundary;
	}
	
	public List<Drawable> getDrawables() {
	    return Arrays.asList(player, opponent, (Drawable) ball); // wtf
	}
	
	public List<PhysicalObject> getPhysicalObjects() {
	    return Arrays.asList(player, opponent, (PhysicalObject) ball); // wtf
	}
	
	public Paddle getPlayer() {
		return player;
	}

	public Paddle getOpponent() {
		return opponent;
	}

	public Ball getBall() {
		return ball;
	}
	
	public double getLeftBoundary() {
	    return leftBoundary;
	}
	
	public double getRightBoundary() {
	    return rightBoundary;
	}

    public double getTopBoundary() {
        return topBoundary;
    }

    public double getBottomBoundary() {
        return bottomBoundary;
    }

    public void resetPositions() {
        synchronized (player) {
            player.setX(DEFAULT_PLAYER_X);
            player.setY(DEFAULT_PLAYER_Y);
            player.stop();
        }
        synchronized (opponent) {
            opponent.setX(DEFAULT_OPPONENT_X);
            opponent.setY(DEFAULT_OPPONENT_Y);
            opponent.stop();
        }
        synchronized (ball) {
            ball.setX(DEFAULT_BALL_X);
            ball.setY(DEFAULT_BALL_Y);
            ball.stop();
        }
    }

}
