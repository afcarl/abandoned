package com.dhconnelly.pong.render;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

import javax.swing.JPanel;

@SuppressWarnings("serial")
public class MainPanel extends JPanel {

    private static final Color COLOR = Color.BLACK;
    private static final Logger log = Logger.getLogger(MainPanel.class.getName());
    
    private List<Drawable> stuff = new ArrayList<Drawable>();
    private volatile int playerScore;
    private volatile int opponentScore;
    
    public MainPanel(int width, int height) {
        setPreferredSize(new Dimension(width, height));
        setBackground(COLOR);
    }
    
    public synchronized void update(List<Drawable> stuff) {
        this.stuff = stuff;
        repaint();
    }
    
    @Override
    public void paintComponent(Graphics g) {
        log.fine("Repainting");
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        
        synchronized (this) {
            for (Drawable thing : stuff) {
                g2.setColor(thing.getColor());
                g2.fill(thing.getShape());
            }
        }

        g2.setColor(Color.WHITE);
        g2.drawString("Player: " + playerScore, 700, 20);
        g2.drawString("Opponent: " + opponentScore, 700, 40);
    }

    public synchronized void updateScore(int playerScore, int opponentScore) {
        this.playerScore = playerScore;
        this.opponentScore = opponentScore;
    }
}
