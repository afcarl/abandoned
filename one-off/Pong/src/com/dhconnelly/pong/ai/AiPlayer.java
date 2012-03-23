package com.dhconnelly.pong.ai;

import java.util.logging.Logger;

import com.dhconnelly.pong.Ball;
import com.dhconnelly.pong.Paddle;
import com.dhconnelly.pong.World;

public class AiPlayer implements Runnable {

    private static final Logger log = Logger.getLogger(AiPlayer.class.getName());
    private static final long REFRESH_RATE = 50; // fps
    
    private final World world;
    private final Paddle paddle;
    
    public AiPlayer(World world, Paddle paddle) {
        this.world = world;
        this.paddle = paddle;
    }

    @Override
    public void run() {
        while (true) {
            Ball ball = world.getBall();
            synchronized (ball) {
                double ballYDist = Math.abs(ball.getY() - paddle.getY());
                double height = Math.abs(world.getTopBoundary() - world.getBottomBoundary());
                double dy = ball.getVy() / Math.abs(ball.getVy());
                boolean towardsPaddle = Math.abs(paddle.getY() - (ball.getY() + dy)) < Math.abs(paddle.getY() - ball.getY()); 
                if (ballYDist < height / 2 && towardsPaddle) {
                    double halfFromCenterLeft = paddle.getX() + paddle.getWidth() / 4;
                    double halfFromCenterRight = paddle.getX() + paddle.getWidth() / 2;

                    // calculate anticipated ballCenter when ball.y == paddle.y
                    double time = ballYDist / Math.abs(ball.getVy());
                    double ballCenter = ball.getX() + ball.getVx() * time + ball.getWidth() / 2;
                    
                    if (paddle.getX() + paddle.getWidth() < ballCenter) {
                        paddle.goRight();
                    } else if (paddle.getX() > ballCenter) {
                        paddle.goLeft();
                    } else if (ballCenter >= halfFromCenterLeft && ballCenter <= halfFromCenterRight) {
                        paddle.stop();
                    }
                }
            }
            
            try {
                Thread.sleep(1000 / REFRESH_RATE);
            } catch (InterruptedException e) {
                log.info("Thread interrupted while sleeping");
            }
        }
    }

}
