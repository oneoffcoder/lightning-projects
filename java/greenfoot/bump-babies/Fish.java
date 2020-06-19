import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * Write a description of class Fish here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Fish extends Actor
{
    /**
     * Act - do whatever the Fish wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void act() 
    {
        try {
            MouseInfo mouseInfo = Greenfoot.getMouseInfo();
            if (null != mouseInfo) {
                setLocation(mouseInfo.getX(), mouseInfo.getY());
            }
        } catch (Exception e) {
            // swallow exception
        }
        
        babyHitDetection();
    }    
    
    public void babyHitDetection() {
        Actor actor = getOneIntersectingObject(Baby.class);
        if (actor != null) {
            Baby baby = (Baby) actor;
            ((MyWorld)getWorld()).remove(actor);
        }
    }
}
