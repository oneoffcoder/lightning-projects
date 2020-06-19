import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.util.List;
import java.util.ArrayList;
import java.util.Random;

/**
 * Write a description of class MyWorld here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class MyWorld extends World
{
    private static final Random _rand = new Random(37L);
    GreenCar greenCar;
    List<RedCar> redCars;
    List<Integer> xPositions;
    List<Integer> xHistory;
    long numRedCarsAdded = 0L;
    int maxRedCars = 5;
    /**
     * Constructor for objects of class MyWorld.
     * 
     */
    public MyWorld()
    {    
        // Create a new world with 600x400 cells with a cell size of 1x1 pixels.
        super(600, 600, 1); 
        Greenfoot.setSpeed(65);
        
        xHistory = new ArrayList<>();
        xPositions = getXPositions();
        
        greenCar = new GreenCar(this);
        redCars = new ArrayList<>();
        
        addObject(greenCar, greenCar.getX(), greenCar.getY());
        addObject(new Score(this), 85, 10);
        addRedCar();
    }
    
    public void act() {
        super.act();
        if (redCars.size() < maxRedCars) {
            double p = _rand.nextDouble();
            double t = (numRedCarsAdded < 5) ? 0.995d : 0.99d;
            if (p > t) {
                addRedCar();
            }
        }
    }
    
    private void addRedCar() {
        RedCar redCar = new RedCar(getRandomXPosition());
        redCars.add(redCar);
        addObject(redCar, redCar.getX(), redCar.getY());
        numRedCarsAdded += 1L;
        if (numRedCarsAdded % 50 == 0) {
            maxRedCars += 1;
        }
    }
    
    public void removeRedCar(RedCar redCar) {
        redCars.remove(redCar);
        removeObject(redCar);
    }
    
    public long getScore() { return numRedCarsAdded; }
    
    public int getLevel() { return maxRedCars - 5 + 1; }
    
    private int getRandomXPosition() {
        int numPositions = xPositions.size();
        int index = -1;
        while (true) {
            index = _rand.nextInt(numPositions);
            
            if (!xHistory.contains(index)) {
                xHistory.add(index);
                break;
            }
        }
        
        if (xHistory.size() > 5) {
            xHistory.remove(0);
        }
        
        return xPositions.get(index);
    }
    
    private List<Integer> getXPositions() {
        int carWidth = (new RedCar()).getWidth();
        int gameWidth = getWidth();
        List<Integer> positions = new ArrayList<>();
        for (int i = 5; i < gameWidth; i += carWidth) {
            positions.add(i);
        }
        return positions;
    }
}
