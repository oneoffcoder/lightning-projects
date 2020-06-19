import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.util.List;
import java.util.ArrayList;
import java.util.Random;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Write a description of class MyWorld here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class MyWorld extends World
{
    private static final Random _rand = new Random(37L);
    private static final AtomicInteger _babyCounter = new AtomicInteger(0);
    
    Fish fish;
    List<Baby> babies;
    final int numBabies = 20;
    /**
     * Constructor for objects of class MyWorld.
     * 
     */
    public MyWorld()
    {    
        // Create a new world with 600x400 cells with a cell size of 1x1 pixels.
        super(600, 400, 1); 
        
        fish = new Fish();
        addObject(fish, getWidth() / 2, getHeight() / 2);
        
        babies = new ArrayList();
        for (int i = 0; i < numBabies; i++) {
            Baby baby = nextBaby();
            babies.add(baby);
            addObject(baby, baby.getX(), baby.getY());
        }
        
    }
    
    private Baby nextBaby() {
        int x = _rand.nextInt(getWidth());
        int y = _rand.nextInt(getHeight());
        Baby baby = new Baby(_babyCounter.getAndIncrement(), x, y);
        System.out.println(baby.getId());
        return baby;
    }
    
    public void remove(Actor actor) {
        babies.remove(actor);
        removeObject(actor);
        
        int threshold = _rand.nextInt(100) + 1;
        if (babies.size() <= threshold) {
            int numToAdd = _rand.nextInt(5) + 1;
            for (int i = 0; i < numToAdd; i++) {
                Baby baby = nextBaby();
                babies.add(baby);
                addObject(baby, baby.getX(), baby.getY());
            }
        }
    }
}
