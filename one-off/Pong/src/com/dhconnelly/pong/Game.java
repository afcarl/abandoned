package com.dhconnelly.pong;

import java.util.logging.Logger;

import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.SwingUtilities;

import com.dhconnelly.pong.ai.AiPlayer;
import com.dhconnelly.pong.physics.PhysicsHandler;
import com.dhconnelly.pong.render.MainPanel;
import com.dhconnelly.pong.render.Renderer;
import com.dhconnelly.pong.user.InputHandler;

public class Game {

    private static final int DEFAULT_WIDTH = 800;
    private static final int DEFAULT_HEIGHT = 600;
    private static final int WIN_SCORE = 3;
    private static final Logger log = Logger.getLogger(Game.class.getName());
    
    public static void main(String[] args) {
        Game game = new Game();
        game.go();
    }
    
    private final JFrame frame = new JFrame("Pong");
    private final MainPanel panel = new MainPanel(DEFAULT_WIDTH, DEFAULT_HEIGHT);
	private final World world = new World(0, 800, 0, 600);
	
	public Game() {
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	    frame.add(panel);
	    frame.pack();
	    frame.setVisible(true);
	}
	
	public void go() {
	    log.info("Starting game");
	    
		Renderer renderer = new Renderer(panel, world);
		InputHandler input = new InputHandler(panel, world);
		PhysicsHandler physics = new PhysicsHandler(this, world);
		AiPlayer ai = new AiPlayer(world, world.getOpponent());
		
		SwingUtilities.invokeLater(renderer);
		new Thread(input).start();
		new Thread(physics).start();
		new Thread(ai).start();
	}

    public void playerScored() {
        Paddle player = world.getPlayer();
        boolean won = false;
        synchronized (player) {
            player.setScore(player.getScore() + 1);
            if (player.getScore() == WIN_SCORE) {
                won = true;
            }
        }
        
        world.resetPositions();
        if (won) {
            SwingUtilities.invokeLater(new Runnable() {
                @Override
                public void run() {
                    JOptionPane.showMessageDialog(null, "You won!");
                }
            });
            player.setScore(0);
            world.getOpponent().setScore(0);
        }
    }

    public void opponentScored() {
        Paddle opponent = world.getOpponent();
        boolean won = false;
        synchronized (opponent) {
            opponent.setScore(opponent.getScore() + 1);
            if (opponent.getScore() == WIN_SCORE) {
                won = true;
            }
        }
        
        world.resetPositions();
        if (won) {
            SwingUtilities.invokeLater(new Runnable() {
                @Override
                public void run() {
                    JOptionPane.showMessageDialog(null, "You lost.");
                }
            });
            opponent.setScore(0);
            world.getPlayer().setScore(0);
        }
    }
}
