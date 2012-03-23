package com.dhconnelly.pong.physics;

import java.util.List;
import java.util.logging.Logger;

import com.dhconnelly.pong.Ball;
import com.dhconnelly.pong.Game;
import com.dhconnelly.pong.Paddle;
import com.dhconnelly.pong.World;

public class PhysicsHandler implements Runnable{

    private static final Logger log = Logger.getLogger(PhysicsHandler.class.getName());
    private static final double BALL_COLLISION_SHIFT = 5;
    private static final int REFRESH_RATE = 50; // fps
    private final Game game;
    private final World world;
    private long lastRefresh = -1;
    
    public PhysicsHandler(Game game, World world) {
        this.world = world;
        this.game = game;
    }
    
    @Override
    public void run() {
        while (true) {
            if (lastRefresh == -1) {
                lastRefresh = System.currentTimeMillis();
                continue;
            }
            
            double dt = (System.currentTimeMillis() - lastRefresh) / 1000.0;
            List<PhysicalObject> stuff = world.getPhysicalObjects();
            for (PhysicalObject obj : stuff) {
                applyMomentum(dt, obj);
                detectCollisions(obj);
            }

            lastRefresh = System.currentTimeMillis();
            try {
                Thread.sleep(1000 / REFRESH_RATE);
            } catch (InterruptedException e) {
                log.info("Thread interrupted while sleeping");
            }
        }
    }
    
    private void applyMomentum(double dt, PhysicalObject obj) {
        synchronized (obj) {
            double dx = obj.getVx() * dt;
            double dy = obj.getVy() * dt;
            obj.setX(obj.getX() + dx);
            obj.setY(obj.getY() + dy);
        }
    }

    private void detectCollisions(PhysicalObject obj) {
        // since this is pong and collisions don't conserve momentum, we
        // have to check to see what we are and what we hit
        if (obj instanceof Paddle) {
            synchronized (obj) {
                if (obj.getX() < world.getLeftBoundary()) {
                    obj.setX(world.getLeftBoundary());
                } else if (obj.getX() + obj.getWidth() > world.getRightBoundary()) {
                    obj.setX(world.getRightBoundary() - obj.getWidth());
                }
            }
        } else if (obj instanceof Ball) {
            synchronized (obj) {
                if (obj.getX() < world.getLeftBoundary()) {
                    obj.setX(world.getLeftBoundary());
                    obj.setVx(-obj.getVx());
                } else if (obj.getX() + obj.getWidth() > world.getRightBoundary()) {
                    obj.setX(world.getRightBoundary() - obj.getWidth());
                    obj.setVx(-obj.getVx());
                } else if (obj.getY() < world.getTopBoundary()) {
                    game.playerScored();
                } else if (obj.getY() + obj.getHeight() > world.getBottomBoundary()) {
                    game.opponentScored();
                } else {
                    // TODO better detection: hitting sides of paddle, etc
                    Paddle paddle = world.getPlayer();
                    synchronized (paddle) {
                        if (obj.getX() >= paddle.getX() &&
                                obj.getX() + obj.getWidth()
                                    <= paddle.getX() + paddle.getWidth() &&
                                obj.getY() + obj.getHeight() >= paddle.getY()) {
                            log.info("boom");
                            obj.setVy(-obj.getVy());
                            obj.setY(obj.getY() - BALL_COLLISION_SHIFT);
                            log.info("VY = " + obj.getVy());
                        }
                    }
                    
                    paddle = world.getOpponent();
                    synchronized (paddle) {
                        if (obj.getX() >= paddle.getX() &&
                                obj.getX() + obj.getWidth()
                                    <= paddle.getX() + paddle.getWidth() &&
                                obj.getY() <= paddle.getY() + paddle.getHeight()) {
                            log.info("boom");
                            obj.setVy(-obj.getVy());
                            obj.setY(obj.getY() + BALL_COLLISION_SHIFT);
                            log.info("VY = " + obj.getVy());
                        }
                    }
                }
            }
        }
    }
}
