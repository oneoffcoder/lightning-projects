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
        /*if (Greenfoot.isKeyDown("w")) {
            setLocation(getX(), getY() - 1);
        } else if (Greenfoot.isKeyDown("s")) {
            setLocation(getX(), getY() + 1);
        } else if (Greenfoot.isKeyDown("a")) {
            setLocation(getX() - 1, getY());
        } else if (Greenfoot.isKeyDown("d")) {
            setLocation(getX() + 1, getY());
        }*/
        if (Greenfoot.isKeyDown("w")) {
            setRotation(-90);
            move(5);
        } else if (Greenfoot.isKeyDown("s")) {
            setRotation(90);
            move(5);
        } else if (Greenfoot.isKeyDown("a")) {
            setRotation(180);
            move(5);
        } else if (Greenfoot.isKeyDown("d")) {
            setRotation(0);
            move(5);
        }
        /*if (Greenfoot.isKeyDown("w")) {
            turn(-1);
            move(5);
        } else if (Greenfoot.isKeyDown("s")) {
            turn(1);
            move(5);
        } else if (Greenfoot.isKeyDown("a")) {
            turn(-1);
            move(5);
        } else if (Greenfoot.isKeyDown("d")) {
            turn(1);
            move(5);
        }*/
        this.x = getX();
        this.y = getY();
    }    
}
