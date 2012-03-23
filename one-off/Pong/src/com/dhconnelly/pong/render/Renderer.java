package com.dhconnelly.pong.render;

import java.util.logging.Logger;

import com.dhconnelly.pong.World;

public class Renderer implements Runnable {

    private static final Logger log = Logger.getLogger(Renderer.class.getName());
	private static final int FRAME_RATE = 50;

	private final MainPanel panel;
	private final World world;

	public Renderer(MainPanel panel, World world) {
		this.world = world;
		this.panel = panel;
	}
	
	@Override
	public void run() {
	    log.info("Starting renderer");
		Thread updater = new Thread(new Runnable() {
		    public void run() {
		        while (true) {
		            panel.update(world.getDrawables());
		            panel.updateScore(world.getPlayer().getScore(),
		                              world.getOpponent().getScore());
		            
		            try {
		                Thread.sleep(1000 / FRAME_RATE);
		            } catch (InterruptedException e) {
		                log.info("Thread interrupted while sleeping");
		            }
		        }
		    }
		});
		updater.start();
	}

}
