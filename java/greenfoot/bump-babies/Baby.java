import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.util.Random;

/**
 * Write a description of class Baby here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Baby extends Actor
{
    private static final Random _rand = new Random(37L);
    private int id;
    private int x;
    private int y;
    private int xDelta;
    private int yDelta;
    
    public Baby(int id, int x, int y) {
        this.id = id;
        this.x = x;
        this.y = y;
        this.xDelta = _rand.nextDouble() < 0.5d ? -1 : 1;
        this.yDelta = _rand.nextDouble() < 0.5d ? -1 : 1;
    }
    
    public int getId() { return id; }
    public int getX() { return x; }
    public int getY() { return y; }
    /**
     * Act - do whatever the Baby wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void act() {
        x = x + xDelta;
        y = y + yDelta;
        
        setLocation(x, y);
        
        if (x == 0 || x == getWorld().getWidth()) {
            xDelta = xDelta * -1;
        }
        if (y == 0 || y == getWorld().getHeight()) {
            yDelta = yDelta * -1;
        }
    }    
}
