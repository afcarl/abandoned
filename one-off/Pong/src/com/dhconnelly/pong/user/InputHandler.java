package com.dhconnelly.pong.user;

import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.util.logging.Logger;

import javax.swing.JComponent;

import com.dhconnelly.pong.Ball;
import com.dhconnelly.pong.Paddle;
import com.dhconnelly.pong.World;

public class InputHandler implements Runnable, KeyListener {

    private static final Logger log = Logger.getLogger(InputHandler.class.getName());
    private final JComponent container;
	private final World world;
	
	private volatile boolean leftDown;
	private volatile boolean rightDown;

	public InputHandler(JComponent container, World world) {
		this.container = container;
	    this.world = world;
	}

    @Override
	public void run() {
        container.setFocusable(true);
        container.requestFocus();
        container.addKeyListener(this);
	}

    @Override
    public void keyPressed(KeyEvent event) {
        log.info("Key pressed");
        
        if (event.getKeyCode() == KeyEvent.VK_LEFT) {
            Paddle player = world.getPlayer();
            synchronized (player) {
                if (rightDown) {
                    player.stop();
                    log.info("VX = " + player.getVx());
                } else if (player.getX() >= world.getLeftBoundary()) {
                    player.goLeft();
                    log.info("VX = " + player.getVx());
                }
            }
            leftDown = true;
        } else if (event.getKeyCode() == KeyEvent.VK_RIGHT) {
            Paddle player = world.getPlayer();
            synchronized (player) {
                if (leftDown) {
                    player.stop();
                    log.info("VX = " + player.getVx());
                } else if (player.getX() + player.getWidth() < world.getRightBoundary()) {
                    player.goRight();
                    log.info("VX = " + player.getVx());
                }
            }
            rightDown = true;
        } else if (event.getKeyCode() == KeyEvent.VK_SPACE) {
            Ball ball = world.getBall();
            synchronized (ball) {
                if (!ball.isLaunched()) {
                    ball.launch();
                }
            }
        }
        
    }

    @Override
    public void keyReleased(KeyEvent event) {
        log.info("Key released");
        Paddle player = world.getPlayer();
        
        if (event.getKeyCode() == KeyEvent.VK_LEFT) {
            if (rightDown) {
                synchronized (player) {
                    player.goRight();
                    log.info("VX = " + player.getVx());
                }
            } else {
                synchronized (player) {
                    player.stop();
                    log.info("VX = " + player.getVx());
                }
            }
            leftDown = false;
        } else if (event.getKeyCode() == KeyEvent.VK_RIGHT) {
            if (leftDown) {
                synchronized (player) {
                    player.goLeft();
                    log.info("VX = " + player.getVx());
                }
            } else {
                synchronized (player) {
                    player.stop();
                    log.info("VX = " + player.getVx());
                }
            }
            rightDown = false;
        } 
    }

    @Override
    public void keyTyped(KeyEvent event) {
        // ignore
    }
}
