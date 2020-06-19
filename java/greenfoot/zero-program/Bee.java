import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * Write a description of class Bee here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Bee extends Actor
{
    static int x, y;
    /**
     * Act - do whatever the Bee wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void act() 
    {
        // Add your action code here.
        if (Greenfoot.isKeyDown("w") || Greenfoot.isKeyDown("up")) {
            setRotation(-90);
            move(5);
        } else if (Greenfoot.isKeyDown("s") || Greenfoot.isKeyDown("down")) {
            setRotation(90);
            move(5);
        } else if (Greenfoot.isKeyDown("a") || Greenfoot.isKeyDown("left")) {
            setRotation(180);
            move(5);
        } else if (Greenfoot.isKeyDown("d") || Greenfoot.isKeyDown("right")) {
            setRotation(0);
            move(5);
        }
        this.x = getX();
        this.y = getY();
    }    
}
