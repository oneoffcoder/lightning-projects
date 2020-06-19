import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * Write a description of class Score here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Score extends Actor
{
    private MyWorld world;
    
    public Score(MyWorld world) {
        this.world = world;
    }
    
    /**
     * Act - do whatever the Score wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void act() 
    {
        String s = "Level " + world.getLevel() + ", Score: " + world.getScore();
        GreenfootImage img = new GreenfootImage(s, 24, Color.GREEN, Color.BLACK);
        setImage(img);
    }    
}
