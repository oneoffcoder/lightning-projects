 import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * Write a description of class Bug here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Bug extends Actor
{
    GreenfootSound sound = new GreenfootSound("ahhh.wav");
    /**
     * Act - do whatever the Bug wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void act() 
    {
        // Add your action code here.
        movement();
        if (isTouching(Bee.class)) {
            sound.play();
            removeTouching(Bee.class);
            Greenfoot.stop();
        }
    }    
     
    public void movement() {
        int dx = 2;
        int dy = 2;
        
        if (getX() < Bee.x) {
            setRotation(0);
            move((int)(Math.random() * dx) + 1);
        } else if (getX() > Bee.x) {
            setRotation(180);
            move((int)(Math.random() * dx) + 1);
        } 
        if (getY() < Bee.y) {
            setRotation(90);
            move((int)(Math.random() * dy) + 1);
        } else if (getY() > Bee.y) {
            setRotation(270);
            move((int)(Math.random() * dy) + 1);
        }
    }
}
