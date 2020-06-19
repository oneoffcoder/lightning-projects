import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.util.Random;

/**
 * Write a description of class RedCar here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class RedCar extends Actor
{
    private static final Random _rand = new Random(37L);
    
    private int x;
    private int y;
    
    public RedCar() {
        x = 0;
        y = 0;
    }
    
    public RedCar(int x) {
        this.x = x;
        this.y = getImage().getHeight() / 2;
    }
    
    public RedCar(World world) {
        int wWidth = world.getWidth();
        int wHeight = world.getHeight();
        int iHeight = getImage().getHeight();
        
        x = _rand.nextInt(wWidth);
        y = iHeight / 2;
    }
    /**
     * Act - do whatever the RedCar wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void act() 
    {
        y = y + 1;
        setLocation(x, y);
        if (isAtEdge()) {
            ((MyWorld)getWorld()).removeRedCar(this);
        }
    }    
    
    public int getX() { return x; }
    public int getY() { return y; }
    public int getWidth() { return getImage().getWidth(); }
    public int getHeight() { return getImage().getHeight(); }
}
