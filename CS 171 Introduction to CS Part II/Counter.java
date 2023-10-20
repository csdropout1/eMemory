public class Counter {

    private int count;

    public Counter() {}
    public Counter(int initial){
        count = initial;
    }
    public int getCount(){
        return count;
    }
    public void increment(){
        count++;
    }
    public void reset() {
        count = 0;
    }
}








