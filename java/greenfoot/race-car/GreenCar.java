import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * Write a description of class GreenCar here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class GreenCar extends Actor
{
    private int x;
    private int y;
    
    public GreenCar(World world) {
        int wWidth = world.getWidth();
        int wHeight = world.getHeight();
        int iWidth = getImage().getWidth();
        int iHeight = getImage().getHeight();
        
        x = (wWidth / 2) - (iWidth / 2);
        y = wHeight - (iHeight / 2);
    }
    /**
     * Act - do whatever the GreenCar wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void act() 
    {
        if (Greenfoot.isKeyDown("left")) {
            x = x - 1;
        } else if (Greenfoot.isKeyDown("right")) {
            x = x + 1;
        } else if (Greenfoot.isKeyDown("up")) {
            y = y - 1;
        } else if (Greenfoot.isKeyDown("down")) {
            y = y + 1;
        }
        setLocation(x, y);
        checkCollision();
    }    
    
    public void checkCollision() {
        RedCar redCar = (RedCar) getOneIntersectingObject(RedCar.class);
        if (null != redCar) {
            Greenfoot.stop();
        }
    }
    
    public int getX() { return x; }
    public int getY() { return y; }
}
